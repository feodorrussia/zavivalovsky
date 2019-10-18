from flask import Flask, url_for, session, redirect, render_template, request, jsonify, \
    make_response, \
    request

app = Flask(__name__)
app.secret_key = 'any random string'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/popcorn')
def popcorn():
    return render_template('popcorn.html')


if __name__ == '__main__':
    app.run(debug=True)
'''port=8080, host='127.0.0.1'''