import requests
import re
import os
import lnlibrary
import argparse
from bs4 import BeautifulSoup
from typing import Tuple


class ln_downloader():
    def __init__(self):
        self.CSS = '''<style>
        #novel_ex { margin: 20px auto 50px; line-height: 180%; overflow: hidden; text-align: left; font-size:17px; }
        div.chapter_title {font-size: 110%; padding: 30px 0 0 0; font-weight:bold;}
        div.index_box { font-size: 17px;}
        dl.novel_sublist2 {overflow: hidden; border-bottom:1px solid #ffffff;}
        dl.novel_sublist2 dd{padding: 10px 10px 2px 5px; width: 515px; font-size: 17px; float:left;}
        </style>\n'''

        self.ILLEGAL_PATH_DICT = {'/': '／', ':': '：', '?': '？', '"': '\''}
        self.ILLEGAL_PATH_LIST = '<>|*\\'

        self.database_path = ""

    def urlValidation(self, url: str):
        try:
            r = requests.get(url, headers={"user-agent": 'Mozilla/5.0'})
        except:
            return False
        else:
            if r.status_code == 200:
                return r
            else:
                return False

    def getCode(self, url: str) -> Tuple[str, str] or bool:
        r = self.urlValidation(url)
        if r:
            url_split = url.split("/")
            if url_split[-1] == "":
                code = url_split[-2]
            else:
                code = url_split[-1]
            return r, code
        else:
            print("Your URL is invalid, please try again.")
            return False

    def getInfo(self, r, code):
        website = BeautifulSoup(r.text, 'html.parser')
        novel_title = website.title.string
        writer_name = website.find_all("div", class_="novel_writername")[0].find("a").string
        description = website.find(id="novel_ex")
        index = website.find_all("div", class_="index_box")[0]
        chapter_link = []
        table_of_content = website.find_all("a")
        for chapter in table_of_content:
            link = chapter.get("href")
            match = re.search(code + '/{1,}[0-9]', link)
            if match:
                full_chapter_link = "https://ncode.syosetu.com" + link
                chapter_link.append(full_chapter_link)
        largest_chapter = len(chapter_link)
        return novel_title, writer_name, description, index, chapter_link, largest_chapter

    def downloadRangeValidation(self, novel_title, download_range, largest_chapter) -> Tuple[int, int]:
        download_range = download_range.split(",")
        if len(download_range) == 2:
            if download_range[0].isnumeric() and download_range[1].isnumeric():
                first = int(download_range[0].strip())
                last = int(download_range[1].strip())
                if first < 0 or last > largest_chapter:
                    print("Download range is invalid, range set to all chapter")
                    first = 1
                    last = largest_chapter
            elif download_range[0].isnumeric() and download_range[1].upper() == "END":
                first = int(download_range[0].strip())
                last = largest_chapter
            else:
                print("Download range is invalid, range set to all chapter")
                first = 1
                last = largest_chapter
        else:
            if not os.path.isfile(f"{self.database_path}/{novel_title}/0. index.html"):
                first = 1
                last = largest_chapter
            else:
                with open(f"{self.database_path}/{novel_title}/0. index.html", "r", encoding="utf-8") as file:
                    for line in file:
                        if 'last =' in line:
                            first = int(re.sub('[^0-9]', '', line)) + 1
                            last = largest_chapter
                            break
        return first, last

    def chapterNumber(self, acn: str) -> bool:
        if acn == "N" or acn == "n":
            acn = False
        else:
            acn = True
        return acn

    def filenameValidation(self, filename: str) -> str:
        for character in self.ILLEGAL_PATH_LIST:
            if character in filename:
                print("Illgeal character in the filename Detected, program exit.")
                exit()
        for character in self.ILLEGAL_PATH_DICT.keys():
            if character in filename:
                filename = filename.replace(character, self.ILLEGAL_PATH_DICT[character])
        return filename

    def createIndexPage(self, novel_title: str, acn: bool, last, writer_name: str, description: str, index) -> None:
        with open(f"{self.database_path}/{novel_title}/0. index.html", "w", encoding="utf-8") as file:
            # Write must be str/NavigableString, not Tag
            file.write(f'<title>{novel_title}</title>\n')
            file.write(self.CSS)
            file.write(f'<!-- append = {acn} -->\n')
            file.write(f'<!-- last = {last} -->\n')
            file.write(f'<h1 style="text-align: center;">{novel_title}</h1>\n')
            file.write(f'<h2 style="text-align: center;">作者：{writer_name}</h2>\n')
            file.write(str(description))
            file.write(str(index))

    def updateIndexPage(self, novel_title: str, acn: bool, code, first: int, last: int, index) -> None:
        subtitle_list = index.find_all("a")
        with open(f"{self.database_path}/{novel_title}/0. index.html", "r+", encoding="utf-8") as file:
            content = file.read()
            for i in range(first, last):
                if acn:
                    filename = f"{i}. {subtitle_list[i-1].string}"
                else:
                    filename = subtitle_list[i-1].string
                filename = self.filenameValidation(filename)
                content = content.replace(f'"/{code}/{i}/"', f'"./{filename}.html" target="_blank"')
            file.seek(0)
            file.write(content)

    def downloadChapterContent(self, novel_title: str, acn: bool, chapter_link, first: int, last: int) -> None:
        for i in range(first, last + 1):
            website = requests.get(chapter_link[i-1], headers={"user-agent": 'Mozilla/5.0'}).text
            website = BeautifulSoup(website, 'html.parser')
            subtitle = website.find_all("p", class_="novel_subtitle")[0].string
            content = website.find_all("p")
            if acn:
                filename = f"{i}. {subtitle}"
            else:
                filename = subtitle
            filename = self.filenameValidation(filename)
            if filename:
                with open(f"{self.database_path}/{novel_title}/{filename}.html", "w", encoding="utf-8") as file:
                    file.write(f'<h1 style="text-align: center;">{subtitle}</h1>\n')
                    for line in content:
                        line = str(line)
                        match = re.search('id="L[0-9]{1,}', line)
                        if match:
                            file.write(line + "\n")
                print(f"Progress: {i}/{last}", end="\r")

    def download(self, interactive: bool, urlCLI: str, skip: bool) -> None:
        if interactive:
            url = input("URL: ")
        else:
            url = urlCLI
        web_response = self.getCode(url)
        if web_response:
            index_page = web_response[0]
            code = web_response[1]
            novel_title, writer_name, description, index, chapter_link, largest_chapter = self.getInfo(index_page, code)
            if skip:
                download_range = ""
            else:
                download_range = input("Download range (A for all, or enter a range separtaed by comma): ")
            first, last = self.downloadRangeValidation(novel_title, download_range, largest_chapter)
            if first == last + 1 and len(chapter_link) != 1:
                print("Light novel no change since the last download, update is not performed.")
                return
            if skip:
                acn = ""
            else:
                acn = input("Append chapter number to the filename? (Y/n): ")
            acn = self.chapterNumber(acn)
            if not os.path.isdir(f"{self.database_path}/{novel_title}"):
                os.mkdir(novel_title)
                exist = False
            else:
                exist = True
            if not exist:
                self.createIndexPage(novel_title, acn, last, writer_name, description, index)
            else:
                with open(f"{self.database_path}/{novel_title}/0. index.html", "r", encoding="utf-8") as file:
                    if 'append = True' in file.read():
                        acn_prev = True
                    else:
                        acn_prev = False
                if acn_prev is False:
                    acn = False
                if acn_prev is True and acn is False:
                    print("Detected inconsistent configuration.")
                    print("Appending chapter number to the filename is YES in old setting while you entered NO this time.")
                    acn = input("Do you want to change to YES? (Y/n):")
                    acn = self.chapterNumber(acn)
                self.createIndexPage(novel_title, acn, last, writer_name, description, index)
            print(f"Downloading {novel_title}")
            self.downloadChapterContent(novel_title, acn, chapter_link, first, last)
            self.updateIndexPage(novel_title, acn, code, first, last + 1, index)
            if exist:
                self.updateIndexPage(novel_title, acn, code, 1, first, index)
            print("\nDone.")

    def update(self):
        lib = lnlibrary.readLib()
        numberOfBook = len(lib["library"])
        if numberOfBook == 0:
            print("Your library is empty.")
        else:
            for book in lib["library"]:
                print("===== Update =====")
                print(f'Updating {book["title"]}')
                self.download(False, book["url"], True)

    def menu(self) -> None:
        print("===== Menu =====")
        print("1. Display all books in the library")
        print("2. Add book to library")
        print("3. Remove book from library")
        print("4. Download the light novel from web")
        print("5. Update the light novel in the library")
        print("0. Exit the program")
        option = input("Your option: ")
        if option == "1":
            lnlibrary.showAllBook()
            self.menu()
        elif option == "2":
            url = input("URL: ")
            web_response = self.getCode(url)
            if web_response:
                index_page = web_response[0]
                code = web_response[1]
                novel_title, writer_name, _, _, _, _ = self.getInfo(index_page, code)
                entry = [novel_title, writer_name, url]
                lnlibrary.addBook(entry)
            self.menu()
        elif option == "3":
            lnlibrary.removeBook(True, None)
            self.menu()
        elif option == "4":
            self.download(True, None, False)
            self.menu()
        elif option == "5":
            self.update()
            self.menu()
        elif option == "0":
            exit()
        else:
            print("Invalid option, please try again.")
            self.menu()

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-a', '--add',
                            metavar='<URL>',
                            type=str,
                            help='add a light novel to the library')
        parser.add_argument('-r', '--remove',
                            metavar='<book title>',
                            type=str,
                            help='remove a light novel from the library')
        parser.add_argument('-d', '--download',
                            metavar='<URL>',
                            type=str,
                            help='download the light novel from the given URL')
        parser.add_argument('-u', '--update',
                            action='store_true',
                            help='update the light novel in the library')
        parser.add_argument('-ad',
                            metavar='<URL>',
                            type=str,
                            help='add a light novel to the library and then \
                            download the light novel from the given URL')
        args = vars(parser.parse_args())
        self.database_path = lnlibrary.readLib()["path"]
        noneCount = 0
        for i in args.values():
            if i is None:
                noneCount = noneCount + 1
        if noneCount == 4 and args["update"] is False:
            self.menu()
        else:
            if args["add"] is not None:
                web_response = self.getCode(args["add"])
                if web_response:
                    index_page = web_response[0]
                    code = web_response[1]
                    novel_title, writer_name, _, _, _, _ = self.getInfo(index_page, code)
                    entry = [novel_title, writer_name, args["add"]]
                    lnlibrary.addBook(entry)
            if args["remove"] is not None:
                lnlibrary.removeBook(False, args["remove"])
            if args["download"] is not None:
                self.download(False, args["download"], True)
            if args["update"] is True:
                self.update()
            if args["ad"] is not None:
                web_response = self.getCode(args["ad"])
                if web_response:
                    index_page = web_response[0]
                    code = web_response[1]
                    novel_title, writer_name, _, _, _, _ = self.getInfo(index_page, code)
                    entry = [novel_title, writer_name, args["add"]]
                    lnlibrary.addBook(entry)
                    self.download(False, args["download"], True)


downloader = ln_downloader()
downloader.main()
