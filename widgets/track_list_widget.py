from typing import List
import typing
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QResizeEvent, QFont
import yandex_music as ym
import asyncio

class TrackList(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.app = parent
        self.track_widgets: List[TrackListItem] = []
        self.track_active: TrackListItem = None
        self.current_id: int = None

        self.active = False

        self._init_ui()
    
    def _init_ui(self):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(27, 38, 44))
        self.setPalette(palette)
        self.layout_:QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
    
    def add_track(self, track:ym.Track):
        """функция для создания виджета элемента списка треков"""
        track_widget = TrackListItem(track, len(self.track_widgets), parent=self)
        self.layout_.addWidget(track_widget)
        self.track_widgets.append(track_widget)
    
    def activate(self):
        """активация текущего плейлиста"""
        self.active = True
    
    def deactivate(self):
        """деактивация текущего плейлиста"""
        self.active = False
        self.current_id = None
        if self.track_active:
            self.track_active.set_unactive()
    
    def set_track_list(self, tracks:List[ym.Track]):
        """генерирует виджеты элементов списка треков"""
        for track in tracks:
            self.add_track(track)
    
    def preload_track(self, id):
        """подгрузка следующего трека в списке"""
        loop = asyncio.get_event_loop()
        if id > len(self.track_widgets):
            return loop.run_in_executor(None, self.track_widgets[0].load_track)
        loop.run_in_executor(None, self.track_widgets[id + 1].load_track)
    
    def set_track_active(self, id:int):
        """установка текущего активного трека"""
        if self.current_id == id:
            return
        if not self.active:
            self.app.set_active_playlist(self)
        if self.track_active:
            self.track_active.set_unactive()
        self.current_id = id
        self.track_active = self.track_widgets[id]
        self.track_active.set_active()

        self.preload_track(id)

        self.app.set_current_track_title(self.track_active.title.text())
        self.app.set_playing_track(self.track_active.track_bytes)
    
    def next(self):
        """следующий по списку трек"""
        print('next')
        if self.current_id == len(self.track_widgets) - 1:
            return self.set_track_active(0)
        return self.set_track_active(self.current_id + 1)
    
    def prev(self):
        """предыдущий по списку элемент"""
        print('prev')
        if self.current_id == 0:
            return self.set_track_active(len(self.track_widgets) - 1)
        return self.set_track_active(self.current_id - 1)
        
    



class TrackListItem(QtWidgets.QWidget):
    def __init__(self, track:ym.Track, id,  parent=None) -> None:
        super().__init__(parent=parent)
        self.track_list: TrackList = parent

        self.track:ym.Track = track
        self.id = id

        self.is_track_loaded = False
        self.is_active = False
        self.setup_ui()
    
    def setup_ui(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(27, 38, 44))
        self.setPalette(palette)
        self.layout_ = QtWidgets.QHBoxLayout(self)

        font = QFont()
        font.setPixelSize(18)

        artists = ','.join([artist.name for artist in self.track.artists])
        self.author = QtWidgets.QLabel(artists, self)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(3)
        self.author.setSizePolicy(size_policy)
        self.author.setFont(font)
        self.layout_.addWidget(self.author)

        self.title = QtWidgets.QLabel(self.track.title, self)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(6)
        self.title.setSizePolicy(size_policy)
        self.title.setFont(font)
        self.layout_.addWidget(self.title)

        track_lenght = f'{int(self.track.duration_ms / 60000)}:{int((self.track.duration_ms % 60000) / 1000)}'
        self.track_lenght = QtWidgets.QLabel(track_lenght, self)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(1)
        self.track_lenght.setSizePolicy(size_policy)
        self.track_lenght.setFont(font)
        self.layout_.addWidget(self.track_lenght)

        self.layout_.setAlignment(Qt.AlignTop)
    
    def mousePressEvent(self, a0) -> None:
        super().mousePressEvent(a0)
        self.track_list.set_track_active(self.id)
    
    def enterEvent(self, a0: QtCore.QEvent) -> None:
        super().enterEvent(a0)
        if not self.is_active:
            palette = self.palette()
            palette.setColor(self.backgroundRole(), QColor(86, 86, 89))
            self.setPalette(palette)
    
    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        super().leaveEvent(a0)
        if not self.is_active:
            palette = self.palette()
            palette.setColor(self.backgroundRole(), QColor(27, 38, 44))
            self.setPalette(palette)

    
    def set_active(self):
        """установка этого трека активным"""
        if not self.is_track_loaded:
            self.load_track()
        self.is_active = True

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(52, 55, 70))
        self.setPalette(palette)
    
    def load_track(self):
        """загрузка трека в память"""
        self.track_bytes = self.track.load_track()
        self.is_track_loaded = True
    
    def unload_track(self):
        """выгрузка трека из памяти"""
        del self.track_bytes
        self.is_track_loaded = False
    
    def set_unactive(self):
        """установка этого трека неактивным"""
        self.unload_track()
        
        self.is_active = False

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(27, 38, 44))
        self.setPalette(palette)