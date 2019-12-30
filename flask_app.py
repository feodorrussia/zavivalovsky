# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

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
    n = int(Data.query.filter_by(name='stallions').first().descr)
    stallions = []
    for i in range(4):
        name = Data.query.filter_by(name=f'stallion{i}').first().descr
        ind = Data.query.filter_by(name=name).first().descr
        stallions.append(ind)
    return render_template('index.html', photo=Photo(), data=Data(), stallions=stallions,
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr)[0].split("\n"),
                           num=[str(i) for i in range(n)])


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


@app.route('/ed_stallion/<int:index>', methods=['POST', 'GET'])
def ed_stallion(index):
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    lenght = len(a)
    n = int(Data.query.filter_by(name='stallions').first().descr)
    if request.method == 'GET':
        return render_template('ed_stallion.html', photo=Photo(), data=Data(), len=lenght, photos=Files(),
                               ln_st=n, index=str(index), num=[str(i) for i in range(n)])
    elif request.method == 'POST':
        filename = request.form.get('background')
        name = request.form.get('name')
        if filename != '' and Files.query.filter_by(filename=filename).all():
            photo = Photo.query.filter_by(descr=f"stallion{index}").first()
            photo.filename = filename
            db.session.commit()
        if name != '':
            inf = Data.query.filter_by(name=f"stallion{index}").first()
            inf.descr = name
            db.session.commit()
        return redirect(f"/ed_stallion/{index}")


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


@app.route('/ed_block_news', methods=['POST', 'GET'])
def ed_block_news():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    lenght = len(a)
    if request.method == 'GET':
        return render_template('ed_block_news.html', photo=Photo(), data=Data(), len=lenght, photos=Files())
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
        return render_template('ed_block_news.html', photo=Photo(), data=Data(), len=lenght, photos=Files())


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
    contacts = information_extractor("contacts.txt")
    staff = [[x.split("\n") for x in i.split("\n/\n")] for i in contacts[1:]]
    if request.method == 'GET':
        return render_template('ed_contacts.html', photo=Photo(), data=Data(), len=lenght, photos=Files(),
                               contacts=contacts[0], staff=staff, length=len(staff),
                               num=[str(i) for i in range(len(staff))])
    elif request.method == 'POST':
        text = request.form.get('contacts')
        if text != '':
            file = information_extractor("contacts.txt")
            file[0] = "\n".join(text.split("\r\n"))
            open(f"static/text_data/contacts{divider}.txt", "w").write("\n/*/\n".join(file))
        return redirect("/ed_contacts")


@app.route('/ed_staff/<int:index>', methods=['POST', 'GET'])
def ed_staff(index):
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    lenght = len(a)
    contacts = information_extractor("contacts.txt")
    staff = [[x.split("\n") for x in i.split("\n/\n")] for i in contacts[1:]]
    if request.method == 'GET':
        return render_template('ed_staff.html', index=index, photo=Photo(), data=Data(), len=lenght, photos=Files(),
                               contacts=contacts[index + 1].split("\n/\n"), staff=staff, length=len(staff),
                               num=[str(i) for i in range(len(staff))])
    elif request.method == 'POST':
        image = request.form.get('image')
        text = request.form.get('contacts')
        if text != '':
            file = information_extractor("contacts.txt")
            file[index+1] = image + "\n/\n" + "\n".join(text.split("\r\n"))
            open(f"static/text_data/contacts{divider}.txt", "w").write("\n/*/\n".join(file))
        return redirect(f"/ed_staff/{index}")


@app.route('/add_person', methods=['POST', 'GET'])
def add_person():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    new_block = '\n/*/\ntrainer.jpg\n/\nДолжность\nИ.О.Ф\nТелефон: +7 (***) ***-**-**\n/\n'
    with open(f"static/text_data/contacts{divider}.txt", "a") as f:
        f.write(new_block)
    return redirect("/ed_staff/0")


