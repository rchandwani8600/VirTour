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
app.config["UPLOAD_FOLDER"] = "static/uploads/"
app.config["CLASSROOM_FOLDER"] = "static/classroom/"
app.config["LIBRARY_FOLDER"] = "static/library/"
app.config["CANTEEN_FOLDER"] = "static/canteen/"
app.config["MONGO_DBNAME"] = "gallery"
app.config["MONGO_URI"] = "mongodb://localhost:27017/gallery"

mongo = PyMongo(app)
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/student_signup/",methods=["POST","GET"])
def student_signup():
    if request.method == "POST":
        name= request.form.get("stname")
        email= request.form.get("email")
        username= request.form.get("username")
        password= request.form.get("password")

        # print(mongo.db.students.insert_one({
        #     "name": name,
        #     "email": email,
        #     "username": username,
        #     "password": password
        # }))

        mongo.db.students.insert_one({
            "name": name,
            "email": email,
            "username": username,
            "password": password
        })

        flash("Successfully added student!", "success")
        return redirect(url_for("student_signup"))
    
    # print(mongo.db)

    return render_template("student_signup.html")


@app.route("/gallery/")
def gallery():
    return render_template("gallery.html", gallery=mongo.db.gallery.find())


@app.route("/upload/",methods=["POST","GET"])
def upload():
    if request.method == "POST":
        image = request.files["image"]
        image2 = request.files["cimage"]
        image3 = request.files["limage"]
        image4 = request.files["caimage"]
        description = request.form.get("description")
        if image and image2 and image3 and image4 and description and image.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS and image2.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS and image3.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS and image4.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            filename = secure_filename(image.filename)
            filename2 = secure_filename(image2.filename)
            filename3 = secure_filename(image3.filename)
            filename4 = secure_filename(image4.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image2.save(os.path.join(app.config["CLASSROOM_FOLDER"], filename2))
            image3.save(os.path.join(app.config["LIBRARY_FOLDER"], filename3))
            image4.save(os.path.join(app.config["CANTEEN_FOLDER"], filename4))

            mongo.db.gallery.insert_one({
                "filename": filename,
                "classroom": filename2,
                "library": filename3,
                "canteen": filename4,
                "description": description.strip()
            })
            get_location()

            flash("Successfully uploaded images to gallery!", "success")
            return redirect(url_for("upload"))
        else:
            flash("An error occurred while uploading the images!", "danger")
            return redirect(url_for("upload"))
    
    # print(mongo.db)
        
    return render_template("upload.html")

@app.route("/map")
def get_location_route():

    return render_template("Map.html")

def get_location():
    images = "static/uploads/"
    directory = os.fsencode(images)
    m = folium.Map( zoom_start = 100)
    for i in os.listdir(directory):
        # print(i)
        img = PIL.Image.open(images+i.decode())
        # print(mongo.db.gallery)
        cllg = mongo.db.gallery.find_one({"filename":i.decode()})
        cllg_name=cllg['description']
        exif = {PIL.ExifTags.TAGS[k]:v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
            }
    # print(exif)
    # print(exif['GPSInfo'])

        north = exif['GPSInfo'][2]
        east = exif['GPSInfo'][4]
        # print(north)
        # print(east)

        latitude = ((((north[0]*60)+north[1])*60)+north[2])/60/60
        longitude = ((((east[0]*60)+east[1])*60)+east[2])/60/60
        latitude = float(latitude)
        longitude = float(longitude)
        # print(latitude)
        # print(longitude)

        geoloc = Nominatim(user_agent="GetLoc")
        locname = geoloc.reverse(f"{latitude}, {longitude}")

        
        folium.Marker([latitude, longitude], popup= cllg_name+ ","+locname.address, tooltip = "Click for virtual tour").add_to(m)
    m.save('templates/Map.html')