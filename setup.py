import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrapy-requests",  # Replace with your own username
    version="0.1.0",
    author="Refael Yzg",
    author_email="rafi.yzgeav@gmail.com",
    description="Scrapy with requests-html",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rafyzg/scrapy-requests",
    packages=setuptools.find_packages(),
    install_requires=[
        'scrapy>=1.0.0',
        'requests-html>=0.10.0',
    ],
    tests_require = [
        'pytest>=6.1.0',
        'codecov',
        'pytest-cov',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)
