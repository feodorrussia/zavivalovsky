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


@app.route('/uprek')
def uprek():
    return render_template('uprek.html')

@app.route('/prelat')
def prelat():
    return render_template('prelat.html')

@app.route('/dakar')
def dakar():
    return render_template('dakar.html')

@app.route('/kreker')
def kreker():
    return render_template('kreker.html')

@app.route('/sale')
def sale():
    return render_template('sale.html')

@app.route('/news')
def news():
    return render_template('news.html')


if __name__ == '__main__':
    app.run(debug=True)
'''port=8080, host='127.0.0.1'''