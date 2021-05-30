from typing import List
import yandex_music as ym
import concurrent.futures

class Downloader:
    def __init__(self, client:ym.Client, workers=5, requests_per_worker=10) -> None:
        self.client = client
        self.workers = workers
        self.requests_per_worker = requests_per_worker
    
    
    def get_liked(self) -> List[ym.Track]:
        liked_preview = self.client.users_likes_tracks()
        liked_full = self._fetch_tracks(liked_preview)
        return liked_full
    
    def get_liked_artists(self) -> List[ym.Artist]:
        return list(map(lambda like: like.artist, self.client.users_likes_artists()))
    
    def get_playlists(self) -> List[ym.Playlist]:
        return self.client.users_playlists()
    
    def load_artist_tracks(self, artist:ym.Artist) -> List[ym.Track]:
        tracks = artist.counts.tracks
        pages = tracks // self.requests_per_worker

        out = []
        
        with concurrent.futures.ThreadPoolExecutor(self.workers) as executor:
            result = executor.map(lambda page: artist.get_tracks(page, self.requests_per_worker).tracks, range(pages + 1))
        for track_list in result:
            out += track_list
        return out

    def _fetch_tracks(self, tracks:List[ym.TrackShort]):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            result = executor.map(lambda track: track.fetch_track(), tracks)
        return result
    
