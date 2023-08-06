import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="soco-tokenizer",
    version="1.0",
    author="tianchez",
    description="Fast tokenizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.soco.ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'numpy >= 1.15.3',
        'boto3 >= 1.9.46',
        'oss2 >= 2.6.0',
        'scipy >= 1.2.1',
        'transformers == 2.11.0',
        'tqdm >= 4.45.0',
        'nltk >= 3.5',
        'jieba >= 0.42.1',
        'spacy >= 2.2.4',
        'requests >= 2.23.0'
    ]
)
