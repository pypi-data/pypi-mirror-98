# curl2pyreqs

A library to convert curl to python requests file.

## Requirement

Python >= 3.6

pyperclip >= 1.8.0

rich >= 9.13.0

On Linux, xclip or xsel needed:

```Shell
sudo apt-get install xclip
or
sudo apt-get install xsel

```

## Install

```Bash
$ pip install curl2pyreqs
```

## Usage

### Use as binary

-   Export curl request file to python script.

```Bash
$ curl2pyreqs -F example.curl
Convertion Finished.
Please open example.py to check the code.
```

-   Convert curl request in the clipboard and paste the requests code back

```Bash
$ curl2pyreqs
Convertion Finished.
Now requests code is copyed in your clipboard.
```

### Use by importing

-   Convert a curl string to python-requests, copyed from Chrome or Firefox:

```Python
>>> from curl2pyreqs.ulti import parseCurlString
>>> output = parseCurlString("""curl -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'accept-language: en-US,en;q=0.5' --compressed -H 'upgrade-insecure-requests: 1' -H 'te: trailers' https://pypi.org/""")
>>> print(output)
```

-   Convert curl file stream to python-requests, copyed from Chrome or Firefox:

```Python
>>> from curl2pyreqs.ulti import parseCurlFile
>>> output = parseCurlFile('./example.curl')
>>> print(output)
```

## README_CN

[中文版说明](https://github.com/knightz1224/curl2pyreqs/blob/main/README_CN.md)
