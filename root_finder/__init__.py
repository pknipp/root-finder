import cmath
from flask import Flask
from . import helper

app = Flask(__name__)

# The following are used to wrap the html string created for server-side rendering.
top = "<head><title>Root finder</title></head><body>"
bottom = '<p align="center">creator:&nbsp;<a href="https://pknipp.github.io/" target="_blank" rel="noopener noreferrer">Peter Knipp</a><br/>repo:&nbsp;<a href="https://github.com/pknipp/root-finder" target="_blank" rel="noopener noreferrer">github.com/pknipp/root-finder</a></p></body>'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    print("path", path)
    if path == 'favicon.ico':
        return app.send_static_file('favicon.ico')
    return app.send_static_file('index.html')


@app.route('/')
def hello():
    html = top + '<div style="padding: 30px;"><p align=center><h3><p align=center>Instructions for finding roots of a polynomial:</p></h3>'
    html += '<p align=center><a href="https://pknipp.github.io/math">Return</a> to the Math APIs page.'
    html += "<div>General:</div><ul>"
    for instruction in helper.general:
        html += "<li>" + instruction + "</li>"
    html += "</ul>"
    html += "<div>Formats:</div><ol><li>array</li><ul>"
    for formatting_instruction in helper.array:
        html += "<li>" + formatting_instruction + "</li>"
    html += "</ul>"
    html += "<li>string:</li><ul>"
    for formatting_instruction in helper.string:
        html += "<li>" + formatting_instruction + "</li>"
    return html + "</ul></ol>" + bottom + '</div></p>'

@app.route('/<str_in>')
def return_html(str_in):
    results = helper.parse_roots(str_in, False)
    if isinstance(results, str):
        return top + results + "</body>"
    else:
        return '<h1>' + results["error"] + '</h1>'

@app.route('/api/<str_in>')
def return_json(str_in):
    return helper.parse_roots(str_in, True)
