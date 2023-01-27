from flask import *
from flask_bootstrap import Bootstrap
import os
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
import folium
import PIL.Image
import PIL.ExifTags
from geopy.geocoders import Nominatim

app = Flask(__name__)
Bootstrap(app)

app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["MONGO_DBNAME"] = "students"
app.config["MONGO_URI"] = "mongodb://localhost:27017/gallery"

mongo = PyMongo(app)

def upload():
    if request.method == "POST":
        name= request.form.get("stname")
        email= request.form.get("email")
        username= request.form.get("username")
        password= request.form.get("password")

        print(mongo.db.students)

        mongo.db.students.insert_one
        ({
            "name": name.strip(),
            "email": email.strip(),
            "username": username.strip(),
            "password": password.strip()
        })

        flash("Successfully added student!", "success")
        return redirect(url_for("student_signup"))
    
    # print(mongo.db)
