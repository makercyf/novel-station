import json
import os

from PySide6.QtWidgets import QFileDialog, QMessageBox


def write_lib(lib: dict) -> None:
    with open("./library.json", "w", encoding="utf-8") as file:
        lib = json.dumps(lib, indent=4, ensure_ascii=False)
        file.write(lib)


def create_lib(path: str) -> None:
    lib = {}
    lib["path"] = path
    lib["library"] = []
    write_lib(lib)


def lib_exist() -> bool:
    if not os.path.isfile("./library.json"):
        return False
    else:
        return True


def read_lib() -> dict:
    if not lib_exist():
        QMessageBox.critical(None, "Error", "Library does not exist. Please create one first.")
        path = QFileDialog.getExistingDirectory()
        if path:
            create_lib(path)
    with open("./library.json", "r", encoding="utf-8") as file:
        lib = json.loads(file.read())
    return lib


def get_last_download(title: str) -> int:
    lib = read_lib()
    for book in lib["library"]:
        if book["title"] == title:
            return book["lastDownload"]
    return 0


def update_last_download(title: str, last_download: int) -> None:
    lib = read_lib()
    for book in lib["library"]:
        if book["title"] == title:
            book["lastDownload"] = last_download
            write_lib(lib)
            break


def get_append_chapter_num(title: str) -> bool or None:
    lib = read_lib()
    for book in lib["library"]:
        if book["title"] == title:
            return book["appendChapterNum"]
    return None


def change_append_chapter_num(title: str, state: bool) -> None:
    lib = read_lib()
    for book in lib["library"]:
        if book["title"] == title:
            book["appendChapterNum"] = state
            write_lib(lib)
            break


def set_lib_path() -> None:
    path = QFileDialog.getExistingDirectory()
    if path:
        lib = read_lib()
        lib["path"] = path
        write_lib(lib)


def book_exist(lib: dict, title: str) -> bool:
    for book in lib["library"]:
        if book["title"] == title:
            return True
    return False


def add_book(data: list) -> None:
    lib = read_lib()
    if book_exist(lib, data[0]):
        QMessageBox.critical(None, "Error", "This book already in to the library.")
    else:
        entry = {"title": data[0], "author": data[1], "url": data[2], "ended": "", "lastDownload": 0, "appendChapterNum": None}
        lib["library"].append(entry)
        write_lib(lib)
        QMessageBox.information(None, "Success", f"Successfully added {data[0]} to library.")


def delete_book(title: str) -> None:
    lib = read_lib()
    for num, book in enumerate(lib["library"]):
        if book["title"] == title:
            del lib["library"][num]
            write_lib(lib)
            QMessageBox.information(None, "Success", f"Successfully deleted {title} from library. Please note that the downloaded content are not deleted.")
            break


def update_book_status(title, state) -> None:
    lib = read_lib()
    for book in lib["library"]:
        if book["title"] == title:
            book["ended"] = state
            write_lib(lib)
            break
