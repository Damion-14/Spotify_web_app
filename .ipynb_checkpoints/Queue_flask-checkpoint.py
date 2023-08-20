from flask import Flask, render_template, request, redirect, url_for
from spotipy_class import UserSpotify

app = Flask(__name__)

UserOBJ = None  # Global variable to store the UserSpotify object

@app.route('/home', methods=['GET', 'POST'])
def home():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    global UserOBJ

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        UserOBJ = UserSpotify(username, password)
        queue = UserOBJ.get_queue()
        if queue is not None:
            return render_template('home.html')
        else:
            return 'User Not Listening to Music'
    return render_template('login.html')

@app.route('/queue')
def queue():
    global UserOBJ
    if UserOBJ is not None:
        queue = UserOBJ.get_queue()
        if queue is not None:
            user = UserOBJ.sp.current_user()
            
            username = user['display_name']
            return render_template('results.html', username=username, listx=queue)
    return 'User Not Logged in or Not Listening to Music'

@app.route('/get_queue', methods=['GET'])
def get_queue():
    global UserOBJ
    if UserOBJ is not None:
        queue = UserOBJ.get_queue()
        return jsonify(queue)
    else:
        return jsonify([])  # Return an empty queue if UserOBJ is not initialized

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
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
