from flask import Flask, render_template, request

app = Flask(__name__, template_folder='.')


@app.route('/')
def index():
    return render_template('index.html')


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)