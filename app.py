from flask import Flask, send_file, request
import main



app = Flask(__name__)


@app.route('/')
def main_app():
    return main.generate_results()


@app.route('/maps/<map_type>')
def get_maps(map_type):
    if request.args.get('type') == '1':
        filename = map_type + '.jpg'
    else:
        filename = 'error.gif'
    return send_file(filename, mimetype='image/jpg')


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
