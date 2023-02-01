import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from map import Ui_MainWindow

SCREEN_SIZE = [600, 450]


class StaticMap(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()
        self.setupUi(self)

    def getImage(self):

        self.current_ll = (37.530887, 55.703118)
        self.current_spn = (0.002, 0.002)
        self.type = 'map'
        params = {
            "ll": ",".join(map(str, self.current_ll)),
            "spn": ",".join(map(str, self.current_ll)),
            "l": self.type
        }
        self.map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(self.map_api_server, params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(self.map_api_server)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StaticMap()
    ex.show()
    sys.exit(app.exec())
