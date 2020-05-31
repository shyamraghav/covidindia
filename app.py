from flask import Flask
import main

app = Flask(__name__))

@app.route('/')
def main_app():
    return main.generate()

@app.route('/ok')
def health():
    return "ok"

if __name__ == '__main__':
    app.run()