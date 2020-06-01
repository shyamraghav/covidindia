from flask import Flask
import main

app = Flask(__name__)

@app.route('/')
def main_app():
    return main.generate_heatmap()

@app.route('/about')
def about():
    return "This is a python REST application created for educational purpose. Data are fetched from international " \
           "credible sources inferences and findinds are purely experiments. Not for research purpose. Please contact " \ 
           "shyamramanan@gmail.com "

@app.route('/ok')
def health():
    return "ok"

if __name__ == '__main__':
    app.run()