import os
import requests

from typing import Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QHBoxLayout, QMessageBox, QProgressBar, QProgressDialog, QRadioButton, QSpinBox, QVBoxLayout


import novel_library
import novel_site_parser


class Downloader():
    ILLEGAL_PATH_DICT = {'/': '／', ':': '：', '?': '？', '"': '\''}
    ILLEGAL_PATH_LIST = '<>|*\\'
    browser_header = {"user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    def __init__(self, path: str):
        self.library_path = path

    def url_validation(self, url: str) -> requests.models.Response or bool:
        try:
            if "?p" in url:
                # get the main index page
                url = url.split("?p")[0]
            response = requests.get(url, headers=self.browser_header)
        except RuntimeWarning:
            return False
        else:
            if response.status_code == 200:
                return response
            else:
                return False

    def get_code(self, url: str) -> Tuple[str, str, str] or bool:
        response = self.url_validation(url)
        if response:
            url_split = url.split("/")
            if "syosetu.com" in url:
                site = "syosetu"
                if url_split[-1] == "" or "?p" in url_split[-1]:
                    code = url_split[-2]
                else:
                    code = url_split[-1]
            elif "shikoto.com" in url:
                site = "shikoto"
                code = url_split[-1].replace(".html", "")
            return response, site, code
        else:
            QMessageBox.critical(self, "Error", "The URL is invalid, please try again.")
            return False

    def add_book(self, url: str) -> list or None:
        result = self.get_code(url)
        if result:
            index_page = result[0]
            site = result[1]
            code = result[2]
            title, author, _, _, _, _, _ = self.get_info(index_page, site, code)
            entry = [title, author, url]
            novel_library.add_book(entry)
            return entry
        else:
            return None

    def get_info(self, index_page: str, site: str, code: str) -> Tuple[str, str, str, str, list, int]:
        # if site == "kakuyomu":
        #     return novel_site_parser.Kakuyomu.get_info(index_page, code)
        if site == "shikoto":
            return novel_site_parser.Shikoto.get_info(index_page)
        if site == "syosetu":
            return novel_site_parser.Syosetu.get_info(index_page)

    def update_spinbox_end_range(self, new_value):
        self.range_button.setChecked(True)
        if self.end_range_box.value() < new_value:
            self.end_range_box.setValue(new_value)

    def update_spinbox_start_range(self, new_value):
        self.range_button.setChecked(True)
        # if self.start_range_box.value() > new_value:
        #     self.start_range_box.setValue(new_value)

    def get_download_range(self, largest_chapter: int) -> Tuple[int, int, bool]:
        dialog = QDialog()
        dialog.setWindowTitle("Download Range")
        dialog.setGeometry(300, 300, 300, 100)

        vertical_layout = QVBoxLayout(dialog)
        vertical_layout.setAlignment(Qt.AlignTop)

        all_button = QRadioButton("All")
        all_button.setChecked(True)
        self.range_button = QRadioButton("Range")
        vertical_layout.addWidget(all_button)
        vertical_layout.addWidget(self.range_button)
        range_options_layout = QHBoxLayout()
        range_options_layout.addWidget(self.range_button)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(range_options_layout)
        self.start_range_box = QSpinBox()
        self.start_range_box.setMinimum(1)
        self.start_range_box.setMaximum(largest_chapter)
        self.start_range_box.valueChanged.connect(self.update_spinbox_end_range)
        self.end_range_box = QSpinBox()
        self.end_range_box.setMinimum(1)
        self.end_range_box.setMaximum(largest_chapter)
        self.end_range_box.setValue(largest_chapter)
        self.end_range_box.valueChanged.connect(self.update_spinbox_start_range)

        horizontal_layout.addWidget(self.start_range_box)
        horizontal_layout.addWidget(self.end_range_box)
        vertical_layout.addLayout(horizontal_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        vertical_layout.addWidget(button_box, alignment=Qt.AlignCenter)

        accepted = dialog.exec() == QDialog.Accepted
        first_chapter = self.start_range_box.value()
        last_chapter = self.end_range_box.value()
        if all_button.isChecked():
            first_chapter = 1
            last_chapter = largest_chapter
        return accepted, first_chapter, last_chapter

    def download_range_validation(self, title: str, title_path: str, first_chapter: int, last_chapter: int, largest_chapter: int) -> Tuple[int, int]:
        if first_chapter == 1 and last_chapter == largest_chapter:
            if not os.path.isfile(f"{self.library_path}/{title_path}/0. index.html"):
                return first_chapter, last_chapter
            else:
                first_chapter = novel_library.get_last_download(title) + 1
                last_chapter = largest_chapter
        if last_chapter < first_chapter:
            QMessageBox.critical(self, "Error", "Download range is invalid, range set to all chapters.")
            first_chapter = 1
            last_chapter = largest_chapter
        return first_chapter, last_chapter
        # if first_chapter == 1 and last_chapter == largest_chapter:
        #     if not os.path.isfile(f"{self.library_path}/{title}/0. index.html"):
        #         return first_chapter, last_chapter
        #     else:
        #         first_chapter = novel_library.getLastDownload(title) + 1
        #         last_chapter = largest_chapter
        #         return first_chapter, last_chapter
        # else:
        #     if first_chapter < 0 or last_chapter > largest_chapter:
        #         QMessageBox.critical(self, "Error", "Download range is invalid, range set to all chapters.")
        #         first_chapter = 1
        #         last_chapter = largest_chapter
        #         return first_chapter, last_chapter

    def path_validation(self, path: str) -> str or False:
        for character in Downloader.ILLEGAL_PATH_LIST:
            if character in path:
                QMessageBox.critical(self, "Error", "Detected illegal character in the path.")
                return False
        for character in Downloader.ILLEGAL_PATH_DICT.keys():
            if character in path:
                path = path.replace(character, Downloader.ILLEGAL_PATH_DICT[character])
        return path

    def create_index_page(self, site: str, title: str, title_path: str, author: str, description: str, index: str) -> None:
        # if site == "kakuyomu":
        #     pass
        if site == "shikoto":
            novel_site_parser.Shikoto.create_index_page(self.library_path, title, title_path, author, description, index)
        if site == "syosetu":
            novel_site_parser.Syosetu.create_index_page(self.library_path, title, title_path, author, description, index)

    def download_chapter_content(self, site: str, title: str, acn: bool, url: str, current_chapter: int) -> None:
        # if site == "kakuyomu":
        #     pass
        if site == "shikoto":
            novel_site_parser.Shikoto.download_chapter_content(self.library_path, title, acn, url, current_chapter)
        if site == "syosetu":
            novel_site_parser.Syosetu.download_chapter_content(self.library_path, title, acn, url, current_chapter)

    def update_index_page(self, site: str, title_path: str, acn: bool, first: int, last: int, chapter_subtitle: list) -> None:
        # if site == "kakuyomu":
        #     pass
        if site == "shikoto":
            novel_site_parser.Shikoto.update_index_page(self.library_path, title_path, acn, first, last, chapter_subtitle)
        if site == "syosetu":
            novel_site_parser.Syosetu.update_index_page(self.library_path, title_path, acn, first, last, chapter_subtitle)

    def update_download_progress(self, current_chapter, last_chapter) -> None:
        self.progress_bar.setValue(current_chapter)
        self.progress_dialog.setLabelText(f"Downloading... {current_chapter}/{last_chapter}")
        if current_chapter == last_chapter:
            self.progress_dialog.close()
        else:
            QApplication.processEvents()

    def show_download_progress(self, title: str, first_chapter: int, last_chapter: int) -> None:
        self.progress_dialog = QProgressDialog()
        self.progress_dialog.setWindowTitle(f"Downloading {title}")
        # make the window strech as window title gets longer
        self.progress_dialog.setFixedWidth(100 + len(title) * 15)
        self.progress_dialog.setLabelText("Downloading...")
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setAutoReset(True)

        self.progress_bar = QProgressBar(self.progress_dialog)
        self.progress_bar.setValue(first_chapter)
        self.progress_bar.setMaximum(last_chapter)
        self.progress_dialog.setBar(self.progress_bar)

        self.progress_dialog.show()

    def download(self, url, skip=False) -> None:
        result = self.get_code(url)
        if result:
            index_page = result[0]
            site = result[1]
            code = result[2]
            title, author, description, index, chapter_link, chapter_subtitle, largest_chapter = self.get_info(index_page, site, code)
            title_path = self.path_validation(title)

            # download range validation
            if skip:
                first_chapter, last_chapter = self.download_range_validation(title, title_path, 1, largest_chapter, largest_chapter)
            else:
                accepted, first_chapter, last_chapter = self.get_download_range(largest_chapter)
                if accepted:
                    first_chapter, last_chapter = self.download_range_validation(title_path, title_path, first_chapter, last_chapter, largest_chapter)
                else:
                    return
            if first_chapter == last_chapter + 1 and len(chapter_link) != 1:
                # print("The book does not have any changes since the last download, update is not performed.")
                return False

            # chapter number validation
            acn = novel_library.get_append_chapter_num(title)
            if acn is None:
                acn = QMessageBox.question(None, "Append Chapter Number", "Do you want to append chapter number to the filename?", QMessageBox.Yes | QMessageBox.No)
                if acn == QMessageBox.Yes:
                    acn = True
                    novel_library.change_append_chapter_num(title, True)
                else:
                    acn = False
                    novel_library.change_append_chapter_num(title, False)

            # create book folder if not exist
            downloaded_before = True
            if title_path:
                if not os.path.isdir(f"{self.library_path}/{title_path}"):
                    os.mkdir(f"{self.library_path}/{title}")
                    downloaded_before = False
            else:
                return

            # create index page
            self.create_index_page(site, title, title_path, author, description, index)

            self.show_download_progress(title, first_chapter, last_chapter)
            for i in range(first_chapter, last_chapter + 1):
                self.download_chapter_content(site, title_path, acn, chapter_link[i-1], i)
                self.update_download_progress(i, last_chapter)

            self.update_index_page(site, title_path, acn, first_chapter, last_chapter + 1, chapter_subtitle)
            if downloaded_before:
                self.update_index_page(site, title_path, acn, 1, first_chapter, chapter_subtitle)

            novel_library.update_last_download(title, last_chapter)
            if not skip:
                QMessageBox.information(None, "Download", f"Succesfully downloaded {title}.")

    def update(self):
        lib = novel_library.read_lib()
        total_book = len(lib["library"])
        if total_book == 0:
            QMessageBox.information(None, "Update", "Your library is empty.")
        else:
            for book in lib["library"]:
                if book["ended"] == "":
                    self.download(book["url"], True)
