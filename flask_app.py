from flask import Flask, url_for, session, redirect, render_template, request, jsonify, \
    make_response, \
    request

from login import LoginForm

app = Flask(__name__)
app.secret_key = 'any random string'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    password = form.password.data
    if password=='123467890':
        return redirect("/title")
    return render_template('loginform.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


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


@app.route('/runners')
def runners():
    return render_template('runners.html')


@app.route('/heavy')
def heavy():
    return render_template('heavy.html')


@app.route('/heavy_ex')
def heavy_ex():
    return render_template('heavy_ex.html')


@app.route('/stallions')
def stallions():
    return render_template('stallions.html')


@app.route('/mares')
def mares():
    return render_template('mares.html')


@app.route('/foals')
def foals():
    return render_template('foals.html')


if __name__ == '__main__':
    app.run(debug=True)
'''port=8080, host='127.0.0.1'''
