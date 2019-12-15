from __future__ import unicode_literals

from flask import redirect, render_template, request

from constants import *
from db import Admin
from db import Data
from db import Files
from db import Photo
from little_functions import *
from login import LoginForm


@app.route('/')
@app.route('/index')
def index():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return render_template('index.html', photo=Photo(), data=Data(),
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr))


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    password = form.password.data
    if Admin.query.filter_by(password=password).all():
        Admin.query.filter_by(id=0).first().status = 1
        db.session.commit()
        return redirect("/ed_title")
    return render_template('loginform.html', form=form)


@app.route('/ed_title', methods=['POST', 'GET'])
def ed_title():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    lenght = len(a)
    if request.method == 'GET':
        return render_template('ed_title.html', photo=Photo(), data=Data(), len=lenght, photos=Files())
    elif request.method == 'POST':
        filename = request.form.get('title')
        if filename != '' and Files.query.filter_by(filename=filename).all():
            photo = Photo.query.filter_by(descr="container-title").first()
            photo.filename = filename
            db.session.commit()
        return render_template('ed_title.html', photo=Photo(), data=Data(), len=lenght, photos=Files())


@app.route('/ed_about', methods=['POST', 'GET'])
def ed_about():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    lenght = len(a)
    if request.method == 'GET':
        return render_template('ed_about.html', photo=Photo(), data=Data(), len=lenght, photos=Files())
    elif request.method == 'POST':
        filename = request.form.get('background')
        descr = request.form.get('title')
        if filename != '' and Files.query.filter_by(filename=filename).all():
            photo = Photo.query.filter_by(descr="about").first()
            photo.filename = filename
            db.session.commit()
        if descr != '':
            inf = Data.query.filter_by(name="about").first()
            inf.descr = descr.upper()
            db.session.commit()
        return render_template('ed_about.html', photo=Photo(), data=Data(), len=lenght, photos=Files())


@app.route('/ed_news', methods=['POST', 'GET'])
def ed_news():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    lenght = len(a)
    if request.method == 'GET':
        return render_template('ed_news.html', photo=Photo(), data=Data(), len=lenght, photos=Files())
    elif request.method == 'POST':
        filename = request.form.get('background')
        descr = request.form.get('title')
        if filename != '' and Files.query.filter_by(filename=filename).all():
            photo = Photo.query.filter_by(descr="news").first()
            photo.filename = filename
            db.session.commit()
        if descr != '':
            inf = Data.query.filter_by(name="news").first()
            inf.descr = descr.upper()
            db.session.commit()
        return render_template('ed_news.html', photo=Photo(), data=Data(), len=lenght, photos=Files())


@app.route('/ed_gallery', methods=['POST', 'GET'])
def ed_gallery():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    lenght = len(a)
    if request.method == 'GET':
        return render_template('ed_gallery.html', gallery=Photo.query.filter_by(descr="gallery").all(), photo=Photo(),
                               data=Data(), len=lenght, photos=Files())
    elif request.method == 'POST':
        for i in range(9):
            filename = request.form.get('img' + str(i))
            if filename != '' and Files.query.filter_by(filename=filename).all():
                photo = Photo.query.filter_by(id=i).first()
                photo.filename = filename
                db.session.commit()
        return render_template('ed_gallery.html', gallery=Photo.query.filter_by(descr="gallery").all(), photo=Photo(),
                               data=Data(), len=lenght, photos=Files())


@app.route('/ed_contacts', methods=['POST', 'GET'])
def ed_contacts():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    lenght = len(a)
    contacts = "\n".join(open("static/text_data/contacts.txt", "r").read().split("\n/*/\n"))
    if request.method == 'GET':
        return render_template('ed_contacts.html', photo=Photo(), data=Data(), len=lenght, photos=Files(),
                               contacts=contacts)
    elif request.method == 'POST':
        text = request.form.get('contacts')
        if text != '':
            file = open("static/text_data/contacts.txt", "w")
            contacts = "\n/*/\n".join(text.split("\n"))
            file.write(contacts)
        return render_template('ed_contacts.html', photo=Photo(), data=Data(), len=lenght, photos=Files(),
                               contacts=contacts)


