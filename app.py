from flask import *
from flask_bootstrap import Bootstrap
import os
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
import folium
import PIL.Image
import PIL.ExifTags
from geopy.geocoders import Nominatim
from cryptography.fernet import Fernet
from bson.json_util import dumps
import pyttsx3

app = Flask(__name__)
Bootstrap(app)
key = Fernet.generate_key()
fernet = Fernet(key)

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

        # encMessage = fernet.encrypt(password.encode())

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

        # print()

        flash("Successfully added student!", "success")
        return redirect(url_for("student_signup"))
    
    # print(mongo.db)

    return render_template("student_signup.html")

@app.route("/student_login/",methods=["POST","GET"])
def student_login():
    if request.method == "POST":
        username= request.form.get("logusername")
        password= request.form.get("logpassword")

        password1 = mongo.db.students.find_one({"username":username})
        if password1:
            password2 = password1['password']
            
            # decMessage = fernet.decrypt(password2.decode())

            if password2 == password:
                flash("Successfully Logged In!", "success")

        else: 
            flash("Username or password invalid!","danger")


        # print(mongo.db.students.insert_one({
        #     "name": name,
        #     "email": email,
        #     "username": username,
        #     "password": password
        # }))

       
        # print()

       
        return redirect(url_for("student_login"))
    
    # print(mongo.db)

    return render_template("student_login.html")


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
        voice = request.form.get("voice")
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
                "description": description.strip(),
                "voice":voice.strip()
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

@app.route("/list")
def json_data():
    cursor = mongo.db.counsellors.find()
    list_cur = list(cursor)
    # print(list_cur)
    json_data = dumps(list_cur, indent = 2) 
    with open('data.json', 'w') as file:
        file.write(json_data)
    return render_template("counsellors_list.html")


def text_to_speech(text, gender):
    """
    Function to convert text to speech
    :param text: text
    :param gender: gender
    :return: None
    """
    voice_dict = {'Male': 0, 'Female': 1}
    code = voice_dict[gender]

    engine = pyttsx3.init()

    # Setting up voice rate
    engine.setProperty('rate', 125)

    # Setting up volume level  between 0 and 1
    engine.setProperty('volume', 0.8)

    # Change voices: 0 for male and 1 for female
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[code].id)

    engine.say(text)
    engine.runAndWait()

text = 'Hello ! My name is Siddhesh.'
gender = 'Male'  # Voice assistant 
@app.route("/virtual_tour")
def virtual_tour():
    # text = mongo.db.gallery.find_one()

    text_to_speech(text, gender)
    return render_template("virtual_tour.html")