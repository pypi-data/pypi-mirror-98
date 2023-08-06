"""
A module to performatically iterate through SciELO API to download JATS XML of each article and
PDF files.

SciELO Metadata has performance issues to iterate (paginate) in queries containing lots of
records. This module works with a delta of time, spliting queries using this delta time and
consequently, reducing drastically the number of records to iterated (paginate).
"""

import os
import argparse
import logging
import tempfile
import shutil
import json
from progressbar import progressbar

from datetime import datetime, timedelta

import requests
from requests.exceptions import RequestException

from xylose.scielodocument import Article


logger = logging.getLogger()

API_HOST = "http://articlemeta.scielo.org"
XML_URL = f"{API_HOST}/api/v1/article/"
# ?collection={col}&code={pid}&format={fmt}
COLLECTIONS_URL = f"{API_HOST}/api/v1/collection/identifiers/"
ARTICLE_IDENTIFIERS_URL = f"{API_HOST}/api/v1/article/identifiers/"
# ?collection={col}&from={from_dt}&limit={limit}&offset={offset}
ARTICLE_URL = f"{API_HOST}/api/v1/article/"
# ?collection={col}&code={article_id}&format={xmlrsps}

LIMIT = 500
TIMEDELTA = 30


class SciELODumpException(Exception):
    pass


def do_request(url, params=None):
    try:
        result = requests.get(url, params=params)
    except RequestException as exc:
        logger.error(f'Fail to retrived data from {url}, {exc}')
        raise SciELODumpException

    if result.status_code != 200:
        raise SciELODumpException

    return result

class SciELOMetadata:

    def __init__(self):
        self._collections = {}
        self._articles_identifiers = {}

    @property
    def collections(self):

        if self._collections:
            return self._collections

        collections = do_request(COLLECTIONS_URL).json()
        for collection in collections:
            self._collections[collection['code']] = collection
            raise SciELODumpException

        return self._collections

    def get_article_identifiers(self, from_date='1997-01-01', until_date=None, collection=None):
        until_date = datetime.strptime(until_date, '%Y-%m-%d') if until_date else datetime.now()
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        next_date = from_date + timedelta(days=TIMEDELTA)
        params = {
            "from": from_date.strftime('%Y-%m-%d'),
            "until": next_date.strftime('%Y-%m-%d'),
            "limit": LIMIT,
            "offset": 0
        }

        while True:
            logger.debug(params)
            response = do_request(
                ARTICLE_IDENTIFIERS_URL,
                params=params
            )
            articles = response.json()
            for article in articles['objects']:
                yield article['collection'], article['code']

            if len(articles['objects']) == 0:
                from_date =  next_date + timedelta(days=1)
                params['from'] = from_date.strftime('%Y-%m-%d')
                next_date = next_date + timedelta(days=TIMEDELTA)
                params['until'] = next_date.strftime('%Y-%m-%d')
                params['offset'] = 0
            else:
                params['offset'] += LIMIT

            if len(articles['objects']) == 0 and next_date > until_date:
                break



    def get_article_xml(self, collection, article_id):
        params = {
            "collection": collection,
            "code": article_id,
            "format": "xmlrsps"
        }
        article = do_request(
            ARTICLE_URL,
            params=params
        ).content

        return article

    def get_article_meta(self, collection, article_id):
        params = {
            "collection": collection,
            "code": article_id
        }
        article = do_request(
            ARTICLE_URL,
            params=params
        )

        try:
            article_data = article.json()
        except json.decoder.JSONDecodeError:
            raise SciELODumpException

        return Article(article_data)


def get_identifiers_from_file_system(data_source):
    local_identifiers = set()
    for path, dirs, files in os.walk(data_source):
        if not dirs and files:
            splited_path = path.replace(data_source, '').split('/')
            if not splited_path[0]:
                splited_path = splited_path[1:]
            collection = splited_path[0]
            article_identifier = ''.join(splited_path[1:])
            article_identifier = f'S{article_identifier}'
            local_identifiers.add(f'{collection} {article_identifier}')

    return local_identifiers


