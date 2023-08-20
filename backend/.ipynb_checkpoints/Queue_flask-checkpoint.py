from flask import Flask, render_template, request, redirect, url_for
from spotipy_class import UserSpotify

app = Flask(__name__)

UserOBJ = None  # Global variable to store the UserSpotify object

@app.route('/home', methods=['GET', 'POST'])
def home():
    global UserOBJ
    if UserOBJ is not None:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    global UserOBJ

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        UserOBJ = UserSpotify(username, password)
        queue = UserOBJ.get_queue()
        return render_template('home.html')
    return render_template('login.html')

@app.route('/queue')
def queue():
    global UserOBJ
    if UserOBJ is not None:
        queue = UserOBJ.get_queue()
        if queue is not None:
            return render_template('results1.html', username=UserOBJ.username, listx=queue)
    return redirect(url_for('login'))
    
@app.route('/queue_data')
def queue_data():
    global UserOBJ
    if UserOBJ is not None:
        queue = UserOBJ.get_queue()
        if queue is not None:
            
            return queue
    return []

@app.route('/search_queue', methods=['POST'])
def search_queue():
    global UserOBJ
    search_results = None
    if request.method == 'POST': 
        search_query = request.form['search']
        if UserOBJ is not None:
            search_results = UserOBJ.get_search_results(search_query)
            
            for idx in range(len(search_results)):
                img_url = UserOBJ.get_song_album_cover(search_results[idx][-1])
                search_results[idx].append(img_url)
                
            return render_template('search_results.html', search_results=search_results)
    return ""
@app.route('/search', methods=['GET', 'POST'])
def search():
    global UserOBJ
    search_results = None
    if request.method == 'POST': 
        search_query = request.form['search']
        if UserOBJ is not None:
            search_results = UserOBJ.get_search_results(search_query)
        else:
            return render_template('login.html')
            
    return render_template('search.html', search_results=search_results)

@app.route('/new_playlist', methods=['GET', 'POST'])
def new_playlist():
    global UserOBJ
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        userID = request.form['userID']
        add_songs = request.form['add_songs']
        seed_artists = request.form['seed_artists'].split(' ')
        seed_genres = request.form['seed_genres'].split(' ')
        seed_tracks = request.form['seed_tracks'].split(' ')
        limit = int(request.form['limit'])
        number_of_songs_to_add = int(request.form['number_of_songs_to_add'])
        if add_songs == '1':
            add_songs = True
        else:
            add_songs = False
        # Do something with the data (e.g., create a new playlist)
        # You can replace the following lines with your playlist creation logic.
        # For demonstration purposes, we'll just print the data.
        print("Playlist Name:", name)
        print("User ID:", userID)
        print("Add Songs:", add_songs)
        print("Seed Artists:", seed_artists)
        print("Seed Genres:", seed_genres)
        print("Seed Tracks:", seed_tracks)
        print("Limit:", limit)
        print("Number of Songs to Add:", number_of_songs_to_add)
        
        if seed_artists == ['']:
            seed_artists = None
        if seed_genres == ['']:
            seed_genres = None
        if seed_tracks == ['']:
            seed_tracks = None
        # You can create the playlist here or call a function that handles playlist creation.
        # For example, you could use Spotify API to create a new playlist.
        UserOBJ.new_playlist(userID, name, add_songs_flag=add_songs, seed_artists=seed_artists, seed_genres=seed_genres, seed_tracks=seed_tracks, limit=limit, number_of_songs_to_add=number_of_songs_to_add)
        
        return "Playlist created successfully!"

    return render_template('new_playlist.html')

@app.route('/add_to_queue', methods=['POST'])
def add_to_queue():
    global UserOBJ
    if request.method == 'POST': 
        song_id = request.form.get('song_id')  # Retrieve the song ID from the request
        print(song_id)
        if UserOBJ is not None:
            UserOBJ.add_song_to_queue(song_id)

    return "Song added to queue"  # Return a response indicating success
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
