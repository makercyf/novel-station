# syosetu-downloader
A simple downloader for ncode.syosetu.com. The downloaded content shown in .html format.

## Requirements
1. [Requests](https://github.com/psf/requests)
2. [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)

You can install the packages via PyPI  
```sh
pip3 install requests && pip3 install beautifulsoup4
```

## Usage
### Windows:
```sh
python syosetu.py
```
### Linux:
```sh
python3 syosetu.py
```

### Sample
```
user@ubuntu:~$ python3 syosetu.py
URL: https://ncode.syosetu.com/n4843br/

Download range (A for all, or enter a range separtaed by comma): a
Append chapter number to the file? (Y/n): y

Downloading 宝石吐きの女の子
Progress: 277/277
Done
user@ubuntu:~$
```
