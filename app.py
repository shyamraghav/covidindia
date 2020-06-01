from flask import Flask
import main

app = Flask(__name__)

@app.route('/')
def main_app():
    return main.generate_results()

@app.route('/about')
def about():
    return """This is a python REST application created for educational purpose. Data are fetched from international \n
           credible sources inferences and findings are purely experiments. Not for research purpose. Please contact \n 
           shyamramanan@gmail.com """

@app.route('/ok')
def health():
    return "ok"

if __name__ == '__main__':
    app.run()