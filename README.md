ChatGPT-GUI
===============
An unofficial GUI app for the ChatGPT backend API.

------------------------------

[![MIT License](https://img.shields.io/github/license/Cubicpath/ChatGPT-GUI?style=for-the-badge)][license]

[![PyPI](https://img.shields.io/pypi/v/chatgpt-gui?label=PyPI&logo=pypi&style=flat-square)][homepage]
[![Python](https://img.shields.io/pypi/pyversions/chatgpt-gui?label=Python&logo=python&style=flat-square)][python]
[![CPython](https://img.shields.io/pypi/implementation/chatgpt-gui?label=Impl&logo=python&style=flat-square)][python]

------------------------------

**Note: This project is in a public alpha, and as such, many features are not complete.**

### Disclaimer:
_**ChatGPT-GUI is in no way associated with, endorsed by, or otherwise affiliated with OpenAI.**_

### Other Documents:
- [Changelog][changelog_github]
- [License][license_github]

### Table of Contents
- [About](#about)
- [How to Use](#how-to-use)
     - [Installation](#installation)
     - [Authentication](#authentication)
     - [Themes](#themes)
          - [Theme File Structure](#theme-file-structure)


About:
---------------
ChatGPT-GUI is a GUI application written using [Qt for Python][PySide] that allows you to easily use
[ChatGPT] API endpoints.

This project is a fork of my other project, [HaloInfiniteGetter](https://github.com/Cubicpath/HaloInfiniteGetter).

How to Use:
---------------

### Installation:
- First, install Python 3.10 using [this link][python310]
- Then, open command prompt (Win + R -- type in "cmd") and type `pip install chatgpt-gui`
  - Optionally, to install the latest unstable version, type `pip install git+https://github.com/Cubicpath/ChatGPT-GUI.git`
- And you are done! To launch the program simply type `chatgpt`
  - Once launched, you can create a desktop shortcut by using the `Create Desktop Shortcut` tool
under the `Tools` context menu

### Authentication:
...

### Themes:
Themes are a way to style already-existing elements (Think CSS). They are held in a directory with their resources
and stylesheet in the same folder level.

#### Theme File Structure:
    ../
    │
    ├───[theme_id]/
    │       ├─── [icon1_name].svg
    │       ├─── [icon2_name].svg
    │       ├─── [icon3_name].svg
    │       └─── stylesheet.qss
    │

The current builtin themes are:
- `Breeze Dark`
- `Breeze Light`
- `Legacy (Default Qt)`

While the current breeze themes are slightly modified versions, you can view the original themes at [BreezeStyleSheets].

[BreezeStyleSheets]: https://github.com/Alexhuszagh/BreezeStyleSheets "BreezeStyleSheets"
[changelog_github]: https://github.com/Cubicpath/ChatGPT-GUI/blob/master/CHANGELOG.md "Changelog"
[ChatGPT]: https://https://chat.openai.com "ChatGPT"
[homepage]: https://pypi.org/project/chatgpt-gui/ "ChatGPT-GUI PyPI"
[license]: https://choosealicense.com/licenses/mit "MIT License"
[license_github]: https://github.com/Cubicpath/ChatGPT-GUI/blob/master/LICENSE "MIT License"
[PySide]: https://pypi.org/project/PySide6/ "PySide6"
[python]: https://www.python.org "Python"
[python310]: https://www.python.org/downloads/release/python-3100/ "Python 3.10"