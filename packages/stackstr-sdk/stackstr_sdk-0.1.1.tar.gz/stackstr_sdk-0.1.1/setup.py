from setuptools import setup

setup(
    name='stackstr_sdk',
    version='0.1.1',
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
