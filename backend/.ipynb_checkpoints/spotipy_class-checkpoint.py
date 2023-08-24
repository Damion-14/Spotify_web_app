import spotipy
from spotipy.oauth2 import SpotifyOAuth

class UserSpotify:
    def __init__(self, client_id, client_secret):
        # Initialize the UserSpotify class with the provided client_id and client_secret.
        # Create an instance of the Spotipy client with appropriate authentication settings.
        self.client_id = client_id
        self.client_secret = client_secret
        redirect_uri = "http://localhost:8080/"  # This should match the redirect URI set in your Spotify app
        scopes = ['playlist-modify-public', 'playlist-modify-private', 'user-read-playback-state', \
                  'app-remote-control', 'streaming']  # Add necessary scopes here

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
                                                            client_secret=self.client_secret,
                                                            redirect_uri=redirect_uri,
                                                            scope=scopes))
        user = self.sp.current_user()
        self.username = user['display_name']
        self.user_id = user['id']
        
        self.currently_playing = None
        self.queue = None
        self.playlists = None
        self.name = client_id

    def get_queue(self):
        """
        Returns the User's Queue.
        The user's queue is a list of songs that are currently playing or in the queue to be played.
        The function makes use of the `queue()` method from the Spotipy library to retrieve this information.
        It returns a list where the first element is the song currently playing and the second element is the list of songs in the 
        queue.
        """
        try:
            queue = self.sp.queue()
            if queue != {'currently_playing': None, 'queue': []}:
                currently_playing = [queue['currently_playing']['name'], queue['currently_playing']['id'], \
                                     self.get_song_album_cover(queue['currently_playing']['id'], image = 1)]
                #print(queue["queue"][0]['album']['artists'])
                queue_list = [[item['name'],item['id'], self.get_song_album_cover(item['id'], image = 2)] for item in queue["queue"]]
                self.queue = queue_list
                self.currently_playing = currently_playing
                return [currently_playing, queue_list]
            else:
                #print('User Not Playing Music')
                return None
        except spotipy.exceptions.SpotifyException as e:
            print('Error Encountered: ', e)
            return None

    def new_playlist(self, name, add_songs_flag=False, seed_artists=[], seed_genres=[], seed_tracks=[], limit=None,
                     number_of_songs_to_add=None, description='I made this playlist with python'):
        """
        Creates a new playlist with the given 'name' for a given userID.
        You can choose to add songs with the add_songs_flag.
        You can provide seeds (artists, genres, and tracks) to get recommendations for adding songs to the playlist.
        """
        user_playlists = self.sp.current_user_playlists()
        user_playlists = [item['name'] for item in user_playlists['items']]
        self.playlists = user_playlists
        if name in user_playlists:
            return 'Playlist name already exists'
        try:
            playlist = self.sp.user_playlist_create(self.user_id, name, description=description)
            playlist_id = playlist['id']
            if add_songs_flag:
                add_songs = self.add_songs(self.user_id, playlist_id, seed_artists=seed_artists, seed_genres=seed_genres, \
                               seed_tracks=seed_tracks, limit=limit,
                              number_of_songs_to_add=number_of_songs_to_add)
            return {'message': f'Playlist Created Successfully, {add_songs}'}
        except spotipy.exceptions.SpotifyException as e:
            return {'messgae': f'Error Encountered: {e}'}

    def add_songs(self, user, playlist_id, seed_artists=[], seed_genres=[], seed_tracks=[], limit=20, number_of_songs_to_add=30):
        """
        Adds songs to a playlist for the given 'user' and 'playlist_id'.
        You can provide seeds (artists, genres, and tracks) to get recommendations for adding songs to the playlist.
        'limit' limits how many songs are returned by recommendations.
        'number_of_songs_to_add' is the number of songs that will be added to the playlist.
        """
        try:
            tracks_to_add = []
            while len(tracks_to_add) < number_of_songs_to_add:
                recommended_tracks = self.sp.recommendations(seed_artists=seed_artists, seed_genres=seed_genres, \
                                                 seed_tracks=seed_tracks, limit=limit)
                for item in recommended_tracks['tracks']:
                    if item['id'] not in tracks_to_add:
                        tracks_to_add.append(item['id'])
                        if len(tracks_to_add) >= number_of_songs_to_add:  # Changed > to >=
                            break

            if tracks_to_add:
                self.sp.user_playlist_add_tracks(user, playlist_id, tracks_to_add)
                return f"{len(tracks_to_add)} tracks added to the playlist"
            else:
                return "No recommended tracks found to add to the playlist"

        except spotipy.SpotifyException as e:
            return f"An error occurred while adding songs: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"
        
    
    def get_playlists(self):
        """
        Retrieves the playlists for the current user and returns a list of lists containing playlist names and their respective IDs.
        """
        user_playlists = self.sp.current_user_playlists()
        user_playlists = [[item['name'], item['id']] for item in user_playlists['items']]
        return user_playlists
    
    def get_songs_in_playlist(self, playlist_id):
        """
        Retrieves all the songs in a playlist with the given 'playlist_id'.
        It fetches the tracks in the playlist using the `playlist_items()` method from the Spotipy library.
        It returns a list of lists containing song names and their respective IDs in the playlist.
        """
        all_items = []
        offset = 0
        while True:
            items = self.sp.playlist_items(playlist_id, offset=offset)
            if not items['items']:
                break
            all_items.extend([[item['track']['name'], item['track']['id']] for item in items['items']])
            offset += len(items['items'])
        return all_items
    
    def get_playlist_id_from_name(self, playlist_name):
        """
        Gets the playlist ID for a given 'playlist_name'.
        It fetches all the user's playlists and finds the ID of the playlist with the matching name.
        """
        playlist_list = self.get_playlists()
        for playlist in playlist_list:
            if playlist[0].lower() == playlist_name.lower():
                return playlist[1]
        return None
    
    def get_search_results(self, q):
        """
        Searches for songs based on the query 'q'.
        It uses the `search()` method from the Spotipy library to perform the search.
        The function returns a list of lists containing song names, artist names, and their respective IDs in the search results.
        """
        search = self.sp.search(q)
        results_list = []
        for item in search['tracks']['items']:
            song_name = item['name']
            artists_data = item['album']['artists']
            artist_names = [artist['name'] for artist in artists_data]
            song_id = item['id']
            artist_names_str = ', '.join(artist_names)
            results_list.append([song_name,artist_names_str, song_id])
        return results_list
    
    def get_song_album_cover(self, songID, image = 2):
        albumID = self.sp.track(songID)['album']
        return albumID['images'][image]['url']

    def add_song_to_queue(self, songID):
        result = self.sp.add_to_queue(songID)
        return result
    
    def skip_song(self):
        self.sp.next_track()
        return "Skipped"
    
    def clear_song_from_queue(self, songid):
        current_queue = self.get_queue()
        #[[name, songid, album cover url]]
        
        self.sp.pause_playback()
        # Skip through the tracks to clear the queue
        print((range(len(current_queue[1]) - 2)))
        for x in range(len(current_queue[1]) - 2):
            self.sp.next_track()
            
        self.sp.start_playback()
        for song in current_queue[1]:
            if song[1] == songid:
                #skip song that is passed...aka remove it from being added bach to the queue
                continue
            #add song to queue
            print(song[1])
            self.sp.add_to_queue(song[1])
        return "removed from queue"
        
        