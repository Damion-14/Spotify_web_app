from flask import Flask, render_template, jsonify, request
from spotipy_class import UserSpotify

app = Flask(__name__)

UserOBJ = None  # Global variable to store the UserSpotify object

@app.route('/', methods=['GET', 'POST'])
def login():
    global UserOBJ

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        UserOBJ = UserSpotify(username, password)
        queue = UserOBJ.get_queue()
        return render_template('results.html', username=username, list=queue)

    return render_template('login.html')

@app.route('/get_queue', methods=['GET'])
def get_queue():
    if UserOBJ is not None:
        queue = UserOBJ.get_queue()
        return jsonify(queue)
    else:
        return jsonify([])  # Return an empty queue if UserOBJ is not initialized

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
