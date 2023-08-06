from setuptools import setup, find_packages

from scielodump import VERSION

install_requires = [
    "requests==2.25.0",
    "xylose==1.35.4",
    "progressbar2==3.53.1",
]

tests_require = [
]

setup(
    name="scielodump",
    version=VERSION,
    description="Library to dump articles in XML and PDF formats from SciELO Collections",
    author="Fabio Batalha",
    author_email="fabiobatalha@gmail.com",
    maintainer="Fabio Batalha",
    maintainer_email="fabiobatalha@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ],
    dependency_links=[],
    tests_require=tests_require,
    test_suite='tests',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'scielo-dump=scielodump.dump_corpus:main',
        ]
    }
)
