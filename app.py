from flask import Flask, render_template
from get_info import ArtsData

app = Flask(__name__)
bd = ArtsData()


@app.route("/")
def start():
    ret = render_template("start.html")
    return ret

@app.route("/museums/")
def museums():
    """Обрабатывает запрос к странице со списком музеев
       http://mipt-space-tis.ru:50XX/ """
    museums_list = bd.get_museums()
    ret = render_template("museums.html",museums_list=museums_list)
    return ret

@app.route("/<museum_id>")
def museum(museum_id=None):
    """Обрабатывает запрос к странице конретного музея
       http://mipt-space-tis.ru:5000/author """
    full_info_museum = bd.get_full_info_museum(museumId)
    museum_name = full_info_museum['museumName']
    museum_date_found = full_info_museum['foundDate']
    museum_city = full_info_museum['city']
    museum_country = full_info_museum['country']
    artworks = full_info_museum['artworks']
    ret = render_template("museum.html",museumName=museum_name,
    foundDate=museum_date_found, city=museum_city, country=museum_country, artworks=artworks)
    #ret ="<pre>" + str(museumName) +"\n" + str(countries) + "\n" + str(books) +
    "</pre>"
    return ret

@app.route("/people/")
def people():
    """Обрабатывает запрос к странице со списком авторов
       http://mipt-space-tis.ru:50XX/ """
    authors_list = bd.get_people()
    ret = render_template("people.html",authors_list=authors_list)
    return ret

@app.route("/people_id")
def person(people_id=None):
    """Обрабатывает запрос к странице конретного автора
       http://mipt-space-tis.ru:50XX/author """

    full_info_person = bd.get_full_info_person(people_id)
    name = full_info_person['name']
    birth = full_info_person['birthday']
    death = full_info_person['deathDate']
    countries = full_info_person['countries']
    artworks = full_info_person['artworks']
    ret = render_template("person.html",name=name,
birth=birth, death=death, countries=countries, artworks=artworks)
    #ret ="<pre>" + str(author_name) +"\n" + str(countries) + "\n" + str(books) +
    "</pre>"
    return ret

@app.route("/artworks")
def artworks():
    """Обрабатывает запрос к странице со списком авторов
       http://mipt-space-tis.ru:50XX/ """
    full_info_artworks = bd.get_full_info_artworks()
    artwork_list = []

    for i in range(len(full_info_artworks)):
        d = {}
        d['name'] = full_info_artworks[i][0]
        d['type'] = full_info_artworks[i][1]
        d['author'] = full_info_artworks[i][2]
        d['date_created'] = full_info_artworks[i][3]
        d['museum'] = full_info_artworks[i][4]
        artwork_list.append(d)
    ret = render_template("artworks.html",artwork_list=artwork_list)
    return ret

app.run(host='0.0.0.0',port=5005)
