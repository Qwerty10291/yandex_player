from PyQt5 import QtGui, QtWidgets, QtCore, QtMultimedia
from widgets import main_widget, track_list_widget
import sys
import yandex_music as ym
from player import Player
from downloader import Downloader

TOKEN = 'AgAAAAA3YWoEAAG8XjrpzOfgAkKVr6rn279Ny-k'

class App(QtWidgets.QWidget, Player):
    def __init__(self) -> None:
        super(QtWidgets.QWidget, self).__init__()
        super(Player, self).__init__()

        self.ui = main_widget.Ui_Form()
        self.ui.setupUi(self)

        self.downloader = Downloader(ym.Client.from_token(TOKEN), workers=10)

        self.current_playlist: track_list_widget.TrackList = None

        self.create_playlists()
        self.load_liked()


        self.connect_slots()
        self.create_shortcuts()

    def create_playlists(self):
        """создание виджетов вкладок"""
        self.liked_widget = track_list_widget.TrackList(self)
        self.ui.scrollArea.setWidget(self.liked_widget)

    def load_liked(self):
        """загрузка информации о любимых треках"""
        tracks = self.downloader.get_liked()
        self.liked_widget.set_track_list(tracks)
    
    def set_current_track_title(self, title):
        """установка названия текущего трека в меню плеера"""
        self.ui.current_track_title.setText(title)
    
    def set_active_playlist(self, playlist:track_list_widget.TrackList):
        """установка плейлиста активным. Вызывается из потомка главного окна"""
        if self.current_playlist:
            self.current_playlist.deactivate()
        self.current_playlist = playlist
        self.current_playlist.activate()
    
    
    def check_media_status(self, status):
        """слот для qmediaplayer, который по окончании проигрывания запускает следующий трек"""
        if status == QtMultimedia.QMediaPlayer.EndOfMedia:
            self.next()
    
    def duration_changed(self, duration):
        if not duration or not self.player.duration():
            return
        progress = int(duration / self.player.duration() * 100)
        if abs(self.ui.progress.progress - progress) >= 1:
            self.ui.progress.set_progress(progress)
    
    def move_to_track(self):
        if not self.current_playlist:
            return
        if not self.current_playlist.isHidden():
            self.ui.scrollArea.ensureWidgetVisible(self.current_playlist.track_active)

    
    def connect_slots(self):
        self.ui.btn_next.clicked.connect(self.next)
        self.ui.btn_prev.clicked.connect(self.prev)
        self.ui.btn_play.clicked.connect(self.play_pause)
        self.ui.progress.position_signal(self.set_current_position)

        self.player.mediaStatusChanged.connect(self.check_media_status)
        self.player.positionChanged.connect(self.duration_changed)

    
    def create_shortcuts(self):
        self.play_shortcut = QtWidgets.QShortcut('space+ctrl', self, self.play_pause)
        self.next_shortcut = QtWidgets.QShortcut('ctrl+right', self, self.next)
        self.prev_shortcut = QtWidgets.QShortcut('ctrl+left', self, self.prev)
        self.move_to_track_shortcut = QtWidgets.QShortcut('ctrl+m', self, self.move_to_track)

        
if __name__ == '__main__':
    executor = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    sys.exit(executor.exec_())