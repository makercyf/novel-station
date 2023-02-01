import json
import os
from typing import Union


def writeLib(lib: dict) -> None:
    with open("./library.json", "w", encoding="utf-8") as file:
        lib = json.dumps(lib, indent=4)
        file.write(lib)


def createLib() -> None:
    path = input("Please enter a path for the library: ")
    lib = {}
    lib["path"] = path
    lib["library"] = []
    writeLib(lib)


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
        entry = {"title": data[0], "writer": data[1], "url": data[2], "ended": "false"}
        lib["library"].append(entry)
        writeLib(lib)
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
                    writeLib(lib)
                    print("Done, removed all books.")
                else:
                    if not bookid.isnumeric():
                        print("Invalid input, please try again.")
                    else:
                        bookid = int(bookid)
                        if bookid < 1 or bookid > numberOfBook:
                            print("Invalid input, please try again.")
                        else:
                            title = lib["library"][bookid-1]["title"]
                            del lib["library"][bookid-1]
                            writeLib(lib)
                            print(f"Done, removed {title}.")
        else:
            if novel_title == '*':
                lib["library"].clear()
                writeLib(lib)
                print("Done, removed all books.")
            elif lnExist(lib, novel_title):
                for book, num in zip(lib["library"], range(len(lib["library"]))):
                    if book["title"] == novel_title:
                        del lib["library"][int(num)]
                        writeLib(lib)
                        print(f"Done, removed {novel_title}.")
            else:
                print("This book is not in your library.")


def markBook(interactive: bool, novel_title: Union[str, None]) -> None:
    lib = readLib()
    numberOfBook = len(lib["library"])
    if numberOfBook == 0:
        print("Your library is empty.")
    else:
        if interactive:
            print("===== Library =====")
            for book, num in zip(lib["library"], range(len(lib["library"]))):
                if lib["library"][num]["ended"] != "true":
                    print(f'{num+1}. {book["title"]}')
            print("===== Library =====")
            print("Enter a number, or 'c' for cancel, or '*' for all books.")
            bookid = input("Book: ")
            if bookid == 'c':
                pass
            else:
                if bookid == '*':
                    for entry in lib["library"]:
                        entry["ended"] = "true"
                    writeLib(lib)
                    print("Done, marked all books as ended.")
                else:
                    if not bookid.isnumeric():
                        print("Invalid input, please try again.")
                    else:
                        bookid = int(bookid)
                        if bookid < 1 or bookid > numberOfBook:
                            print("Invalid input, please try again.")
                        else:
                            title = lib["library"][bookid-1]["title"]
                            lib["library"][bookid-1]["ended"] = "true"
                            writeLib(lib)
                            print(f"Done, marked {title} as ended.")
        else:
            if novel_title == '*':
                for entry in lib["library"]:
                    entry["ended"] = "true"
                writeLib(lib)
                print("Done, marked all books as ended.")
            elif lnExist(lib, novel_title):
                for book, num in zip(lib["library"], range(len(lib["library"]))):
                    if book["title"] == novel_title:
                        lib["library"][int(num)]["ended"] = "true"
                        writeLib(lib)
                        print(f"Done, marked {title} as ended.")
            else:
                print("This book is not in your library.")
