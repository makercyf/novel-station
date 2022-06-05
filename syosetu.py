import requests
import re
import os
from bs4 import BeautifulSoup

CSS = '''<style>
#novel_ex { margin: 20px auto 50px; line-height: 180%; overflow: hidden; text-align: left; font-size:17px; }
div.chapter_title {font-size: 110%; padding: 30px 0 0 0; font-weight:bold;}
div.index_box { font-size: 17px;}
dl.novel_sublist2 {overflow: hidden; border-bottom:1px solid #ffffff;}
dl.novel_sublist2 dd{padding: 10px 10px 2px 5px; width: 515px; font-size: 17px; float:left;}
</style>\n'''

ILLEGAL_PATH_DICT = {'/': '／', ':': '：', '?': '？', '"': '\''}
ILLEGAL_PATH_LIST = '<>|*\\'


def urlValidation(url):
    try:
        r = requests.get(url, headers={"user-agent": 'Mozilla/5.0'})
    except:
        return False
    else:
        if r.status_code == 200:
            return r
        else:
            return False


def getCode(url):
    url_split = url.split("/")
    if url_split[-1] == "":
        code = url_split[-2]
    else:
        code = url_split[-1]
    return code


def getInfo(r, code):
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


def downloadRangeValidation(novel_title, download_range, largest_chapter):
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
        if not os.path.isfile(f"./{novel_title}/0. index.html"):
            first = 1
            last = largest_chapter
        else:
            with open(f"./{novel_title}/0. index.html", "r", encoding="utf-8") as file:
                for line in file:
                    if 'last =' in line:
                        first = int(re.sub('[^0-9]', '', line))
                        last = largest_chapter
                        break
    return first, last


def chapterNumber(acn):
    if acn == "N" or acn == "n":
        acn = False
    else:
        acn = True
    return acn


def filenameValidation(filename):
    for character in ILLEGAL_PATH_LIST:
        if character in filename:
            print("Illgeal character in the filename Detected, program exit.")
            exit()
    for character in ILLEGAL_PATH_DICT.keys():
        if character in filename:
            filename = filename.replace(character, ILLEGAL_PATH_DICT[character])
    return filename


def createIndexPage(novel_title, acn, last, writer_name, description, index):
    with open(f"./{novel_title}/0. index.html", "w", encoding="utf-8") as file:
        # Write must be str/NavigableString, not Tag
        file.write(f'<title>{novel_title}</title>\n')
        file.write(CSS)
        file.write(f'<!-- append = {acn} -->\n')
        file.write(f'<!-- last = {last} -->\n')
        file.write(f'<h1 style="text-align: center;">{novel_title}</h1>\n')
        file.write(f'<h2 style="text-align: center;">作者：{writer_name}</h2>\n')
        file.write(str(description))
        file.write(str(index))


def updateIndexPage(novel_title, acn, code, first, last, index):
    subtitle_list = index.find_all("a")
    with open(f"./{novel_title}/0. index.html", "r+", encoding="utf-8") as file:
        content = file.read()
        for i in range(first, last):
            if acn:
                filename = f"{i}. {subtitle_list[i-1].string}"
            else:
                filename = subtitle_list[i-1].string
            filename = filenameValidation(filename)
            content = content.replace(f'"/{code}/{i}/"', f'"./{filename}.html" target="_blank"')
        file.seek(0)
        file.write(content)


def downloadChapterContent(novel_title, acn, chapter_link, first, last):
    for i in range(first, last + 1):
        website = requests.get(chapter_link[i-1], headers={"user-agent": 'Mozilla/5.0'}).text
        website = BeautifulSoup(website, 'html.parser')
        subtitle = website.find_all("p", class_="novel_subtitle")[0].string
        content = website.find_all("p")
        if acn:
            filename = f"{i}. {subtitle}"
        else:
            filename = subtitle
        filename = filenameValidation(filename)
        if filename:
            with open(f"./{novel_title}/{filename}.html", "w", encoding="utf-8") as file:
                file.write(f'<h1 style="text-align: center;">{subtitle}</h1>\n')
                for line in content:
                    line = str(line)
                    match = re.search('id="L[0-9]{1,}', line)
                    if match:
                        file.write(line + "\n")
            print(f"Progress: {i}/{last}", end="\r")


def main():
    url = input("URL: ")
    r = urlValidation(url)
    if r:
        code = getCode(url)
        novel_title, writer_name, description, index, chapter_link, largest_chapter = getInfo(r, code)
        download_range = input("\nDownload range (A for all, or enter a range separtaed by comma): ")
        first, last = downloadRangeValidation(novel_title, download_range, largest_chapter)
        if first == last and len(chapter_link) != 1:
            print("You alrady downloaded the lastest chapter, program exit")
            exit()
        acn = input("Append chapter number to the filename? (Y/n): ")
        acn = chapterNumber(acn)
        if not os.path.isdir(f"./{novel_title}"):
            os.mkdir(novel_title)
            exist = False
        else:
            exist = True
        if not exist:
            createIndexPage(novel_title, acn, last, writer_name, description, index)
        else:
            with open(f"./{novel_title}/0. index.html", "r", encoding="utf-8") as file:
                if 'append = True' in file.read():
                    acn_prev = True
                else:
                    acn_prev = False
            if acn_prev == True and acn == False:
                print("\nDetected inconsistent configuration.")
                print("Appending chapter number to the filename is YES in old setting while you entered NO this time.")
                acn = input("Do you want to change to YES? (Y/n):")
                acn = chapterNumber(acn)
            createIndexPage(novel_title, acn, last, writer_name, description, index)
        print(f"\nDownloading {novel_title}")
        downloadChapterContent(novel_title, acn, chapter_link, first, last)
        updateIndexPage(novel_title, acn, code, first, last + 1, index)
        if exist:
            updateIndexPage(novel_title, acn, code, 1, first, index)
        print("\nDone.")
    else:
        print("Your URL is invalid, please try again.")


main()
