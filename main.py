import os
import sys
import requests
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap, QWheelEvent
from PyQt5.QtWidgets import QApplication,  QMainWindow

SCREEN_SIZE = [600, 600]


class StaticMap(QMainWindow):
    current_coord = (37.530887, 55.703118)
    current_spn = (0.002, 0.002)
    current_map = 'map'
    map_api_server = "http://static-maps.yandex.ru/1.x/"

    def __init__(self):
        super().__init__()
        self.initUI()
        self.getImage()

    def getImage(self):
        map_params = {
            "ll": ",".join(map(str, self.current_coord)),
            "spn": ",".join(map(str, self.current_spn)),
            "l": self.current_map
        }
        response = requests.get(self.map_api_server, map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(self.map_api_server)
            print("Http статус:", response.status_code, "(", response.reason, ")")

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        uic.loadUi('map.ui', self)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.angleDelta().y() > 0:
            self.changeMapScale('-')
        else:
            self.changeMapScale('+')
        self.getImage()

    def changeMapScale(self, eventScaleType: str):
        current_change = 1
        if eventScaleType == '-':
            current_change = -current_change
        new_spn = (self.current_spn[0] + current_change, self.current_spn[1] + current_change)
        if 0 <= new_spn[0] <= 90 and 0 <= new_spn[1] <= 90:
            self.current_spn = new_spn

    def changeMapCenterPoint(self, event_change_type: str):
        if event_change_type == 'up':
            current_delta = (0, 1)
            new_coord = (self.current_coord[0] + current_delta[0], self.current_coord[1] + current_delta[1])
        elif event_change_type == 'down':
            current_delta = (0, -1)
            new_coord = (self.current_coord[0] + current_delta[0], self.current_coord[1] + current_delta[1])
        elif event_change_type == 'left':
            current_delta = (-1, 0)
            new_coord = (self.current_coord[0] + current_delta[0], self.current_coord[1] + current_delta[1])
        elif event_change_type == 'right':
            current_delta = (1, 0)
            new_coord = (self.current_coord[0] + current_delta[0], self.current_coord[1] + current_delta[1])
        if 0 <= new_coord[0] <= 90 and 0 <= new_coord[1] <= 180:
            self.current_coord = new_coord

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Up:
            self.changeMapCenterPoint('up')
        if event.key() == QtCore.Qt.Key.Key_Down:
            self.changeMapCenterPoint('down')
        if event.key() == QtCore.Qt.Key.Key_Left:
            self.changeMapCenterPoint('left')
        if event.key() == QtCore.Qt.Key.Key_Right:
            self.changeMapCenterPoint('right')
        self.getImage()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StaticMap()
    ex.show()
    sys.exit(app.exec())
