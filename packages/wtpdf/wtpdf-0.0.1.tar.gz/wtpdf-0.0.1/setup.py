import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='wtpdf',
    version='0.0.1',
    scripts=['wtpdf'],
    author="Jordan Patterson",
    author_email="jordanpatterson1939@gmail.com",
    description="Tool for saving webpages as pdf files from the terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jordanpatterson1939/youtube-cl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pdfkit'],
    python_requires='>=3',
)
