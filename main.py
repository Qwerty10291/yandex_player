from PyQt5 import QtWidgets, QtCore, QtMultimedia
from widgets import main_widget, track_list_widget
import sys
import yandex_music as ym

TOKEN = 'AgAAAAA3YWoEAAG8XjrpzOfgAkKVr6rn279Ny-k'

class App(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = main_widget.Ui_Form()
        self.ui.setupUi(self)

        self.client = ym.Client.from_token(TOKEN)

        self.current_playlist: track_list_widget.TrackList = None

        print(self.client.token)
        self.create_playlists()
        self.load_liked()

        self.player = QtMultimedia.QMediaPlayer(self)
        self.is_playing = False

        self.connect_buttons()


    def create_playlists(self):
        self.liked_widget = track_list_widget.TrackList(self)
        self.ui.scrollArea.setWidget(self.liked_widget)

    def load_liked(self):
        tracks = map(lambda track: track.fetch_track(), self.client.users_likes_tracks()[:20])
        self.liked_widget.set_track_list(tracks)
    
    def set_current_track_title(self, title):
        self.ui.current_track_title.setText(title)
    
    def set_active_playlist(self, playlist:track_list_widget.TrackList):
        if self.current_playlist:
            self.current_playlist.deactivate()
        self.current_playlist = playlist
        self.current_playlist.activate()
    
    def set_playing_track(self, track_bytes):
        array = QtCore.QByteArray(track_bytes)
        self.buffer = QtCore.QBuffer(self)
        self.buffer.setData(array)
        self.buffer.open(QtCore.QIODevice.ReadOnly)
        self.player.deleteLater()
        self.player = QtMultimedia.QMediaPlayer(self)
        print('opened')
        self.player.setMedia(QtMultimedia.QMediaContent(), self.buffer)
        self.player.mediaStatusChanged.connect(self.check_media_status)
        self.player.play()
        self.is_playing = True
    
    def check_media_status(self, status):
        if status == QtMultimedia.QMediaPlayer.EndOfMedia:
            self.next()

    def next(self):
        if self.current_playlist:
            self.player.stop()
            self.current_playlist.next()
    
    def prev(self):
        if self.current_playlist:
            self.player.stop()
            self.current_playlist.prev()
    
    
    def play_pause(self):
        if self.current_playlist:
            if self.is_playing:
                self.player.pause()
                self.is_playing = False
            else:
                self.player.play()
                self.is_playing = True

    
    def connect_buttons(self):
        self.ui.btn_next.clicked.connect(self.next)
        self.ui.btn_prev.clicked.connect(self.prev)
        self.ui.btn_play.clicked.connect(self.play_pause)

        

if __name__ == '__main__':
    executor = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    sys.exit(executor.exec_())