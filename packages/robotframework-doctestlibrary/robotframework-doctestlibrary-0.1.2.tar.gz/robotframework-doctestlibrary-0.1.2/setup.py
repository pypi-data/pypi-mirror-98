from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="robotframework-doctestlibrary",
    version="0.1.2",
    author="Many Kasiriha",
    author_email="many.kasiriha@dbschenker.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manykarim/robotframework-doctestlibrary",
    packages=find_packages(),
    install_requires=['imutils', 'numpy', 'opencv-python-headless', 'parsimonious', 'pytesseract', 'robotframework', 'scikit-image', 'Wand', 'pylibdmtx', 'pdfminer.six', 'deepdiff'],
    dependency_links=['https://github.com/tesseract-ocr/tesseract', 'https://www.ghostscript.com/download/gsdnld.html' , 'https://www.ghostscript.com/download/gpcldnld.html', 'https://imagemagick.org/script/download.php'],
    zip_safe=False
)