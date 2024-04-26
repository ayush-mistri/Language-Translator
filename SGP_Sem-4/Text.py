from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def text():
    return render_template('Text.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

