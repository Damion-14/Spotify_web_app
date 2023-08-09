from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks

from spotipy_class import UserSpotify  # Import the UserSpotify class from Spotify_class
import csv
import time

app = FastAPI()

# # Create an instance of the UserSpotify class with your Spotify app credentials

# spotify = UserSpotify(client_id, client_secret)

# Create a dictionary to store UserSpotify instances for each user
user_instances = {}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/login")
def login(request: Request, client_id: str, client_secret: str, username: str):
    client_ip = request.client.host  # Get the user's IP address
    
    # Check if the user already exists in the CSV file
    user_exists = False
    with open('/home/orangepi/Documents/Code/Spotify_web_app/backend/user_data/users_csv.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] == client_id:
                user_exists = True
                if client_id in user_instances.keys():
                    print('IN user_instances')
                user_instances[row[0]] = {"instance": UserSpotify(row[0], row[1]), "ip": client_ip, 'login_time': time.time()}
                break
    
    if not user_exists:
        # If user doesn't exist, add the user to the CSV file
        with open('/home/orangepi/Documents/Code/Spotify_web_app/backend/user_data/users_csv.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([client_id, client_secret, client_ip])
            
        user_instances[client_id] = {"instance": UserSpotify(client_id, client_secret), "ip": client_ip, 'login_time': time.time()}
        return {"message": "Logged in and user data added to CSV"}
    
    return {"message": "Logged in"}

# Define routes to interact with the Spotify API using the UserSpotify instance
@app.post("/get_queue")
def get_queue(client_id: str):
    queue = user_instances[client_id]["instance"].get_queue()
    if queue is None:
        return {"message": "User is not playing music"}
    return {"currently_playing": queue[0], "queue": queue[1]}

def clean_and_validate_seeds(seed: str) -> list:
    if seed is None:
        return []
    cleaned_seed = [s.strip() for s in seed.split(',') if s.strip()]
    return cleaned_seed

@app.post("/new_playlist")
def new_playlist(client_id: str, name: str, add_songs_flag: bool = False, seed_artists: str = None,
                 seed_genres: str = None, seed_tracks: str = None, limit: int = None,
                 number_of_songs_to_add: int = None, description: str = None):
    
    seed_artists = clean_and_validate_seeds(seed_artists)
    seed_genres = clean_and_validate_seeds(seed_genres)
    seed_tracks = clean_and_validate_seeds(seed_tracks)
        
    print(name, add_songs_flag, seed_artists, seed_genres,seed_tracks, limit, number_of_songs_to_add, description)
        
    result = user_instances[client_id]["instance"].new_playlist(name, add_songs_flag, seed_artists, seed_genres,
                                  seed_tracks, limit, number_of_songs_to_add, description)
    return {"message": result}

@app.post("/add_songs_to_playlist")
def add_songs_to_playlist(
    client_id: str,
    playlist_name: str,
    seed_artists: str = None,
    seed_genres: str = None,
    seed_tracks: str = None,
    limit: int = None,
    number_of_songs_to_add: int = None,
):
    playlist_id = user_instances[client_id]["instance"].get_playlist_id_from_name(playlist_name)
    if playlist_id is None:
        return {"message": f"Playlist '{playlist_name}' not found"}

    result = user_instances[client_id]["instance"].add_songs(
        user_instances[client_id]["instance"].user_id,
        playlist_id,
        seed_artists=seed_artists,
        seed_genres=seed_genres,
        seed_tracks=seed_tracks,
        limit=limit,
        number_of_songs_to_add=number_of_songs_to_add,
    )
    return {"message": result}


@app.post("/get_playlists")
def get_playlists(client_id: str):
    playlists = user_instances[client_id]["instance"].get_playlists()
    return {"playlists": playlists}

@app.post("/get_songs_in_playlist")
def get_songs_in_playlist(client_id: str, playlist_id: str):
    songs = user_instances[client_id]["instance"].get_songs_in_playlist(playlist_id)
    return {"songs_in_playlist": songs}

@app.post("/search")
def search(client_id: str, q: str):
    search_results = user_instances[client_id]["instance"].get_search_results(q)
    return {"search_results": search_results}




def check_active_users():
    while True:
        now = time.time()
        for user_id in user_instances.keys():
            last_access_time = user_instances[user_id]['login_time']
            now = time.time()
            if now - last_access_time > 3600:  # Assume user is inactive after 1 hour
                user_instances.pop(user_id, None)
        time.sleep(600)  # Check every 10 minutes
# Add more routes to interact with other methods of the UserSpotify class

background_tasks = BackgroundTasks()
background_tasks.add_task(check_active_users)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
