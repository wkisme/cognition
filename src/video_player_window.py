from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog,\
    QApplication, QPushButton, QStyle, QWidget, QHBoxLayout, \
    QVBoxLayout, QSlider
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtCore import QDir, QUrl, Qt
from PyQt5.QtMultimedia import QMediaContent
import sys
import pickle
from collections import Iterable
from src.result_store.pickle_path import pickle_file_path
import datetime
result_list1 = list()


def isiterable(p_object):
    try:
        it = iter(p_object)
    except TypeError:
        return False
    return True


class VideoPlayerWindow(QMainWindow):
    def __init__(self, input_user):
        super().__init__()
        self.title = input_user + '\'s Work Window'
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 400
        global result_list1
        result_list1 = list()
        result_list1.append(('user', input_user))
        self.second_window_interface()

    def second_window_interface(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.save_result_Button = QPushButton('save result')
        self.save_result_Button.clicked.connect(self.save_result)


        self.positionSlider = QSlider(Qt.Horizontal)

        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)

        # Create menu bar and add action
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')

        new_action = QAction('&Open a video', self)
        new_action.triggered.connect(self.open_file)

        # fileMenu.addAction(newAction)
        file_menu.addAction(new_action)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.save_result_Button)

        layout = QVBoxLayout()
        videoWidget = QVideoWidget()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)

        # Set widget to contain window contents
        wid.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

        self.show()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                                                  QDir.homePath())

        if filename != '':
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filename)))
            self.playButton.setEnabled(True)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            print(self.mediaPlayer.position())
            result_list1.append(self.mediaPlayer.position())

        else:
            self.mediaPlayer.play()

    def save_result(self):
        # print('list: ', result_list1)

        print(result_list1)
        pickle.dump(result_list1, open(pickle_file_path + str(result_list1[0][1]) + ".p", "wb"))



    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        # print(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        # print(duration/10**3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SecondWindow()
    sys.exit(app.exec_())


