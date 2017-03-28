from flask import Blueprint
from flask import request
from flask import render_template
from flask import jsonify
from flask import json
import urllib.request
import os
from app.models import Movie, db

movies = Blueprint('movies', __name__)

@movies.route('/', methods=['GET'])
def showallmovies():
    movieresults = []
    for i in Movie.query.all():
        movieresults.append(i.serialize())
    response = jsonify(movieresults)
    return response

@movies.route('/search', methods=['GET'])
def findmoviebyName():
    moviename = request.args.get('name')
    movieresults = Movie.query.filter(Movie.Name.startswith(moviename)).count()
    if movieresults>0:
        movie = Movie.query.filter(Movie.Name.startswith(moviename)).first()
        response = jsonify(movie.serialize())
        return response
    else:
        return render_template('review.html'), 404

@movies.route('/', methods=['POST'])
def handle_fomdata():
        moviename = request.form['name']
        movielength = Movie.query.filter_by(Name = moviename).count()
        if movielength==0 :
            moviedesc = request.form['desc']
            movieposter = request.form['poster']
            try:
                f = open('app/static/poster/' + moviename + '.jpg','wb')
                with urllib.request.urlopen(movieposter) as url:
                    s = url.read()
                f.write(s)
                f.close()
                dbmovieposter = '/poster/' + moviename + '.jpg'
            except:
                dbmovieposter = ""            
            nmovie = Movie(moviename, moviedesc, dbmovieposter)
            db.session.add(nmovie)
            db.session.commit()
     
        return "success"