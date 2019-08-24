import sys
from PyQt5.QtWidgets import QWidget, QLineEdit,\
    QPushButton, QApplication, QMessageBox, QComboBox

from src.init_user_information import list_of_dic
import pickle
from src.store_user_information.user_info_pickle_path import user_info_pickle_path


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Register'
        self.top = 100
        self.left = 100
        self.width = 400
        self.height = 400
        self.register_interface()

    def register_interface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        self.user = QLineEdit(self)
        self.user.setPlaceholderText('User Name')
        self.user.move(100, 150)
        self.pw = QLineEdit(self)
        self.pw.setPlaceholderText('Password')
        self.pw.move(100, 200)
        self.age = QLineEdit(self)
        self.age.setPlaceholderText('Age')
        self.age.move(100, 250)
        self.combo = QComboBox(self)
        for i in range(150):
            self.combo.addItem(str(i))
        self.combo.move(200, 250)
        self.combo.activated[str].connect(self.onchanged)
        btn = QPushButton('confirm to submit', self)
        btn.move(100, 300)
        btn.clicked.connect(self.register)
        self.show()

    def onchanged(self, text):
        self.age.setText(text)
        self.age.adjustSize()

    def register(self):
        input_user = self.user.text()
        input_password = self.pw.text()
        input_age = self.age.text()
        dic1 = dict()
        dic1['user'] = input_user
        dic1['password'] = input_password
        dic1['age'] = input_age
        list_of_dic.append(dic1)
        pickle.dump(list_of_dic, open(user_info_pickle_path + "user_info.p", "wb"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RegisterWindow()
    sys.exit(app.exec_())
