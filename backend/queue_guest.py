from flask import Flask, render_template, request, redirect, url_for, jsonify
from spotipy_class import UserSpotify


app = Flask(__name__)

# client_id = input('What is your client id? ')

# client_secret = input('What is your client secret? ')

client_id = "f37f818b564747d2b4544dec97671b36"
client_secret = "c0e61c93a6e546888f5d463ccae09d8e"

UserOBJ = UserSpotify("93302b3440374f75bd84102271a41701", "218fdcfb4bab4abf9157c6b8be5d71f8")

liked_songs = []
disliked_songs = []

print(UserOBJ)
@app.route('/queue')
def queue():
    global UserOBJ, liked_songs, disliked_songs
    if UserOBJ is not None:
        
        old_liked_songs = liked_songs
        old_disliked_songs = disliked_songs
        
        liked_songs = []
        disliked_songs = []
        queue = UserOBJ.get_queue()
        for song in queue[1]:
            if song[1] in old_liked_songs:
                liked_songs.append(song[1])
                
            if song[1] in old_disliked_songs:
                disliked_songs.append(song[1])
                
        if queue is not None:
            return render_template('queue_guest.html', username=UserOBJ.username, listx=queue)
    return render_template('queue_guest.html', username=UserOBJ.username, listx=queue)

@app.route('/queue_data')
def queue_data():
    global UserOBJ, liked_songs, disliked_songs
    if UserOBJ is not None:
        queue = UserOBJ.get_queue()
        
        old_liked_songs = liked_songs
        old_disliked_songs = disliked_songs
        
        liked_songs = []
        disliked_songs = []
        queue = UserOBJ.get_queue()
        for song in queue[1]:
            if song[1] in old_liked_songs:
                liked_songs.append(song[1])
                
            if song[1] in old_disliked_songs:
                disliked_songs.append(song[1])
                
        if queue is not None:
            
            return queue
    return []

@app.route('/search', methods=['POST'])
def search():
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

@app.route('/add_to_queue', methods=['POST'])
def add_to_queue():
    global UserOBJ
    if request.method == 'POST': 
        song_id = request.form.get('song_id')  # Retrieve the song ID from the request
        print(song_id)
        if UserOBJ is not None:
            UserOBJ.add_song_to_queue(song_id)

    return "Song added to queue"  # Return a response indicating success
    
    
@app.route('/update_like_status', methods=['POST'])
def dislike():
    global UserOBJ, liked_songs, disliked_songs
    song_id = request.form.get('songId')
    action = request.form.get('action')
    print(song_id)
    print(action)
    if action == 'Love':
        #do something
        liked_songs.append(song_id)
    if action == 'remove Love':
        #do something
       # UserOBJ.skip_song()
        liked_songs.remove(song_id)
    if action == 'thumbs down':
        #do someting
        #UserOBJ.clear_song_from_queue(song_id)
        disliked_songs.append(song_id)
    if action == 'remove thumbs down':
        #do something
        disliked_songs.remove(song_id)
        
        
    
    print("Disliked songs ", disliked_songs)
    print("Liked songs ", liked_songs)
    
    return "Recieved"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)