def write_to_file(data, file_path):
    with open(file_path, 'wb') as output:
        output.write(data)


def run(from_date, until_date, data_source, differential=True, download_pdf=False, collection=None):
    client = SciELOMetadata()
    identifiers = set()
    local_identifiers = set()

    logger.info('Dumping SciELO Data')
    logger.info(f'From: {from_date}')
    logger.info(f'To: {until_date}')
    logger.info(f'Source Folder: {data_source}')
    logger.info(f'Differential: {differential}')
    os.makedirs(data_source, exist_ok=True)
    logger.info('Loading articles identifiers from SciELO Metadata API')
    for collection, identifier in client.get_article_identifiers(
        from_date=from_date, until_date=until_date, collection=collection):
        identifiers.add(f'{collection} {identifier}')

    if differential:
        logger.info('Loading articles identifiers from Source Data directory ')
        local_identifiers = get_identifiers_from_file_system(data_source)

    new_identifiers = identifiers - local_identifiers

    for identifier in progressbar(new_identifiers, redirect_stdout=True):
        with tempfile.TemporaryDirectory(prefix='scielodump_') as tmpdir:
            collection, article_id = identifier.split(' ')
            try:
                article_xml = client.get_article_xml(collection=collection, article_id=article_id)
                article_meta = client.get_article_meta(collection=collection, article_id=article_id)
            except SciELODumpException:
                logger.exception(SciELODumpException)
                continue

            xml_file = tmpdir + '/' + article_id + '.xml'
            write_to_file(article_xml, xml_file)

            if download_pdf:
                try:
                    pdfs = article_meta.fulltexts()['pdf']
                except KeyError:
                    continue

                for language, url in pdfs.items():
                    try:
                        article_pdf = do_request(url).content
                    except SciELODumpException:
                        logger.exception(SciELODumpException)
                        continue
                    pdf_file = tmpdir  + '/' + article_id + '_' + language + '.pdf'
                    write_to_file(article_pdf, pdf_file)

            # Move temporary dowloaded files to their final directory
            dirs = '/'.join([
                data_source,
                collection,
                article_id[1:10], # ISSN
                article_id[10:14], # YEAR
                article_id[14:18], # ISSUE CODE
                article_id[18:], # ARTICLE CODE
            ])
            os.makedirs(dirs, exist_ok=True)
            for file in os.listdir(tmpdir):
                try:
                    shutil.move(os.path.join(tmpdir, file), dirs, )
                except shutil.Error:
                    pass


def main():

    arg_parser = argparse.ArgumentParser(
        description="Run the processing to dump SciELO Data"
    )

    arg_parser.add_argument(
        '--from-date',
        '-f',
        default='1997-01-01',
        help='An iso date ex: YYYY-MM-AA. Default is setup to first SciELO processing year (1997)'
    )

    arg_parser.add_argument(
        '--until-date',
        '-u',
        default=datetime.now().isoformat()[0:10],
        help='An iso date ex: YYYY-MM-AA. Default is setup to current date.'
    )

    arg_parser.add_argument(
        '--data-source',
        '-s',
        default='data',
        help='Directory where the downloaded files will be stored.'
    )

    arg_parser.add_argument(
        '--download-pdf',
        '-p',
        default=False,
        action='store_true',
        help='Download PDF files. Large storage size is required. recomended 1.5Tb.'
    )

    arg_parser.add_argument(
        '--differential',
        '-d',
        action="store_true",
        help='Differential download only files that are not available in the data source directory'
    )

    arg_parser.add_argument(
        '--logging-level',
        '-l',
        default='DEBUG',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level'
    )

    args = arg_parser.parse_args()

    logging.basicConfig(
        level=args.logging_level,
        format="%(asctime)s - articlelogtransformer - %(levelname)s - %(message)s",
    )

    run(
        args.from_date,
        args.until_date,
        args.data_source,
        args.differential,
        args.download_pdf
    )
