from flask import Flask , render_template
from db_lib import museums_data
 
app = Flask(__name__)
bd = museums_data()
 
@app.route("/")
def museums_artworks():
    ret = render_template("start.html")
    return ret
@app.route("/museums")
def museums():
    museums_list = bd.get_museums()
    ret = render_template("museums.html", museums_list = museums_list)
    return ret
@app.route("/museum/<museum_id>")
def museum(museum_id =None):
    museum_name = bd.get_museum_name(museum_id)
    artworks = bd.get_artworks_museum(museum_id)
    country = bd.get_country(museum_id)
    city = bd.get_museum_city(museum_id)
    date_of_found = bd.get_museum_date_of_found(museum_id)
    ret = render_template("museum.html",museum_name = museum_name, artworks = artworks,country= country, city=city, date_of_found = date_of_found)
    return ret
@app.route("/artists")
def artists():
    artists_list = bd.get_people()
    ret = render_template("artists.html", artists_list = artists_list)
    return ret
@app.route("/artist/<artist_id>")
def artist(artist_id=None):
    artist_name = bd.get_name_people(artist_id)
    countries = bd.get_country_people(artist_id)
    artworks = bd.get_artworks_people(artist_id)
    ret = render_template("artist.html", artist_name = artist_name, countries = countries, artworks = artworks)
    return ret
@app.route("/artworks")
def artworks():
    artists_list = bd.get_people()
    ret = render_template("artists.html", artists_list = artists_list)
#     artworks_list = bd.get_artworks()
#     ret = render_template("artworks.html", artworks_list = artworks_list)
    return ret
app.run(host = '0.0.0.0', port = 5005)
