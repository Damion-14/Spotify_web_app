from flask import Flask, render_template, request, redirect, url_for, jsonify
from spotipy_class import UserSpotify


app = Flask(__name__)

# client_id = input('What is your client id? ')

# client_secret = input('What is your client secret? ')

client_id = "f37f818b564747d2b4544dec97671b36"
client_secret = "c0e61c93a6e546888f5d463ccae09d8e"

UserOBJ = UserSpotify("93302b3440374f75bd84102271a41701", "218fdcfb4bab4abf9157c6b8be5d71f8")

liked_songs = {}
disliked_songs = {}

<<<<<<< HEAD
=======
class Node:
    def __init__(self, data, next):
        self.data = data
        self.next = next

    def displayData(self):
        print(self.data)
        print(self.next)
        
queue = UserOBJ.get_queue()
node_obj = Node(queue)

print(UserOBJ)
>>>>>>> 97206464b8954699b43fc0428ade05a6ff46affe
@app.route('/queue')
def queue():
    global UserOBJ, liked_songs, disliked_songs, node_obj
    if UserOBJ is not None:
        queue = UserOBJ.get_queue()

        for user in liked_songs.keys():
            users_liked_songs = liked_songs[user]
            users_disliked_songs = disliked_songs[user]
            
            for song in users_liked_songs:
                if not any(song == queue_song[1] for queue_song in queue[1]):
                    print("Remove: ", song)
                    if song in liked_songs[user]:
                        liked_songs[user].remove(song)
                
            
            for song in users_disliked_songs:
                if not any(song == queue_song[1] for queue_song in queue[1]):
                    print("Remove: ", song)
                    if song in disliked_songs[user]:
                        disliked_songs[user].remove(song)
        if queue:
            for idx in range(len(queue[1])):
                song = queue[1][idx][1]
                if song[1] in liked_songs[user]:
                    queue[1][idx][1].append(True)
                else:
                    queue[1][idx][1].append(False)
                if song in disliked_songs[user]:
                    queue[1][idx][1].append(True)
                else:
                    queue[1][idx][1].append(False)
                
            
                
        if queue is not None:
            return render_template('queue_guest.html', username=UserOBJ.username, listx=queue)
    return render_template('queue_guest.html', username=UserOBJ.username, listx=queue)

@app.route('/queue_data')
def queue_data():
    global UserOBJ, liked_songs, disliked_songs
    if UserOBJ is not None:
        queue = UserOBJ.get_queue()
        
        for user in liked_songs.keys():
            users_liked_songs = liked_songs[user]
            users_disliked_songs = disliked_songs[user]
            
            for song in users_liked_songs:
                if not any(song == queue_song[1] for queue_song in queue[1]):
                    print("Remove: ", song)
                    if song in liked_songs[user]:
                        liked_songs[user].remove(song)
                
            
            for song in users_disliked_songs:
                if not any(song == queue_song[1] for queue_song in queue[1]):
                    print("Remove: ", song)
                    if song in disliked_songs[user]:
                        disliked_songs[user].remove(song)
        
        queue = UserOBJ.get_queue()
                
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
def update_like_status():
    global UserOBJ, liked_songs, disliked_songs
    
    user_ip = request.remote_addr
    print(user_ip)
    
    if user_ip not in liked_songs:
        liked_songs[user_ip] = []
        disliked_songs[user_ip] = []
   
    song_id = request.form.get('songId')
    action = request.form.get('action')
    
    if action == 'Love':
        liked_songs[user_ip].append(song_id)
        
    elif action == 'remove Love':
        liked_songs[user_ip].remove(song_id)
        
    elif action == 'thumbs down':
        
        disliked_songs[user_ip].append(song_id)
        
    elif action == 'remove thumbs down':
        disliked_songs[user_ip].remove(song_id)
        
    print("Disliked songs ", disliked_songs)
    print("Liked songs ", liked_songs)
    
    return "Received"

@app.route('/get_songs_status')
def get_songs_status():
    global UserOBJ, liked_songs, disliked_songs
    if UserOBJ is not None:
        user_ip = request.remote_addr
        if liked_songs == {}:
            return ['NONE']
        return [liked_songs[user_ip], disliked_songs[user_ip]]

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)