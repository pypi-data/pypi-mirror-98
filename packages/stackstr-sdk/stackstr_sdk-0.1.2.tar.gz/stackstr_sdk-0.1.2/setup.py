from setuptools import setup
import os


def get_version_from_tag() -> str:
    if os.getenv('CIRCLE_TAG') is None:
        if os.getenv('ENV') != 'dev':
            exit(1)
        else:
            return '0.0.0'

    return os.getenv('CIRCLE_TAG').replace('v', '')


setup(
    name='stackstr_sdk',
    version=get_version_from_tag(),
    author='StackStr Eng',
    author_email='founders@stackstr.io',
    packages=['stackstr'],
    description='SDK to log predictions and ground truth',
    install_requires=[
        "certifi == 2020.11.8",
        "chardet == 3.0.4",
        "idna == 2.10",
        "joblib == 1.0.0",
        "numpy == 1.19.5",
        "pandas == 1.2.0",
        "python-dateutil == 2.8.1",
        "pytz == 2020.5",
        "requests == 2.25.0",
        "scikit-learn == 0.24.0",
        "scipy == 1.6.0",
        "six == 1.15.0",
        "sklearn == 0.0",
        "threadpoolctl == 2.1.0",
        "urllib3 == 1.26.2",
    ],
)