from flask import Flask, jsonify, request
from flaskext import mysql
import requests, json

app = Flask(__name__)

#homepage
@app.route('/')
def home():
    response = requests.get('https://www.theaudiodb.com/api/v1/json/123/searchalbum.php?s=daft_punk')           #pull data from audiodb
    if response.status_code == 200:                                                                             #check response is good
        data = response.json()                                                                                  #store data in var
        print(data['album'][00]['strAlbum']) #basically goes search_Result_Container/albumIndex/attributeName   #keepAsAlbum/int/whateverYouWish
    return data['album'][00]['strAlbum']

@app.route("/api/album/<albumid>")
def album_lookup(albumid):
    return jsonify({
        "idAlbum":"2130752",
        "strAlbum":"good kid, m.A.A.d city",
        "strArtist":"Kendrick Lamar",
        "albumArt":"https://r2.theaudiodb.com/images/media/album/thumb/good-kid-maad-city-507f66df92d44.jpg",
        "intYearReleased":"2012",
        "strGenre":"Hip-Hop",
        "avgRating":"4.23",
        "numReviews":"46071",
        "tracklist":[
            "Sherane a.k.a. Master Splinter's Daughter",
            "Bitch, Don't Kill My Vibe",
            "Backseat Freestyle",
            "The Art of Peer Pressure",
            "Money Trees",
            "Poetic Justice",
            "good kid",
            "m.A.A.d city",
            "Swimming Pools (Drank) (extended version)",
            "Sing About Me, I'm Dying of Thirst",
            "Real",
            "Compton",
            "The Recipe",
            "Black Boy Fly",
            "Now or Never"
        ]})

@app.route("/api/album/<albumid>/reviews")
def albums_reviews(albumid):
    limit = request.args.get('limit')
    limit = int(limit) if limit != None else 5

    cursor = sql.get_db().cursor()
    cursor.execute("SELECT Account.ID, Account.Name, Review.timestamp, Review.Score, Review.Liked, Review.Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes FROM Review JOIN Account ON Account.ID = Review.AccountID WHERE AlbumID=%s ORDER BY Likes DESC LIMIT %s;", (albumid, limit))
    results = cursor.fetchall()
    cursor.close()

    return jsonify({
        "reviews":[{"id":x[0], "name":x[1], "timestamp":x[2], "score":x[3], "liked":x[4], "content":x[5], "numLikes":x[6], "userliked":False, "userreport":False} for x in results]
    })

@app.route("/api/user/<userid>")
def user_lookup(userid):
    cursor = sql.get_db().cursor()
    cursor.execute("SELECT * FROM Account WHERE ID=%s LIMIT 1;",  str(userid))
    user = cursor.fetchone()
    cursor.execute("SELECT Review.AlbumID, Review.timestamp, Review.Score, Review.Liked, Review.Content, (SELECT COUNT(*) FROM Tags WHERE Tags.ReviewAccountID = Review.AccountID AND Tags.ReviewAlbumID = Review.AlbumID AND Tags.info & 128) AS Likes FROM Review JOIN Account ON Account.ID = Review.AccountID WHERE Review.AccountID=%s ORDER BY Review.timestamp DESC LIMIT 5;", (userid))
    reviews = cursor.fetchall()
    cursor.close()
    
    return jsonify({
        "id":user[0],
        "name":user[1],
        "bio":user[5],
        "reviews":[{"albumid":x[0], "timestamp":x[1], "score":x[2], "liked":x[3], "content":x[4], "numLikes":x[5], "userliked":False, "userflagged":False} for x in reviews]
    })

@app.route("/api/albums")
def album_search():
    return jsonify({
        "albums":[
            {"id":"2130752", "strAlbum":"good kid, m.A.A.d city", "strArtist":"Kendrick Lamar", "albumArt":"https://r2.theaudiodb.com/images/media/album/thumb/good-kid-maad-city-507f66df92d44.jpg", "intYearReleased":"2012", "avgRating":"4.23","numReviews":"46071"},
            {"id":"2130752", "strAlbum":"good kid, m.A.A.d city", "strArtist":"Kendrick Lamar", "albumArt":"https://r2.theaudiodb.com/images/media/album/thumb/good-kid-maad-city-507f66df92d44.jpg", "intYearReleased":"2012", "avgRating":"4.23","numReviews":"46071"},
            {"id":"2130752", "strAlbum":"good kid, m.A.A.d city", "strArtist":"Kendrick Lamar", "albumArt":"https://r2.theaudiodb.com/images/media/album/thumb/good-kid-maad-city-507f66df92d44.jpg", "intYearReleased":"2012", "avgRating":"4.23","numReviews":"46071"},
            {"id":"2130752", "strAlbum":"good kid, m.A.A.d city", "strArtist":"Kendrick Lamar", "albumArt":"https://r2.theaudiodb.com/images/media/album/thumb/good-kid-maad-city-507f66df92d44.jpg", "intYearReleased":"2012", "avgRating":"4.23","numReviews":"46071"},
            {"id":"2130752", "strAlbum":"good kid, m.A.A.d city", "strArtist":"Kendrick Lamar", "albumArt":"https://r2.theaudiodb.com/images/media/album/thumb/good-kid-maad-city-507f66df92d44.jpg", "intYearReleased":"2012", "avgRating":"4.23","numReviews":"46071"}   
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)