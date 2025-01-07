import base64
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QCheckBox, QHeaderView, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMenu, QMessageBox, QPushButton, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

import downloader
import library_manager


class DownloaderGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Novel Station")
        self.setGeometry(200, 200, 950, 500)
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode("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"))
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

        self.library_path = library_manager.read_lib()["path"]
        self.downloader = downloader.Downloader(self.library_path)
        self.init_ui()

    def init_ui(self) -> None:
        # Create a central widget and main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Create the book list tree view on the left
        self.book_tree = QTreeWidget(self)
        self.book_tree.setHeaderLabels(["Title", "Author", "URL", "Ended"])

        # set header label width (QHeaderView.Stretch, QHeaderView.ResizeToContents, QHeaderView.Fixed)
        header = self.book_tree.header()
        header.setSectionResizeMode(0, QHeaderView.Fixed)  # Title
        header.resizeSection(0, 200)
        header.setSectionResizeMode(1, QHeaderView.Fixed)  # Author
        header.resizeSection(1, 80)
        header.setSectionResizeMode(2, QHeaderView.Fixed)  # URL
        header.resizeSection(2, 130)
        header.setSectionResizeMode(3, QHeaderView.Fixed)  # Ended
        header.resizeSection(3, 30)

        self.display_all_books()

        # Connect double-click signal to open folder function
        self.book_tree.itemDoubleClicked.connect(self.open_folder)

        # Connect right-click signal to show context menu
        self.book_tree.setContextMenuPolicy(Qt.CustomContextMenu)  # ContextMenuPolicy is set to CustomContextMenu
        self.book_tree.customContextMenuRequested.connect(self.show_context_menu)

        main_layout.addWidget(self.book_tree)

        # Create the actions panel on the right
        actions_layout = QVBoxLayout()

        # library path configuration
        path_label = QLabel("Library file path")
        path_layout = QHBoxLayout()
        path_input = QLineEdit()
        path_input.setText(self.library_path)
        path_btn = QPushButton("Change")
        path_layout.addWidget(path_input)
        path_layout.addWidget(path_btn)
        actions_layout.addWidget(path_label)
        actions_layout.addLayout(path_layout)
        path_btn.clicked.connect(library_manager.set_lib_path)

        # search function
        search_label = QLabel("Search in library")
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_btn = QPushButton("Search")
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_btn)
        actions_layout.addWidget(search_label)
        actions_layout.addLayout(search_layout)
        search_btn.clicked.connect(self.search_book)
        search_input.returnPressed.connect(self.search_book)
        search_input.textChanged.connect(self.search_book)

        # add function
        add_label = QLabel("Add a book to library")
        add_layout = QHBoxLayout()
        self.add_input = QLineEdit()
        add_btn = QPushButton("Add")
        add_layout.addWidget(self.add_input)
        add_layout.addWidget(add_btn)
        actions_layout.addWidget(add_label)
        actions_layout.addLayout(add_layout)
        add_btn.clicked.connect(self.add_book)
        self.add_input.returnPressed.connect(self.add_book)

        # download function
        download_label = QLabel("Download a book")
        download_layout = QHBoxLayout()
        self.download_input = QLineEdit()
        download_btn = QPushButton("Download")
        download_layout.addWidget(self.download_input)
        download_layout.addWidget(download_btn)
        actions_layout.addWidget(download_label)
        actions_layout.addLayout(download_layout)
        download_btn.clicked.connect(self.download_book)
        self.download_input.returnPressed.connect(self.download_book)

        # update function
        update_btn = QPushButton("Update all the books in the library")
        update_btn.setFixedHeight(50)
        update_btn.clicked.connect(self.downloader.update)
        actions_layout.addWidget(update_btn)

        actions_layout.addStretch(1)
        main_layout.addLayout(actions_layout)

    def add_book_to_treeview(self, book: dict, path: str) -> None:
        book_item = QTreeWidgetItem(self.book_tree, [book["title"], book["author"], book["url"], book["ended"]])
        book_item.setData(0, Qt.UserRole, path)  # Using setData to store folder path
        book_ended_checkbox = QCheckBox()
        if book["ended"] == "✔":
            book_ended_checkbox.setChecked(True)
        book_ended_checkbox.stateChanged.connect(self.update_book_status)
        self.book_tree.setItemWidget(book_item, 3, book_ended_checkbox)  # 3 is the column index for "Ended"

    def display_all_books(self) -> None:
        # loop through the library and add items to the tree
        lib = library_manager.read_lib()
        for book in lib["library"]:
            path = lib["path"] + "\\" + book["title"]
            self.add_book_to_treeview(book, path)

    def open_folder(self, item) -> None:
        # Get the folder path from the hidden variable
        if QApplication.mouseButtons() == Qt.LeftButton:
            folder_path = item.data(0, Qt.UserRole)
            if folder_path:
                try:
                    os.startfile(folder_path)
                except FileNotFoundError:
                    # get the title of the book
                    QMessageBox.critical(self, "Error", f"Folder {item.text(0)} not found.")

    def show_context_menu(self, position) -> None:
        # Get the item at the clicked position
        item = self.book_tree.itemAt(position)

        # Show context menu only if an item is clicked
        if item:
            # Create a context menu with a delete option
            menu = QMenu(self)
            delete_action = menu.addAction("Delete")
            action = menu.exec(self.book_tree.mapToGlobal(position))

            # If the delete option is selected, call the delete function
            if action == delete_action:
                self.delete_item()

    def delete_item(self) -> None:
        # Get the currently selected item(s)
        selected_items = self.book_tree.selectedItems()

        # Iterate over selected items and remove them
        for item in selected_items:
            library_manager.delete_book(item.text(0))
            (item.parent() or self.book_tree.invisibleRootItem()).removeChild(item)

    def update_book_status(self) -> None:
        # Retrieve the checkbox object that emitted the signal
        checkbox = self.sender()
        # get the item that the checkbox belongs to
        # item = self.book_tree.itemAt(checkbox.pos())
        # get the title of the book
        title = self.book_tree.itemAt(checkbox.pos()).text(0)
        # Retrieve the current state of the checkbox
        checkbox_state = checkbox.isChecked()

        # Perform actions based on the checkbox state
        if checkbox_state:
            library_manager.update_book_status(title, "✔")
        else:
            library_manager.update_book_status(title, "")

    def search_book(self) -> None:
        search_input = self.sender().text()
        lib = library_manager.read_lib()
        if search_input:
            for book in lib["library"]:
                # hide treeview item if the search input is not in the title or author or url
                if search_input.lower() not in book["title"].lower() and search_input.lower() not in book["author"].lower() and search_input.lower() not in book["url"].lower():
                    self.book_tree.findItems(book["title"], Qt.MatchExactly)[0].setHidden(True)
        else:
            # show back all books
            for book in lib["library"]:
                self.book_tree.findItems(book["title"], Qt.MatchExactly)[0].setHidden(False)

    def add_book(self) -> None:
        # print(self.add_input.text())
        entry = self.downloader.add_book(self.add_input.text())
        if entry:
            entry = {"title": entry[0], "author": entry[1], "url": entry[2], "ended": ""}
            path = self.library_path + "\\" + entry["title"]
            self.add_book_to_treeview(entry, path)
            self.add_input.clear()
            # ask for user to download the book
            download = QMessageBox.question(self, "Download", "Do you want to download this book now?", QMessageBox.Yes | QMessageBox.No)
            if download == QMessageBox.Yes:
                self.downloader.download(entry["url"])

    def download_book(self) -> None:
        # print(self.download_input.text())
        self.downloader.download(self.download_input.text())
        self.download_input.clear()
