from typing import Union
from fastapi import FastAPI
from spotipy_class import UserSpotify  # Import the UserSpotify class from Spotify_class

app = FastAPI()

# # Create an instance of the UserSpotify class with your Spotify app credentials
# client_id = "779617d6c75e425992d9aad1336fc8e4"
# client_secret = "a9b25d041321424b8b9ddbbb804ab80e"
# spotify = UserSpotify(client_id, client_secret)

# Create a dictionary to store UserSpotify instances for each user
user_instances = {}

@app.get("/")
def read_root():
    return {"Hello": "World"}

#
@app.post("/login")
def login(client_id: str, client_secret: str):
    # Check if the user already has an instance, if not, create one
    if client_id not in user_instances:
        user_instances[client_id] = UserSpotify(client_id, client_secret)
    return {"message": "Logged in"}

# Define routes to interact with the Spotify API using the UserSpotify instance
@app.post("/get_queue")
def get_queue(client_id: str):
    queue = user_instances[client_id].get_queue()
    if queue is None:
        return {"message": "User is not playing music"}
    return {"currently_playing": queue[0], "queue": queue[1]}

@app.post("/new_playlist")
def new_playlist(userID: str, name: str, add_songs_flag: bool = False, seed_artists: list = [],
                 seed_genres: list = [], seed_tracks: list = [], limit: int = None,
                 number_of_songs_to_add: int = None):
    result = spotify.new_playlist(userID, name, add_songs_flag, seed_artists, seed_genres,
                                  seed_tracks, limit, number_of_songs_to_add)
    return {"message": result}


# Add more routes to interact with other methods of the UserSpotify class

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
