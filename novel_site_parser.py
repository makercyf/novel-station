import re
import requests

from typing import Tuple

from bs4 import BeautifulSoup


class Site():
    ILLEGAL_PATH_DICT = {'/': '／', ':': '：', '?': '？', '"': '\''}
    ILLEGAL_PATH_LIST = '<>|*\\'
    browser_header = {"user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    @classmethod
    def path_validation(cls, path: str) -> str or False:
        for character in cls.ILLEGAL_PATH_LIST:
            if character in path:
                return False
        for character in cls.ILLEGAL_PATH_DICT.keys():
            if character in path:
                path = path.replace(character, cls.ILLEGAL_PATH_DICT[character])
        return path


class Shikoto(Site):
    CSS = '''        <style>
        .chapter-list { margin: 20px auto 50px; line-height: 180%; overflow: hidden; font-size:17px; }
        </style>\n'''

    @classmethod
    def get_info(cls, response):
        website = BeautifulSoup(response.text, 'html.parser')
        title = website.find("h1").string
        author = website.find('meta', {'name': 'author'}).get('content')
        description = website.find('meta', {'name': 'description'}).get('content').replace("\n", "")
        index = website.find_all("ul", class_="list-inline chapter-list inline")[0]
        chapter_link = []
        chapter_subtitle = []
        table_of_content = index.find_all("a")
        for link in table_of_content:
            full_chapter_link = "https://www.shikoto.com" + link.get("href")
            chapter_link.append(full_chapter_link)
            chapter_subtitle.append(link.string)
            link["href"] = full_chapter_link
            link["target"] = "_blank"
        largest_chapter = len(chapter_link)
        return title, author, description, str(index), chapter_link, chapter_subtitle, largest_chapter

    @classmethod
    def create_index_page(cls, library_path: str, title: str, title_path: str, author: str, description: str, index: str) -> None:
        with open(f"{library_path}/{title_path}/0. index.html", "w", encoding="utf-8") as file:
            # Write must be str/NavigableString, not Tag
            file.write(f'<title>{title}</title>\n')
            file.write(Shikoto.CSS)
            file.write(f'<h1 style="text-align: center;">{title}</h1>\n')
            file.write(f'<h2 style="text-align: center;">作者：{author}</h2>\n')
            file.write(description)
            file.write(index)

    @classmethod
    def update_index_page(cls, library_path: str, title_path: str, acn: bool, first_chapter: int, last_chapter: int, chapter_subtitle: list) -> None:
        with open(f"{library_path}/{title_path}/0. index.html", "r", encoding="utf-8") as file:
            content = file.read()
        with open(f"{library_path}/{title_path}/0. index.html", "w", encoding="utf-8") as file:
            website = BeautifulSoup(content, 'html.parser')
            index = website.find_all("ul", class_="list-inline chapter-list inline")[0]
            table_of_content = index.find_all("a")
            for i in range(first_chapter, last_chapter):
                if acn:
                    filename = f"{i}. {chapter_subtitle[i-1]}"
                else:
                    filename = chapter_subtitle[i-1]
                filename = cls.path_validation(filename)
                if filename:
                    table_of_content[i-1]["href"] = f"./{filename}.html"
            file.write(str(website))

    @classmethod
    def download_chapter_content(cls, library_path: str, title_path: str, acn: bool, url: str, current_chapter: int) -> None:
        response = requests.get(url, headers=cls.browser_header).text
        website = BeautifulSoup(response, 'html.parser')
        subtitle = re.sub(r".*?: ", "", website.find("h1").string)
        content = website.find_all("div", class_="chapter-content-wrapper")[0]
        content = content.find("div")
        if acn:
            filename = f"{current_chapter}. {subtitle}"
        else:
            filename = subtitle
        filename = cls.path_validation(filename)
        if filename:
            with open(f"{library_path}/{title_path}/{filename}.html", "w", encoding="utf-8") as file:
                file.write(f'<h1 style="text-align: center;">{subtitle}</h1>\n')
                for line in content:
                    file.write(str(line))


class Syosetu(Site):
    CSS = '''        <style>
        #novel_ex { margin: 20px auto 50px; line-height: 180%; overflow: hidden; text-align: left; font-size:17px; }
        div.chapter_title {font-size: 110%; padding: 30px 0 0 0; font-weight:bold;}
        div.index_box { font-size: 17px;}
        dl.novel_sublist2 {overflow: hidden; border-bottom:1px solid #ffffff;}
        dl.novel_sublist2 dd{padding: 10px 10px 2px 5px; width: 515px; font-size: 17px; float:left;}
        </style>\n'''

    @classmethod
    def get_info(cls, response: requests.models.Response) -> Tuple[str, str, str, str, list, list, int]:
        website = BeautifulSoup(response.text, 'html.parser')
        title = website.title.string
        author = website.find_all("div", class_="novel_writername")[0].find("a").string
        description = website.find(id="novel_ex")
        index = website.find_all("div", class_="index_box")[0]
        chapter_link = []
        chapter_subtitle = []
        table_of_content = index.find_all("a")
        for link in table_of_content:
            full_chapter_link = "https://ncode.syosetu.com" + link.get("href")
            chapter_link.append(full_chapter_link)
            chapter_subtitle.append(link.string)
            link["href"] = full_chapter_link
            link["target"] = "_blank"
        largest_chapter = len(chapter_link)
        return title, author, str(description), str(index), chapter_link, chapter_subtitle, largest_chapter

    @classmethod
    def create_index_page(cls, library_path: str, title: str, title_path: str, author: str, description: str, index: str) -> None:
        with open(f"{library_path}/{title_path}/0. index.html", "w", encoding="utf-8") as file:
            # Write must be str/NavigableString, not Tag
            file.write(f'<title>{title}</title>\n')
            file.write(Syosetu.CSS)
            file.write(f'<h1 style="text-align: center;">{title}</h1>\n')
            file.write(f'<h2 style="text-align: center;">作者：{author}</h2>\n')
            file.write(description)
            file.write(index)

    @classmethod
    def update_index_page(cls, library_path: str, title_path: str, acn: bool, first_chapter: int, last_chapter: int, chapter_subtitle: list) -> None:
        with open(f"{library_path}/{title_path}/0. index.html", "r", encoding="utf-8") as file:
            content = file.read()
        with open(f"{library_path}/{title_path}/0. index.html", "w", encoding="utf-8") as file:
            website = BeautifulSoup(content, 'html.parser')
            index = website.find_all("div", class_="index_box")[0]
            table_of_content = index.find_all("a")
            for i in range(first_chapter, last_chapter):
                if acn:
                    filename = f"{i}. {chapter_subtitle[i-1]}"
                else:
                    filename = chapter_subtitle[i-1]
                filename = cls.path_validation(filename)
                if filename:
                    table_of_content[i-1]["href"] = f"./{filename}.html"
            file.write(str(website))

    @classmethod
    def download_chapter_content(cls, library_path: str, title_path: str, acn: bool, url: str, current_chapter: int) -> None:
        response = requests.get(url, headers=cls.browser_header).text
        website = BeautifulSoup(response, 'html.parser')
        subtitle = website.find_all("p", class_="novel_subtitle")[0].string
        content = website.find_all("div", id="novel_honbun")[0]
        if acn:
            filename = f"{current_chapter}. {subtitle}"
        else:
            filename = subtitle
        filename = cls.path_validation(filename)
        if filename:
            with open(f"{library_path}/{title_path}/{filename}.html", "w", encoding="utf-8") as file:
                file.write(f'<h1 style="text-align: center;">{subtitle}</h1>\n')
                for line in content:
                    file.write(str(line))
