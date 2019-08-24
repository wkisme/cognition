import sys
from PyQt5.QtWidgets import QWidget, QLineEdit,\
    QPushButton, QApplication, QMessageBox, QComboBox

from src.init_user_information import list_of_dic
from src.video_player_window import VideoPlayerWindow
import pickle
from src.store_user_information.user_info_pickle_path import user_info_pickle_path

list_of_dic = pickle.load(open(user_info_pickle_path + "user_info.p", "rb"))


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Login'
        self.top = 100
        self.left = 100
        self.width = 400
        self.height = 400
        self.log_interface()

    def log_interface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        self.user = QLineEdit(self)
        self.user.setPlaceholderText('User Name')
        self.user.move(100, 150)
        self.pw = QLineEdit(self)
        self.pw.setPlaceholderText('Password')
        self.pw.move(100, 200)
        self.combo = QComboBox(self)
        for i in [dic1['user'] for dic1 in list_of_dic]:
            self.combo.addItem(i)
        self.combo.move(250, 150)
        self.combo.activated[str].connect(self.onchanged)
        btn = QPushButton('Click to login', self)
        btn.move(100, 300)
        btn.clicked.connect(self.login)
        btn1 = QPushButton('Click to Register!!!', self)
        btn1.move(200, 300)
        btn1.clicked.connect(self.regeister)
        self.show()

    def onchanged(self, text):
        self.user.setText(text)
        self.user.adjustSize()

    def regeister(self):
        pass


    def login(self):
        input_user = self.user.text()
        input_password = self.pw.text()
        if input_user in [dic['user'] for dic in list_of_dic]:
            if (input_user, input_password) in [(dic['user'], dic['password']) for dic in list_of_dic]:
                # print('login successfully')
                self.SW = VideoPlayerWindow(input_user)
                self.SW.show()
            else:
                # print('wrong password')
                QMessageBox.about(self, "Login Wrong!", "wrong password!")
        else:
            # print('no exist such a user')
            QMessageBox.about(self, "Login Wrong!", "no exist such a user!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    sys.exit(app.exec_())
