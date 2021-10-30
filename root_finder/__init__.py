import os, cmath
from flask import Flask
from root_finder.config import Config
from . import helper

app = Flask(__name__)
app.config.from_object(Config)

# Application Security
# CORS(app)

top = "<head><title>Root finder</title></head><body>"

bottom = "<span>creator:&nbsp;<a href='https://pknipp.github.io/' target='_blank' rel='noopener noreferrer'>Peter Knipp</a></span></body>"

# @app.after_request
# def inject_csrf_token(response):
#     response.set_cookie(
#         'csrf_token',
#         generate_csrf(),
#         secure=True if os.environ.get('FLASK_ENV') else False,
#         samesite='Strict' if os.environ.get('FLASK_ENV') else None,
#         httponly=True)
#     return response


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    print("path", path)
    if path == 'favicon.ico':
        return app.send_static_file('favicon.ico')
    return app.send_static_file('index.html')


@app.route('/')
def hello():
    html = top + "<h3><p align=center>Instructions:</p></h3>"
    html += "<div>General:</div><ul>"
    for line in helper.general:
        html += "<li>" + line + "</li>"
    html += "</ul>"
    html += "<div>Formats:</div><ol><li>array</li><ul>"
    for line in helper.array:
        html += "<li>" + line + "</li>"
    html += "</ul>"
    html += "<li>string:</li><ul>"
    for line in helper.string:
        html += "<li>" + line + "</li>"
    return html + "</ul></ol>" + bottom

    # return {"instructions": [ \
        # {"general": helper.general}, \
        # {"formats": [{"array": helper.array}, {"string": "UNDER CONSTRUCTION"}]} \
    # ]}

@app.route('/<str_in>')
def return_html(str_in):
    results = helper.parse_roots(str_in, False)
    return (top + results + bottom) if isinstance(results, str) else results #("<h1>" + results["error"] + "</h1>")

@app.route('/json/<str_in>')
def return_json(str_in):
    return helper.parse_roots(str_in, True)
