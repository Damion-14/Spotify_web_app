import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.exceptions as spexceptions

class UserSpotify:
    def __init__(self, username, password):
        self.client_id = username
        self.client_secret = password
        redirect_uri = "http://localhost:8080/"  # This should match the redirect URI set in your Spotify app
        scopes = ['playlist-modify-public', 'playlist-modify-private', 'user-read-playback-state']  # Add necessary scopes here

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
                                                            client_secret=self.client_secret,
                                                            redirect_uri=redirect_uri,
                                                            scope=scopes))
        
    def get_queue(self):
        queue = self.sp.queue()
        queue_list = []
        if queue != {'currently_playing': None, 'queue': []}:
            #print(queue['currently_playing']['name'])
            #print('Currently Playing: ', queue['currently_playing']['name']) 
            #print('QUEUE:')
            for item in queue["queue"]:
                queue_list.append(item['name'])
            return [queue['currently_playing']['name'], queue_list]
        else:
            print('User Not Playing Music')
            return None
     
    def new_playlist(userID, name, add_songs_flag=False):
        user_playlists = sp.current_user_playlists()
        user_playlists = [item['name'] for item in user_playlists['items']]
        try:
            playlist = sp.user_playlist_create(userID, name, description='I made this playlist with python')
            playlist_id = playlist['id']
            if add_songs_flag:
                add_songs(userID, playlist_id, seed_artists=['4O15NlyKLIASxsJ0PrXPfz'])
            print('Playlist created successfully!')
        except Exception as e:
            print('Error Encountered: ', e)
            
    def add_songs(user, playlist_id, seed_artists=[], seed_genres=[], seed_tracks=[], number_of_songs_to_add=30):
        tracks_to_add = []
        while len(tracks_to_add) < number_of_songs_to_add:
            recommended_tracks = sp.recommendations(seed_artists=seed_artists, seed_genres=seed_genres, seed_tracks=seed_tracks)
            for item in recommended_tracks['tracks']:
                if item['id'] not in tracks_to_add:
                    tracks_to_add.append(item['id'])

        sp.user_playlist_add_tracks(user, playlist_id, tracks_to_add)
    