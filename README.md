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
This program support CLI mode and interactive mode. You will be asked to enter a path for storing the .HTML file, the path will be stored in the config file ```library.json```. The config file will also be used to store the book information in the library.

### CLI mode

#### Optional arguments reference
```
usage: syosetu.py [-h] [-a <URL>] [-r <book title>] [-e <book title>] [-d <URL>] [-u] [-ad <URL>]

optional arguments:
  -h, --help            show this help message and exit
  -a <URL>, --add <URL>
                        add a book to the library
  -r <book title>, --remove <book title>
                        remove a book from the library
  -e <book title>, --end <book title>
                        mark a book as ended, a book marked as ended will not be checked for update
  -d <URL>, --download <URL>
                        download the book from the given URL
  -u, --update          update the book in the library
  -ad <URL>             add a book to the library and then download the book from the given URL
```

### Interactive mode

#### Menu page
```
user@ubuntu:~$ python3 syosetu.py
===== Menu =====
1. Display all books in the library
2. Add book to library
3. Remove book from library
4. Download the light novel from web
5. Update the light novel in the library
0. Exit the program
Your option:
```
Remarks:  
Option 4 will **ONLY** download the book, but **NOT** adding the light novel to library. If you want to add the book to the library and download all chapters, you may follow the below sample.

### Sample
```
user@ubuntu:~$ python3 syosetu.py
===== Menu =====
1. Display all books in the library
2. Add a book to the library
3. Remove a book from the library
4. Mark a book as ended
5. Download the book from web
6. Update the book in the library
0. Exit the program
Your option: 2
URL: https://ncode.syosetu.com/n4843br/
Successfully added 宝石吐きの女の子 to library.
===== Menu =====
1. Display all books in the library
2. Add a book to the library
3. Remove a book from the library
4. Mark a book as ended
5. Download the book from web
6. Update the book in the library
0. Exit the program
Your option: 6
===== Update =====
Updating 宝石吐きの女の子
Downloading 宝石吐きの女の子
Progress: 277/277
Done.
===== Menu =====
1. Display all books in the library
2. Add a book to the library
3. Remove a book from the library
4. Mark a book as ended
5. Download the book from web
6. Update the book in the library
0. Exit the program
Your option: 0
user@ubuntu:~$
```
Remarks:  
If you use the above method to download the book, the chapter number will be appended to the filename automatically.

```
user@ubuntu:~$ python3 syosetu.py
===== Menu =====
1. Display all books in the library
2. Add a book to the library
3. Remove a book from the library
4. Mark a book as ended
5. Download the book from web
6. Update the book in the library
0. Exit the program
Your option: 5
URL: https://ncode.syosetu.com/n8356ga/
Download range (A for all, or enter a range separtaed by comma): a
Append chapter number to the filename? (Y/n): y
Downloading サイレント・ウィッチ
Progress: 236/236
Done.
===== Menu =====
1. Display all books in the library
2. Add book to library
3. Remove book from library
4. Download the light novel from web
5. Update the light novel in the library
0. Exit the program
Your option: 0
user@ubuntu:~$
```
Remarks:  
For option 4, the download range will be set to **all** and chapter number **will be append** to the filename if nothing is entered.  
**If you downloaded that book before and want to update the content to the lastest chapter, simply enter nothing for both questions.**
