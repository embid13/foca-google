# NOTE
[![Fork](https://img.shields.io/github/forks/embid13/foca-google.svg?style=social)](https://github.com/embid13/foca-google/network/members)
[![Stars](https://img.shields.io/github/stars/embid13/foca-google.svg?style=social)](https://github.com/embid13/foca-google/stargazers)


This repository is a fork of [Original Repository](https://github.com/egorvinogradov/foca-google) and the original repository was created and maintained by [Original Author](https://github.com/egorvinogradov).

This fork aims to build upon the excellent work done in the original project by upgrading deprecated resources and improving existing functionality. I have also made some modifications to tailor the project to specific use cases.

The main differences are the replacement of deprecated function "find_elements_by_css_selector", among other details.

I encourage you to check out the original repository for more information on the work that this project is built upon.

# foca-google
`foca-google` searches and downloads documents from a specified domain using Google (e.g. PDFs, DOCs, XLS', RTFs, RARs etc — full list of extensions is listed on [lines 11-15](foca-google.py#L11)).

This is a partial alternative to the original [FOCA](https://github.com/ElevenPaths/FOCA) since Google Search doesn't work there sometimes.

### Example
If you want to find documents on `example.com`, run:

```
foca-google example.com
```

It will

1. Create a folder `example.com`
2. Download all found documents (PDFs, DOCs, XLS' etc) into `example.com` folder
3. Save URLs of all found documents into `example.com/0_log.txt`

Alternatively, run:

```
foca-google example.com <extension[e.g. pdf|docx|ppt etc]>
```
It will find and download only the files with the extension you specified.


### Installation
You must have `wget`, `pip` and Google Chrome installed.

1. Download [foca-google.py](foca-google.py)
2. `mv foca-google.py /usr/local/bin/foca-google`.
3. Install Selenium via pip: `pip install selenium`.
4. Install Selenium [Chrome Driver](https://developer.chrome.com/docs/chromedriver/downloads#current_releases) and also move the binary into `/usr/local/bin/`.
5. Linux users, see **Troubleshooting#1 (below)**
6. Your `foca-google` is ready to go.

### Troubleshooting
1. **Linux users:** on [line 60](foca-google.py#L60), change `user-data-dir` path to yours (where `{0}` is your user's home directory). You can find it at `chrome://version` => Profile Path (but remove "/Default" at the end of the path). If using Brave, `brave://version`.
2. If the script crashes with the error "Chrome is no longer running, so ChromeDriver is assuming that Chrome has crashed.", kill all Chrome entities and run the script again.
3. Let me know if you see any other errors (create an issue on Github).
