**About**

**ImageLibrary** is designed to automate cases involving various types of screen processing with RoboFramework.

*It operates with:*

- OpenCV
- TesseractOCR


**Installation**

pip install robotframework-imagelibrary

**Keywords**

[Keyword documentation](https://simakvokka.github.io/robotframework-imagelibrary/ImageLibrary.html)

*Installation Requirements*
- **[Python](https://www.python.org/downloads/)** **2.7**, **3.5+** 

- **Robot Framework**

- **[TesseractOCR](https://github.com/tesseract-ocr/tesseract)** 

    For number and text recognition. May not be installed if not planned to use. 
    Install the [3.02 version for your OS](https://github.com/tesseract-ocr/tesseract/wiki)


*Usage*

Implement the _ImageLibrary_ into robot test suite file with specifying the _output_ directory to store screenshots.

_Example_

**Library ImageLibrary ${CURDIR}${/}output**

Pass the image.png (with path) as _the template_ argument to the keyword.

_Example_

**Find Template    path\my_image.png**

