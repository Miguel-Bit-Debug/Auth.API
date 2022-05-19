from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__, template_folder='template')
Bootstrap(app)

@app.route('/')
def index():
    return "<a href='/posts'>Posts</a>"


@app.route('/redirect')
def redrect_to_response():
    return redirect(url_for('response'))

@app.route('/response')
def response():
    return render_template("response.html")

@app.route('/posts')
@app.route('/posts/<id>')
def posts(id):
    titulo = request.args.get('titulo')
    data = dict(
        path = request.path,
        referrer = request.referrer,
        content_type = request.content_type,
        method = request.method,
        titulo = titulo,
        id = id if id else 0
    )
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)