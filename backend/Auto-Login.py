from flask import Flask, redirect, request, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    client_id = request.form['client_id']
    client_secret = request.form['client_secret']
    redirect_uri = request.form['redirect_uri']
    
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=client_id,
                                          client_secret=client_secret,
                                          redirect_uri=redirect_uri,
                                          scope='user-read-playback-state')

    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
