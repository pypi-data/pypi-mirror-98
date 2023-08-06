import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redditeasy",
    version="2.8.0",
    author="MakufonSkifto",
    description="RedditEasy is an API wrapper for the Reddit JSON API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MakufonSkifto/RedditEasy",
    packages=setuptools.find_packages(),
    install_requires=["requests", "python-dotenv"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    keywords="reddit api",
    python_requires='>=3.0',
)
