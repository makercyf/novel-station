# syosetu-downloader
A simple downloader for ncode.syosetu.com. The downloaded content will be saved in .html format.

## Requirements
1. [Requests](https://github.com/psf/requests)
2. [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)

You can install the packages via PyPI  
```sh
pip3 install requests && pip3 install beautifulsoup4
```

## Usage
### Recommended
```
user@ubuntu:~$ python3 syosetu.py
URL: https://ncode.syosetu.com/n4843br/

Download range (A for all, or enter a range separtaed by comma): 
Append chapter number to the filename? (Y/n): 

Downloading 宝石吐きの女の子
Progress: 277/277
Done
user@ubuntu:~$
```
Remarks:  
If you do not enter anything, the download range will be set to **all** and chapter number **will be append** to the filename.  
**If you downloaded that light novel before and want to update the content to the lastest chapter, simply enter nothing for both questions.**

### Sample
```
user@ubuntu:~$ python3 syosetu.py
URL: https://ncode.syosetu.com/n4843br/

Download range (A for all, or enter a range separtaed by comma): a
Append chapter number to the filename? (Y/n): y

Downloading 宝石吐きの女の子
Progress: 277/277
Done
user@ubuntu:~$
```

```
user@ubuntu:~$ python3 syosetu.py
URL: https://ncode.syosetu.com/n4843br/

Download range (A for all, or enter a range separtaed by comma): 250,end
Append chapter number to the filename? (Y/n): 

Downloading 宝石吐きの女の子
Progress: 277/277
Done
user@ubuntu:~$
```