@app.route('/ed_story/<int:index>', methods=['POST', 'GET'])
def ed_story(index):
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    history = information_extractor("history.txt")
    data = [i.split("\n/\n") for i in history]
    for i in data:
        i.append(i[2])
        i.append("\n".join(i[1].split("\n\n")))
        i[2] = i[2].split("; ")
        i[1] = i[1].split("\n\n")
    if request.method == 'GET':
        return render_template('ed_story.html', photo=Photo(), photos=Files(), history=data, story=data[index],
                               len=len(a), length=len(data), index=index)
    elif request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        images = request.form.get('images')
        if title != '':
            stories = information_extractor("history.txt")
            stories[index] = "\n/\n".join([title.strip(), text.strip(), images.strip()])
            print(stories)
            file = open("static/text_data/history.txt", "w")
            contacts = "\n/*/\n".join(stories)
            file.write(contacts)
        return redirect(f"/ed_story/{index}")


@app.route('/add_block', methods=['POST', 'GET'])
def add_block():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    new_block = "\n/*/\nЗаголовок\n/\nТекст\n/\n"
    file = open("static/text_data/history.txt", "r").read()
    with open("static/text_data/history.txt", "w") as f:
        f.write(file + new_block)
    return redirect("/ed_story/0")

@app.route('/delete_block/<int:index>', methods=['POST', 'GET'])
def delete_block(index):
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    if index==0:
        return redirect("/ed_story/0")
    file = information_extractor("history.txt")
    del file[index]
    with open("static/text_data/history.txt", "w") as f:
        f.write("\n/*/\n".join(file))
    return redirect("/ed_story/0")


@app.route('/upload_file', methods=['POST', 'GET'])
def file_upload():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    global i
    if request.method == 'GET':
        return render_template('upload_file.html', )
    elif request.method == 'POST':
        f = request.files['file']
        x = f.__repr__()
        tmp = f.read()
        file_name = x[x.index("'") + 1:x.index("'", 15)]
        if not Files.query.filter_by(filename=file_name).all():
            n = open("static/img/user/" + file_name, "wb")
            n.write(tmp)
            n.close()
            photo = Files(filename=file_name)
            db.session.add(photo)
            db.session.commit()
        return redirect("/ed_title")


@app.route('/about')
def about():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    history = information_extractor("history.txt")
    data = [i.split("\n/\n") for i in history]
    for i in data:
        i.append(i[2])
        i[2] = i[2].split("; ")
        i[1] = i[1].split("\n\n")
    return render_template('about.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr), history=data)


@app.route('/popcorn')
def popcorn():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return render_template('popcorn.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr))


@app.route('/uprek')
def uprek():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return render_template('uprek.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr))


@app.route('/prelat')
def prelat():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return render_template('prelat.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr))


@app.route('/dakar')
def dakar():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return render_template('dakar.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr))


@app.route('/kreker')
def kreker():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return render_template('kreker.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr))


@app.route('/sale')
def sale():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return render_template('sale.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr))


@app.route('/news')
def news():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return render_template('news.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr))


@app.route('/runners')
def runners():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return render_template('runners.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr))


@app.route('/heavy')
def heavy():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return render_template('heavy.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr))


@app.route('/heavy_ex')
def heavy_ex():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return render_template('heavy_ex.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr))


@app.route('/stallions')
def stallions():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return render_template('stallions.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr))


@app.route('/mares')
def mares():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return render_template('mares.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr))


@app.route('/foals')
def foals():
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return render_template('foals.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr))


if __name__ == '__main__':
    app.run(debug=True)
'''port=8080, host='127.0.0.1'''