@app.route('/delete_person/<int:index>', methods=['POST', 'GET'])
def delete_person(index):
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    if index == 0:
        return redirect("/ed_staff/0")
    file = information_extractor("contacts.txt")
    del file[index+1]
    with open(f"static/text_data/contacts{divider}.txt", "w") as f:
        f.write("\n/*/\n".join(file))
    return redirect("/ed_staff/0")


@app.route('/ed_story/<int:index>', methods=['POST', 'GET'])
def ed_story(index):
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    history = information_extractor(f"history.txt")
    data = [i.split("\n/\n") for i in history]
    for i in data:
        i.append(i[2])
        i.append("\n".join(i[1].split("\n\n")))
        i[2] = i[2].split("; ")
        i[1] = i[1].split("\n\n")
    if request.method == 'GET':
        return render_template('ed_story.html', photo=Photo(), data=Data(), photos=Files(), history=data,
                               story=data[index],
                               len=len(a), length=len(data), index=index)
    elif request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        images = request.form.get('images')
        if title != '':
            stories = information_extractor(f"history.txt")
            stories[index] = "\n/\n".join([title.strip(), text.strip(), images.strip()])
            file = open(f"static/text_data/history{divider}.txt", "w")
            contacts = "\n/*/\n".join(stories)
            file.write(contacts)
        return redirect(f"/ed_story/{index}")


@app.route('/add_block', methods=['POST', 'GET'])
def add_block():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    new_block = "\n/*/\nЗаголовок\n/\nТекст\n/\n"
    with open(f"static/text_data/history{divider}.txt", "a") as f:
        f.write(new_block)
    return redirect("/ed_story/0")


@app.route('/delete_block/<int:index>', methods=['POST', 'GET'])
def delete_block(index):
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    if index == 0:
        return redirect("/ed_story/0")
    file = information_extractor("history.txt")
    del file[index]
    with open(f"static/text_data/history{divider}.txt", "w") as f:
        f.write("\n/*/\n".join(file))
    return redirect("/ed_story/0")


@app.route('/ed_news/<int:index>', methods=['POST', 'GET'])
def ed_news(index):
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    history = information_extractor("news.txt")
    data = [i.split("\n/\n") for i in history]
    for i in data:
        i.append(i[2])
        i.append("\n".join(i[1].split("\n\n")))
        i[2] = i[2].split("; ")
        i[1] = i[1].split("\n\n")
    if request.method == 'GET':
        return render_template('ed_news.html', photo=Photo(), data=Data(), photos=Files(), history=data,
                               story=data[index],
                               len=len(a), length=len(data), index=index)
    elif request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        images = request.form.get('images')
        if title != '':
            stories = information_extractor("news.txt")
            stories[index] = "\n/\n".join([title.strip(), text.strip(), images.strip()])
            file = open(f"static/text_data/news{divider}.txt", "w")
            contacts = "\n/*/\n".join(stories)
            file.write(contacts)
        return redirect(f"/ed_news/{index}")


@app.route('/add_news_block', methods=['POST', 'GET'])
def add_news_block():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    new_block = "\n/*/\nЗаголовок\n/\nТекст\n/\ndefault.png"
    with open(f"static/text_data/news{divider}.txt", "a") as f:
        f.write(new_block)
    return redirect("/ed_news/0")


@app.route('/delete_news_block/<int:index>', methods=['POST', 'GET'])
def delete_news_block(index):
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    if index == 0:
        return redirect("/ed_news/0")
    file = information_extractor("news.txt")
    del file[index]
    with open(f"static/text_data/news{divider}.txt", "w") as f:
        f.write("\n/*/\n".join(file))
    return redirect("/ed_news/0")


@app.route('/ed_sale', methods=['POST', 'GET'])
def ed_sale():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    lenght = len(a)
    if request.method == 'GET':
        return render_template('ed_sale.html', photo=Photo(), data=Data(), len=lenght, photos=Files(),
                               text=open(f"static/text_data/sale{divider}.txt", "r").read())
    elif request.method == 'POST':
        filename = request.form.get('background')
        descr = request.form.get('text')
        if filename != '' and Files.query.filter_by(filename=filename).all():
            photo = Photo.query.filter_by(descr="sale").first()
            photo.filename = filename
            db.session.commit()
        if descr != '':
            file = open(f"static/text_data/sale{divider}.txt", "w")
            file.write(descr)
        return redirect("/ed_sale")


