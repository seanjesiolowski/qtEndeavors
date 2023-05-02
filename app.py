from PySide6.QtWidgets import QMainWindow, QLineEdit, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QFrame, QLabel, QPushButton,  QStackedWidget, QTextEdit, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from collection import Collection
from fonts import heading_font


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.my_collection = Collection()
        self.current_index = None

        self.close_ok = False

        #  ------------------------------ Menu Bar ------------------------------
        self.menu_bar = self.menuBar()

        #  ------------------------------ File Menu ------------------------------
        file_menu = self.menu_bar.addMenu('File')
        reset_action = file_menu.addAction('Home')
        reset_action.triggered.connect(self.reset_home)
        save_action = file_menu.addAction('Save to db')
        save_action.triggered.connect(self.save_to_db)
        quit_action = file_menu.addAction('Quit program')
        quit_action.triggered.connect(self.quit_app)

        #  ------------------------------ Endeavors Menu ------------------------------
        self.endeavors_menu = self.menu_bar.addMenu('Endeavors')
        self.update_endeavors_index()

        #  ------------------------------ Tools Menu ------------------------------
        self.tools_menu = self.menu_bar.addMenu('Tools')
        save_action = self.tools_menu.addAction('Save details')
        save_action.triggered.connect(self.save_details)
        delete_action = self.tools_menu.addAction('Delete endeavor')
        delete_action.triggered.connect(self.delete_endeavor)

        #  ------------------------------ Stacked Widget ------------------------------
        self.my_stacked = QStackedWidget()
        self.setCentralWidget(self.my_stacked)

        #  ------------------------------ Home Frame ------------------------------
        self.home_frame = QFrame()
        self.home_layout = QVBoxLayout()
        self.home_frame.setLayout(self.home_layout)
        self.my_stacked.addWidget(self.home_frame)

        self.label_frame = QFrame()
        self.home_layout.addWidget(self.label_frame)
        self.label_layout = QHBoxLayout()
        self.label_frame.setLayout(self.label_layout)
        self.my_label = QLabel('big idea:')
        self.my_label.setAlignment(Qt.AlignCenter)
        self.my_label.setFont(heading_font())
        self.label_layout.addWidget(self.my_label)

        self.input_frame = QFrame()
        self.home_layout.addWidget(self.input_frame)
        self.input_layout = QHBoxLayout()
        self.input_frame.setLayout(self.input_layout)
        self.my_input = QLineEdit()
        self.input_layout.addWidget(self.my_input)

        self.button_frame = QFrame()
        self.home_layout.addWidget(self.button_frame)
        self.button_layout = QHBoxLayout()
        self.button_frame.setLayout(self.button_layout)
        self.my_button = QPushButton('Submit')
        self.my_button.setFixedWidth(100)
        self.button_layout.addWidget(self.my_button)
        self.my_button.clicked.connect(self.take_input)

        #  ------------------------------ Endeavor Frame ------------------------------
        self.endeavor_frame = QFrame()
        self.endeavor_layout = QVBoxLayout()
        self.endeavor_frame.setLayout(self.endeavor_layout)
        self.my_stacked.addWidget(self.endeavor_frame)

        self.title_frame = QFrame()
        self.endeavor_layout.addWidget(self.title_frame)
        self.title_layout = QHBoxLayout()
        self.title_frame.setLayout(self.title_layout)
        self.title_label = QLabel('')
        self.title_label.setFont(heading_font())
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_layout.addWidget(self.title_label)

        self.text_frame = QFrame()
        self.endeavor_layout.addWidget(self.text_frame)
        self.text_layout = QHBoxLayout()
        self.text_frame.setLayout(self.text_layout)
        self.text_edit = QTextEdit()
        self.text_edit.setAlignment(Qt.AlignCenter)
        self.text_layout.addWidget(self.text_edit)

    #  ------------------------------ Event Methods ------------------------------
    def closeEvent(self, event: QCloseEvent):
        if self.close_ok:
            pass
        else:
            event.ignore()
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Every Good Endeavor")
            dlg.setFixedSize(300, 150)
            dlg.setText("Save to the database?")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            clicked_btn = dlg.exec_()
            if clicked_btn == QMessageBox.Yes:
                self.save_to_db()
            self.close_ok = True
            self.app.quit()

    #  ------------------------------ File Actions ------------------------------
    def reset_home(self):
        self.my_stacked.setCurrentIndex(0)
        self.my_input.clear()
        self.current_index = None

    def save_to_db(self):
        self.my_collection.data_to_db()

    def quit_app(self):
        self.app.quit()

    #  ------------------------------ Endeavor Actions ------------------------------
    def open_endeavor(self):
        chosen_index = self.endeavors_menu.actions().index(self.sender())
        the_endeavor = self.my_collection.read_endeavor(chosen_index)
        self.my_stacked.setCurrentIndex(1)
        self.title_label.setText(the_endeavor.big_idea)
        self.text_edit.setText(the_endeavor.details)
        self.current_index = chosen_index

    def save_details(self):
        the_details = self.text_edit.toPlainText()
        self.my_collection.update_endeavor(self.current_index, the_details)
        self.update_endeavors_index()
        self.reset_home()

    def delete_endeavor(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("QDialog")
        dlg.setFixedSize(300, 150)
        dlg.setText("Are you sure?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        clicked_btn = dlg.exec_()
        if clicked_btn == QMessageBox.Yes:
            self.my_collection.delete_endeavor(self.current_index)
            self.update_endeavors_index()
            self.reset_home()

    #  ------------------------------ Additional Methods ------------------------------
    def take_input(self):
        self.my_collection.create_endeavor(self.my_input.text())
        self.update_endeavors_index()
        self.reset_home()

    def update_endeavors_index(self):
        self.endeavors_menu.clear()
        for index, item in enumerate(self.my_collection.collection):
            selection = self.endeavors_menu.addAction(item.big_idea)
            selection.triggered.connect(self.open_endeavor)
            item.index = index
