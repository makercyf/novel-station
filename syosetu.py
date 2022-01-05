import requests
import re
import os
from bs4 import BeautifulSoup

url = input("URL: ")
r = requests.get(url, headers={"user-agent": 'Mozilla/5.0'})

if r.status_code == 200:
    ###
    code = url.split("/")
    if code[-1] == "":
        code = code[-2]
    else:
        code = code[-1]
    ###
    website = BeautifulSoup(r.text, 'html.parser')
    NovelTitle = website.title.string
    ###
    ChapterLinkList = []
    toc = website.find_all("a")
    for chapter in toc:
        link = chapter.get("href")
        match = re.search(code + '/{1,}[0-9]', link)
        if match:
            ChapterLink = "https://ncode.syosetu.com" + link
            ChapterLinkList.append(ChapterLink)
    LargestChapter = len(ChapterLinkList)
    ###
    DownloadRange = input("\nDownload range (A for all, or enter a range separtaed by comma): ")
    DownloadRange = DownloadRange.split(",")
    if len(DownloadRange) == 2:
        if DownloadRange[0].isnumeric and DownloadRange[1].isnumeric:
            first, last = DownloadRange[0].strip(), DownloadRange[1].strip()
            first, last = int(first), int (last)
            if first < 0 or last > LargestChapter:
                print("Download range is invalid, range set to all chapter")
                first, last = 1, LargestChapter
        else:
            print("Download range is invalid, range set to all chapter")
            first, last = 1, LargestChapter
    else:
        first, last = 1, LargestChapter
    ###
    cn = input("Append chapter number to the file? (Y/n): ")
    if cn == "N" or cn == "n":
        cn = False
    else:
        cn = True
    ###
    if not os.path.isdir(f'./{NovelTitle}'):
        os.mkdir(NovelTitle)
    print(f"\nDownloading {NovelTitle}")
    for i in range(first, last + 1):
        website = requests.get(ChapterLinkList[i-1], headers={"user-agent": 'Mozilla/5.0'}).text
        website = BeautifulSoup(website, 'html.parser')
        subtitle = website.find_all("p", class_="novel_subtitle")[0].string
        content = website.find_all("p")
        if cn:
            filename = f"{i}. {subtitle}"
        else:
            filename = subtitle
        IllgealPathDict = {'/':'／', ':':'：', '?':'？', '"':'\''}
        IllgealPathList = '<>|*\\'
        for a in IllgealPathDict.keys():
            if a in filename:
                filename = filename.replace(a, IllgealPathDict[a])
        for b in IllgealPathList:
            if b in filename:
                print("Illgeal name detected, progran exit")
                exit()
        with open(f"./{NovelTitle}/{filename}.html", "w", encoding="utf-8") as f:
            f.write(f'<h1 style="text-align: center;">{subtitle}</h1>\n')
            for line in content:
                match = re.search('id="L[0-9]{1,}', str(line))
                if match:
                    f.write(str(line) + "\n")
        print(f"Progress: {i}/{last}", end="\r")
    print("\nDone")
else:
    print("Your URL is invalid, please try again.")
