from PyQt5 import QtMultimedia, QtCore

class Player:
    def __init__(self):
        self.player = QtMultimedia.QMediaPlayer(self)
        self.is_playing = False
    
    def set_playing_track(self, track_bytes):
        """принимает на вход сырой бинарник трека, обрабатывает и запускает плеер"""
        array = QtCore.QByteArray(track_bytes)
        self.buffer = QtCore.QBuffer(self)
        self.buffer.setData(array)
        self.buffer.open(QtCore.QIODevice.ReadOnly)
        self.player.setMedia(QtMultimedia.QMediaContent(), self.buffer)
        self.play()
        self.is_playing = True
    
    def set_current_position(self, progress):
        if self.player.duration():
            duration = self.player.duration() / 100 * progress
            self.player.setPosition(duration)
    
    def next(self):
        if self.current_playlist:
            self.stop()
            self.current_playlist.next()
    
    def prev(self):
        if self.current_playlist:
            self.stop()
            self.current_playlist.prev()
    
    def stop(self):
        if self.current_playlist:
            self.player.stop()
            self.ui.set_button_pause()
            self.is_playing = False
    
    def pause(self):
        if self.current_playlist:
            self.player.pause()
            self.ui.set_button_play()
            self.is_playing = False
    
    def play(self):
        if self.current_playlist:
            self.player.play()
            self.ui.set_button_pause()
            self.is_playing = True
    
    def play_pause(self):
        if self.current_playlist:
            if self.is_playing:
                self.pause()
            else:
                self.play()