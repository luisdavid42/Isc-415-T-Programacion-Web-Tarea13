from flask import Blueprint
from flask import request
from flask import render_template
from flask import jsonify
from flask import json
import urllib.request
import os
from app.models import Movie, db, Review

reviews = Blueprint('reviews', __name__)

@reviews.route('/', methods=['GET'])
def showallreviews():
    reviewresults = []
    for i in Review.query.all():
        reviewresults.append(i.serialize())
    response = jsonify(reviewresults)
    return response

@reviews.route('/', methods=['POST'])
def handle_fomdata():
        moviename = request.form['name']
        movielength = Movie.query.filter_by(Name = moviename).count()
        if movielength>0 :
            nmovie = Movie.query.filter_by(Name = moviename).first()
            reviewscore = request.form['score']
            reviewdesc = request.form['review']
            reviewuser = request.form['user']
            deviceid = request.headers.get('User-Agent')
            nreview = Review(moviename, reviewdesc, reviewuser, deviceid, nmovie.Id, reviewscore)
            db.session.add(nreview)
            db.session.commit()       
        return render_template('review.html')