from flask import Flask

app = Flask(__name__)

@app.route('/data')
def get_data():
    
    return {
        'Name': "Jack",
        "Age": "21",
        "programming": "python"
    }

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
