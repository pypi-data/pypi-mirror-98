import pathlib
import setuptools

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setuptools.setup(
    name="cnco",
    version="0.0.0",

    description="cnco python client",
    long_description=README,
    long_description_content_type="text/markdown",

    url="https://github.com/hizvi",
    author="cnco",
    author_email="hasangr8@gmail.com",

    classifiers=[
        "Programming Language :: Python :: 3",
    ],

    packages=setuptools.find_packages(),
    install_requires=[],
)