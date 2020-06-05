from flask import Flask, send_file, request
# from main import generate_results
import main

app = Flask(__name__)


@app.route('/')
def main_app():
    return main.try_generate()


# @app.route('/maps/<map_type>')
# def get_maps(map_type):
#     bytes_obj = generate_results()
#
#     return send_file(bytes_obj,
#                      attachment_filename='plot.png',
#                      mimetype='image/png')


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
