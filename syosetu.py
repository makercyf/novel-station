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
    css = '''<style>
#novel_ex { margin: 20px auto 50px; line-height: 180%; overflow: hidden; text-align: left; font-size:17px; }
div.chapter_title {font-size: 110%; padding: 30px 0 0 0; font-weight:bold;}
div.index_box { font-size: 17px;}
dl.novel_sublist2 {overflow: hidden; border-bottom:1px solid #ffffff;}
dl.novel_sublist2 dd{padding: 10px 10px 2px 5px; width: 515px; font-size: 17px; float:left;}</style>\n'''
    novel_title = website.title.string
    writer_name = str(website.find_all("div", class_="novel_writername")[0]).split(">")[2].split("<")[0]
    description = str(website.find(id="novel_ex"))
    index = str(website.find_all("div", class_="index_box")[0])
    ###
    chapter_link = []
    toc = website.find_all("a")
    for chapter in toc:
        link = chapter.get("href")
        match = re.search(code + '/{1,}[0-9]', link)
        if match:
            full_chapter_link = "https://ncode.syosetu.com" + link
            chapter_link.append(full_chapter_link)
    largest_chapter = len(chapter_link)
    ###
    download_range = input("\nDownload range (A for all, or enter a range separtaed by comma): ")
    download_range = download_range.split(",")
    if len(download_range) == 2:
        if download_range[0].isnumeric and download_range[1].isnumeric:
            first, last = download_range[0].strip(), download_range[1].strip()
            first, last = int(first), int (last)
            if first < 0 or last > largest_chapter:
                print("Download range is invalid, range set to all chapter")
                first, last = 1, largest_chapter
        else:
            print("Download range is invalid, range set to all chapter")
            first, last = 1, largest_chapter
    else:
        first, last = 1, largest_chapter
    ###
    cn = input("Append chapter number to the file? (Y/n): ")
    if cn == "N" or cn == "n":
        cn = False
    else:
        cn = True
    ###
    if not os.path.isdir(f'./{novel_title}'):
        os.mkdir(novel_title)
    with open(f"./{novel_title}/0. index.html", "w", encoding="utf-8") as f:
        f.write(css)
        f.write(f'<h1 style="text-align: center;">{novel_title}</h1>\n')
        f.write(f'<h2 style="text-align: center;">作者：{writer_name}</h2>\n')
        f.write(description)
        f.write(index)
    print(f"\nDownloading {novel_title}")
    for i in range(first, last + 1):
        website = requests.get(chapter_link[i-1], headers={"user-agent": 'Mozilla/5.0'}).text
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
        with open(f"./{novel_title}/{filename}.html", "w", encoding="utf-8") as f:
            f.write(f'<h1 style="text-align: center;">{subtitle}</h1>\n')
            for line in content:
                match = re.search('id="L[0-9]{1,}', str(line))
                if match:
                    f.write(str(line) + "\n")
        with open(f"./{novel_title}/0. index.html", "r+", encoding="utf-8") as f:
            new = f.read().replace(f'"/{code}/{i}/"', f'"./{filename}.html" target="_blank"')
            f.seek(0)
            f.write(new)
        print(f"Progress: {i}/{last}", end="\r")
    print("\nDone")
else:
    print("Your URL is invalid, please try again.")