@app.route('/ed_catalog/<breed>', methods=['POST', 'GET'])
def ed_catalog(breed):
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    history = information_extractor(f"{breed[:-1]}.txt")
    data = [i.split("\n/\n") for i in history]
    for i in data:
        i.append(i[2])
        i.append("\n".join(i[1].split("\n\n")))
        i[2] = i[2].split("; ")
        i[1] = i[1].split("\n")
    if request.method == 'GET':
        return render_template('ed_catalog.html', photo=Photo(), data=Data(), photos=Files(), stallions=data,
                               stallion=data[int(breed[-1])],
                               len=len(a), length=len(data), breed=breed)
    elif request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        images = request.form.get('images')
        if title != '':
            stories = information_extractor(f"{breed[:-1]}.txt")
            horse = Data.query.filter_by(descr=breed).first()
            if horse:
                horse.name = title.strip()
            else:
                horse = Data(name=title.strip().upper(), descr=breed)
                db.session.add(horse)
            db.session.commit()
            stories[int(breed[-1])] = "\n/\n".join([title.strip(), text.strip(), images.strip()])
            file = open(f"static/text_data/{breed[:-1]}{divider}.txt", "w")
            contacts = "\n/*/\n".join(stories)
            file.write(contacts)
        return redirect(f"/ed_catalog/{breed}")


@app.route('/ed_price_catalog/<breed>', methods=['POST', 'GET'])
def ed_price_catalog(breed):
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    history = information_extractor(f"{breed[:-1]}.txt")
    data = [i.split("\n/\n") for i in history]
    for i in data:
        i.append(i[2])
        i.append("\n".join(i[1].split("\n")[:-1]))
        i[2] = i[2].split("; ")
        i[1] = i[1].split("\n")
    if request.method == 'GET':
        return render_template('ed_price_catalog.html', photo=Photo(), data=Data(), photos=Files(), stallions=data,
                               stallion=data[int(breed[-1])],
                               len=len(a), length=len(data), breed=breed)
    elif request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text') + "\n" + request.form.get('price')
        text = "\n".join(text.split("\r\n"))
        images = request.form.get('images')
        if title != '':
            stories = information_extractor(f"{breed[:-1]}.txt")
            horse = Data.query.filter_by(descr=breed).first()
            if horse:
                horse.name = title.strip().upper()
            else:
                horse = Data(name=title.strip().upper(), descr=breed)
                db.session.add(horse)
            db.session.commit()
            stories[int(breed[-1])] = "\n/\n".join([title.strip(), text.strip(), images.strip()])
            file = open(f"static/text_data/{breed[:-1]}{divider}.txt", "w")
            contacts = "\n/*/\n".join(stories)
            file.write(contacts)
        return redirect(f"/ed_price_catalog/{breed}")


@app.route('/add_horse/<breed>', methods=['POST', 'GET'])
def add_horse(breed):
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    new_block = "\n/*/\nКличка\n/\nДанные\nЦена\n/\npopcorn1.png"
    file = open(f"static/text_data/{breed[:-2]}{divider}.txt", "r").read()
    with open(f"static/text_data/{breed[:-2]}{divider}.txt", "a") as f:
        f.write(new_block)
    inf = Data(name="КЛИЧКА", descr=breed[:-1] + str(len(file.split("\n/*/\n"))))
    db.session.add(inf)
    db.session.commit()
    if breed[-1] == "p":
        return redirect(f"/ed_price_catalog/{breed[:-2]}0")
    else:
        return redirect(f"/ed_catalog/{breed[:-2]}0")


