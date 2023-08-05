from setuptools import setup
from os.path import exists


requires = [
    "bs4",
    "requests"
]
long_description = open("readme.md", encoding="utf-8_sig").read() if exists("readme.md") else ""


setup(
    name='niconico_dl',
    version='1.0.2',
    description='ニコニコ動画ダウンロードモジュール。',
    url='https://github.com/tasuren/niconico_dl',
    author='tasuren',
    author_email='tasuren5@gmail.com',
    license='MIT',
    keywords='download video',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        "niconico_dl"
    ],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)