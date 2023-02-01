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
from folium.plugins import MarkerCluster
from folium.plugins import Search
from PyPDF2 import PdfReader
from flask import Flask, render_template, url_for, request, abort
import stripe

app = Flask(__name__)

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51MUQGMSJjAhmPZHxvNE5dBZz7NB2m1log9ISyr4ftGSqDtIQki0FAbiSuJ7cIjjIu3CI7s9A57I1Z1YLSnOWdViF00hzorWvfm'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51MUQGMSJjAhmPZHxEMg3S2evX7xMaZPTUYyv3oxlxQsB6L92ONi852niJxf8IS9iw4puXPfGefiz4npx8XB4mas400U9BLD3rU'

stripe.api_key = app.config['STRIPE_SECRET_KEY']


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
        return redirect(url_for("student_login"))
    
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

       
        return redirect("http://127.0.0.1:5000/list/")
    
    # print(mongo.db)

    return render_template("student_login.html")


@app.route("/college_login/",methods=["POST","GET"])
def college_login():
    if request.method == "POST":
        email= request.form.get("logemail")
        password= request.form.get("logpassword")

        password1 = mongo.db.gallery.find_one({"email":email})
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

       
        return redirect(url_for("dashboard"))
    
    # print(mongo.db)

    return render_template("college_login.html")


@app.route("/gallery/")
def gallery():
    return render_template("gallery.html", gallery=mongo.db.gallery.find())


def findPage():
    reader = PdfReader('static/college.pdf')
        
    for i in range(0, len(reader.pages)):
            page = reader.pages[i]
            text = page.extract_text()
            print(cllg_mumid)
            print(text)
            if  cllg_mumid in text:
                return True
            
            
@app.route("/upload/",methods=["POST","GET"])
def upload():
    global cllg_mumid
    if request.method == "POST":
        cllg_email = request.form.get('email')
        cllg_mumid = request.form.get('cllg_mumid')
        cllg_pass = request.form.get('cllg_pass')
        image = request.files["image"]
        image2 = request.files["cimage"]
        image3 = request.files["limage"]
        image4 = request.files["caimage"]
        description = request.form.get("description")
        voice = request.form.get("voice")

        text1 = findPage()
        if text1 == True:
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
                        "email":cllg_email,
                        "password":cllg_pass,
                        "cllg_mumid":cllg_mumid,
                        "filename": filename,
                        "classroom": filename2,
                        "library": filename3,
                        "canteen": filename4,
                        "description": description.strip(),
                        "voice":voice.strip()
                    })
                    get_location()

                    flash("Successfully registered!", "success")
                    return redirect(url_for("college_login"))
                else:
                    flash("An error occurred while uploading the images!", "danger")
                    return redirect(url_for("upload"))
                
        else: 
            flash("Cllg not verified!", "danger")
            return redirect(url_for("upload"))
        
    # print(mongo.db)
        
    return render_template("upload.html")

@app.route("/map/")
def get_location_route():
    return render_template("Map.html")

def get_location():
    images = "static/uploads/"
    directory = os.fsencode(images)
    m = folium.Map( zoom_start = 100)
    marker_cluster = MarkerCluster().add_to(m)
    for i in os.listdir(directory):
        # print(i)
        img = PIL.Image.open(images+i.decode())
        # print(mongo.db.gallery)
        cllg = mongo.db.gallery.find_one({"filename":i.decode()})
        cllg_name=cllg['description']
        cllg_id = str(cllg['_id'])
        print(cllg_id)
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

        popup=generate_link(cllg_name,cllg_id, locname.address)
        folium.Marker([latitude, longitude], popup= popup,name = cllg_name, tooltip = "Click for virtual tour").add_to(m)
        
    # servicesearch = Search(
    #     layer=marker_cluster,
    #     search_label="name",
    #     placeholder='Search for a service',
    #     collapsed=False,
    # ).add_to(m)

    m.save('templates/Map.html')

@app.route("/list")
def json_data():
    
    return render_template("counsellors_list.html")

@app.route("/virtual_tour/<cllg>")
def virtual_tour(cllg):
    return render_template("virtual_tour.html")

def generate_link(cllgname,cllgid,cllgaddress):
    return "<a href=/virtual_tour/"+cllgid+">"+cllgname+","+cllgaddress+"</a>"


@app.route("/fetch_cllg")
def fetch_cllg():
    cursor = mongo.db.gallery.find()
    list_cur = list(cursor)
    # print(list_cur)
    return dumps(list_cur, indent = 2) 


@app.route("/dashboard")
def dashboard():
    return render_template("cllg_dashboard.html")

@app.route("/counsellor_signup")
def counsellor_signup():
    if request.method == "POST":
        name= request.form.get("stname")
        email= request.form.get("email")
        username= request.form.get("username")
        password= request.form.get("password")

        mongo.db.counsellors.insert_one({
            "name": name,
            "email": email,
            "username": username,
            "password": password
        })

        # print()

        flash("Successfully added student!", "success")
        return redirect(url_for("counsellor_signup"))
    

    return render_template("counsellor_signup.html")


@app.route('/stripe_pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1MUw0pSJjAhmPZHxRvwDIzVx',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'whsec_00181ceb50125d103e6a60d77da3331d2869b3ff56d59707b13c47a9d9e6add0'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}