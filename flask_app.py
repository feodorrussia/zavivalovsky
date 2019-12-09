from __future__ import unicode_literals

from flask import redirect, render_template, request

from constants import *
from db import Admin
from db import Photo
from login import LoginForm


@app.route('/')
@app.route('/index')
def index():
    gallery = Photo()

    return render_template('index.html', gallery=gallery)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    password = form.password.data
    if Admin.query.filter_by(password=password).all():
        return redirect("/ed_index")
    return render_template('loginform.html', form=form)


@app.route('/ed_index')
def ed_index():
    title = Photo.query.filter_by(descr='title_index').first()
    stallions = [Photo.query.filter_by(descr='stallions').first(),]
    return render_template('ed_index.html', title=title, stallions=stallions)


@app.route('/ed_gallery', methods=['POST', 'GET'])
def ed_gallery():
    if request.method == 'GET':
        return render_template('ed_gallery.html', gallery=Gallery.query.filter_by(gallery_flag=1).all())
    elif request.method == 'POST':

        return redirect("/title")


@app.route('/upload_file', methods=['POST', 'GET'])
def file_upload():
    global i
    if request.method == 'GET':
        return render_template('upload_file.html', )
    elif request.method == 'POST':
        name = request.form.get('name')
        f = request.files['file']
        x = f.__repr__()
        tmp = f.read()
        file_name = x[x.index("'") + 1:x.index("'", 15)]
        n = open("static/img/gallery/" + file_name, "wb")
        n.write(tmp)
        n.close()
        photo = Gallery(filename=file_name)
        db.session.add(photo)
        db.session.commit()
        return redirect("/ed_gallery")


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