@app.route('/delete_horse/<breed>', methods=['POST', 'GET'])
def delete_horse(breed):
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    if index == 0:
        return redirect(f"/ed_catalog/{breed[:-2]}0")
    file = information_extractor(f"{breed[:-2]}.txt")
    del file[int(breed[-2])]
    inf = Data.query.filter_by(descr=breed[:-2]).first()
    db.session.delete(inf)
    for i in file[int(breed[-2]):]:
        n = Data.query.filter_by(name=i.split("\n/\n")[0].upper()).first().descr
        Data.query.filter_by(name=i.split("\n/\n")[0].upper()).first().descr = n[:-1] + str(int(n[-1]) - 1)
    db.session.commit()
    with open(f"static/text_data/{breed[:-2]}{divider}.txt", "w") as f:
        f.write("\n/*/\n".join(file))
    if breed[-1] == "p":
        return redirect(f"/ed_price_catalog/{breed[:-2]}0")
    else:
        return redirect(f"/ed_catalog/{breed[:-2]}0")


@app.route('/upload_file', methods=['POST', 'GET'])
def file_upload():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
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


@app.route('/delete_file', methods=['POST', 'GET'])
def delete_file():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    a = Files.query.all()
    lenght = len(a)
    if request.method == 'GET':
        return render_template('delete_file.html', len=lenght, photos=Files())
    elif request.method == 'POST':
        filename = request.form.get('filename')
        if Files.query.filter_by(filename=filename).all():
            photo = Files.query.filter_by(filename=filename).first()
            db.session.delete(photo)
            db.session.commit()
            os.remove(f"static/img/user/{filename}")
        return redirect("/ed_title")


@app.route('/exit')
def f_exit():
    if Admin.query.filter_by(id=0).first().status != 1:
        return redirect("/login")
    Admin.query.filter_by(id=0).first().status = 0
    db.session.commit()
    return redirect("/index")


@app.route('/about')
def about():
    history = information_extractor("history.txt")
    data = [i.split("\n/\n") for i in history]
    for i in data:
        i.append(i[2])
        i[2] = i[2].split("; ")
        i[1] = i[1].split("\n\n")
    return render_template('about.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr)[0].split("\n"),
                           history=data)


@app.route('/stallion/<breed>')
def stallion(breed):
    file = information_extractor(breed[:-1] + ".txt")
    file = file[int(breed[-1])].split("\n/\n")
    file[1] = file[1].split("\n")
    file[2] = file[2].split("; ")
    contacts = information_extractor("contacts.txt")
    staff = [[x.split("\n") for x in i.split("\n/\n")] for i in contacts[1:]]
    return render_template('stallion.html', stallion=file, staff=staff,
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr)[0].split("\n"))


@app.route('/sale')
def sale():
    return render_template('sale.html', photo=Photo(), text=open(f"static/text_data/sale{divider}.txt", "r").read(),
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr)[0].split("\n"))


@app.route('/news')
def news():
    history = information_extractor("news.txt")
    data = [i.split("\n/\n") for i in history]
    for i in data:
        i.append(i[2])
        i[2] = i[2].split("; ")
        i[1] = i[1].split("\n\n")
    return render_template('news.html',
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr)[0].split("\n"),
                           history=data)


@app.route('/price_catalog/<breed>')
def price_catalog(breed):
    horses = information_extractor(f"{breed}.txt")
    data = [i.split("\n/\n") for i in horses]
    for i in data:
        i[2] = i[2].split("; ")
        i[1] = i[1].split("\n")
    return render_template('price_catalog.html', horses=data, length=len(horses), breed=breed,
                           num=[str(i) for i in range(len(horses))],
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr)[0].split("\n"))


@app.route('/catalog/<breed>')
def catalog(breed):
    horses = information_extractor(f"{breed}.txt")
    data = [i.split("\n/\n") for i in horses]
    for i in data:
        i[2] = i[2].split("; ")
        i[1] = i[1].split("\n")
    return render_template('catalog.html', horses=data,
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr)[0].split("\n"))


if __name__ == '__main__':
    app.run(debug=True)
'''port=8080, host='127.0.0.1'''
