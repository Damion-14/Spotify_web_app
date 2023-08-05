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
        self.currently
    def get_queue(self):
        """
        Returns the Users Queue
        list of lists
        get_queue()[0] = song currently playing
        """
        queue = self.sp.queue()
        queue_list = []
        #checks if user is listening to music
        if queue != {'currently_playing': None, 'queue': []}:
            
            #loop through songs in queue and append their name, 
            #can append song id eventually with item['id']
            
            for item in queue["queue"]:
                queue_list.append(item['name'])
            return [queue['currently_playing']['name'], queue_list]
        else:
            print('User Not Playing Music')
            return None
     
    def new_playlist(userID, name, add_songs_flag=False, seed_artists=[], seed_genres=[], seed_tracks=[], limit=None, \
                     number_of_songs_to_add=None):
        """
        will create a new playlist with given 'name' for a given userID
        you can choose to add songs with add_songs_flag
        add seeds you want
        """
        user_playlists = sp.current_user_playlists()
        user_playlists = [item['name'] for item in user_playlists['items']]
        if name in user_playlists:
            return 'Playlist name already exsits'
        try:
            playlist = sp.user_playlist_create(userID, name, description='I made this playlist with python')
            playlist_id = playlist['id']
            if add_songs_flag:
                add_songs(userID, playlist_id, seed_artists=seed_artists, seed_genres=seed_genres, seed_tracks=seed_tracks, limit,\
                         number_of_songs_to_add=number_of_songs_to_add)
            print('Playlist created successfully!')
        except Exception as e:
            print('Error Encountered: ', e)
            
    def add_songs(user, playlist_id, seed_artists=[], seed_genres=[], seed_tracks=[], limit=20, number_of_songs_to_add=30):
        """
        user - userID
        playlist_id - id of the playlist you want to add songs to 
        seed_XXXXX - can input 5 total seeds in any category and the recommendations will give songs relatred to those seeds
        limit - limits how many songs are returned by recommendations
        number_of_songs_to_add - number of songs that will be added to the playlist, it wont add dups but will if it was in the 
                                playlist before running this func
        
        """
        tracks_to_add = []
        while len(tracks_to_add) < number_of_songs_to_add:
            recommended_tracks = sp.recommendations(seed_artists=seed_artists, seed_genres=seed_genres, \
                                                    seed_tracks=seed_tracks, limit=limit)
            for item in recommended_tracks['tracks']:
                if item['id'] not in tracks_to_add:
                    tracks_to_add.append(item['id'])

        sp.user_playlist_add_tracks(user, playlist_id, tracks_to_add)
        
    