from flask import Flask, make_response, jsonify

app = Flask(__name__)

@app.route("/")
def data():
    resp = make_response(jsonify(
        username="Jack",
        taste=["rap", "rock"]
        ))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

"""
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
"""
if __name__ == '__main__':
    app.run(debug=True)
