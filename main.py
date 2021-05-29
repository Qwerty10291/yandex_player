from PyQt5 import QtWidgets, QtCore
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
    
    def next(self):
        if self.current_playlist:
            self.current_playlist.next()
    
    def prev(self):
        if self.current_playlist:
            self.current_playlist.prev()
    
    def connect_buttons(self):
        self.ui.btn_next.clicked.connect(self.next)
        self.ui.btn_prev.clicked.connect(self.prev)

        

if __name__ == '__main__':
    executor = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    sys.exit(executor.exec_())