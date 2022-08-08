import json
import os
from typing import Union


def createLib() -> None:
    path = input("Please input the light novel library path: ")
    lib = {}
    lib["path"] = path
    lib["library"] = []
    with open("./library.json", "w", encoding="utf-8") as file:
        lib = json.dumps(lib, indent=4)
        file.write(lib)


def libExist() -> bool:
    if not os.path.isfile("./library.json"):
        return False
    else:
        return True


def readLib() -> dict:
    if not libExist():
        print("Library does not exist. Please create one first.")
        createLib()
    with open("./library.json", "r", encoding="utf-8") as file:
        lib = json.loads(file.read())
    return lib


def showAllBook() -> None:
    lib = readLib()
    print("===== Library =====")
    for book, num in zip(lib["library"], range(len(lib["library"]))):
        print(f'{num+1}. {book["title"]}')
    print("===== Library =====")


def lnExist(lib: dict, title: str) -> bool:
    for book in lib["library"]:
        if book["title"] == title:
            return True
    return False


def addBook(data: list) -> None:
    lib = readLib()
    if lnExist(lib, data[0]):
        print("This book already in to the library.")
    else:
        entry = {"title": data[0], "writer": data[1], "url": data[2]}
        lib["library"].append(entry)
        with open("./library.json", "w", encoding="utf-8") as file:
            lib = json.dumps(lib, indent=4)
            file.write(lib)
        print(f"Successfully added {data[0]} to library.")


def removeBook(interactive: bool, novel_title: Union[str, None]) -> None:
    lib = readLib()
    numberOfBook = len(lib["library"])
    if numberOfBook == 0:
        print("Your library is empty.")
    else:
        if interactive:
            showAllBook()
            print("Enter a number, or 'c' for cancel, or '*' for all books.")
            bookid = input("Book: ")
            if bookid == 'c':
                pass
            else:
                if bookid == '*':
                    lib["library"].clear()
                    with open("./library.json", "w", encoding="utf-8") as file:
                        lib = json.dumps(lib, indent=4)
                        file.write(lib)
                    print("Done, removed all books.")
                else:
                    if not bookid.isnumeric():
                        print("Invalid input, please try again.")
                    else:
                        bookid = int(bookid)
                        if bookid < 1 or bookid > numberOfBook:
                            print("Invalid input, please try again.")
                        else:
                            title = lib["library"][int(bookid)-1]["title"]
                            del lib["library"][int(bookid)-1]
                            with open("./library.json", "w", encoding="utf-8") as file:
                                lib = json.dumps(lib, indent=4)
                                file.write(lib)
                            print(f"Done, removed {title}.")
        else:
            if novel_title == '*':
                lib["library"].clear()
                with open("./library.json", "w", encoding="utf-8") as file:
                    lib = json.dumps(lib, indent=4)
                    file.write(lib)
                print("Done, removed all books.")
            elif lnExist(lib, novel_title):
                for book, num in zip(lib["library"], range(len(lib["library"]))):
                    if book["title"] == novel_title:
                        del lib["library"][int(num)]
                        with open("./library.json", "w", encoding="utf-8") as file:
                            lib = json.dumps(lib, indent=4)
                            file.write(lib)
                        print(f"Done, removed {novel_title}.")
            else:
                print("This book is not in your library.")
