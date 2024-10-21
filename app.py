from flask import Flask, render_template, redirect, make_response, request, session, url_for, abort
import json
import random
import urllib.request

# session
from flask_session import Session

# mail
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)

# session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

Session(app)

@app.route("/sitemap")
def sitemap():
    response = make_response(render_template('sitemap.xml', username='Alkobrosly'))
    response.headers['Content-type'] = 'text/xml; charset=utf-8'
    return response

@app.route("/manifest.json")
def webmanifest():
    
    manifest = {
        "name": "kobros-tech for cloud services & solutions",
        "short_name": "kobros-tech",
        "description": "Web application that enables our customers to easily inspect updates and offers in our website",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#000000",
        "icons": [
            {
                "src": "/static/images/favicon.ico",
                "sizes": "48x48"
            },
            {
                "src": "/static/images/android-chrome-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/images/android-chrome-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }

    body = json.dumps(manifest)
    response = make_response(body, [
        ('Content-Type', 'application/manifest+json'),
    ])

    return response


def _get_service_worker_content():
    """ Returns a ServiceWorker javascript file scoped for the backend (aka. '/')
    """
    with open('./static/js/service_worker.js') as f:
        body = f.read()
        
        return body

@app.route("/service-worker.js")
def service_worker():
    body = _get_service_worker_content()
    response = make_response(
        body, 
        [
            ("Content-Type", "text/javascript"),
            ("Service-Worker-Allowed", "/"),
        ]
    )

    return response
        

@app.route("/set/lang", )
@app.route("/set/lang/<lang>")
def set_language(lang):
    allowed_langs = ['en', 'fr', 'ar']
    data = {
            'lang': 'en',
        }
    
    if lang in allowed_langs:
        session['lang'] = lang
        data['lang'] = session['lang']
    else:
        session['lang'] = 'en'
        data['lang'] = session['lang']
    
    body = json.dumps(data)
    response = make_response(body, [
        ('Content-Type', 'application/json'),
    ])

    return response


@app.route("/get/lang")
def get_language():
    data = {}

    try:
        data['lang'] = session['lang']
    except KeyError:
        # data['lang'] = "en"
        session['lang'] = 'en'
        data['lang'] = session['lang']

    body = json.dumps(data)
    response = make_response(body, [
        ('Content-Type', 'application/json'),
    ])

    return response


@app.route("/")
def index():
     return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/subscribe/<email>")
def subscribe(email):
    # url = "https://web.kobros-tech.com/website_mass_mailing/subscribe"
    url = "http://localhost:8069/website_mass_mailing/subscribe"
    args = {
        'list_id': 1,
        'value': email,
        'subscription_type': "email",
    }

    data = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": args,
        "id": random.randint(0, 1000000000),
    }

    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type":"application/json",
    })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])

    body = json.dumps(reply["result"])
    response = make_response(body, [
        ('Content-Type', 'application/manifest+json'),
    ])
    return response


# Requires that "Less secure app access" be on
# https://support.google.com/accounts/answer/6010255
app.config["MAIL_DEFAULT_SENDER"] = "info@kobros-tech.com"
app.config["MAIL_PASSWORD"] = "Y9R#kT_.qiC.ZvJ"
app.config["MAIL_PORT"] = 465
app.config["MAIL_SERVER"] = "smtppro.zoho.com"
app.config["MAIL_USE_TLS"] = False
app.config['MAIL_USE_SSL'] = True
app.config["MAIL_USERNAME"] = "alkobroslymohamed@gmail.com"
mail = Mail(app)

@app.route('/json_post_form', methods=['POST'])
def json_post_form():
    # Get the JSON data from the request
    data = request.get_json()

    # current date and time
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y, %H:%M:%S")

    message_copy = ""

    if data['name']:
        message_copy = message_copy + f"Name: {data['name']}"
    
    if data['email']:
        message_copy = message_copy + f"\nEmail: {data['email']}"
    
    if data['phone']:
        message_copy = message_copy + f"\nPhone: {data['phone']}"

    if data['subject']:
        message_copy = message_copy + f"\nSubject: {data['subject']}"
    
    if data['message']:
        message_copy = message_copy + f"\nMessage: {data['message']}"

    message_copy = message_copy + f"\nDate and Time: {date_time}"
    notify_message = Message("Notification: Mohamed Alkobrosli", recipients=["info@kobros-tech.com"])
    notify_message.body = message_copy
    mail.send(notify_message)

    # Return a success message
    body = json.dumps({'result': "Message received successfully"})
    response = make_response(body, [
        ('Content-Type', 'application/manifest+json'),
    ])
    return response

# handle 404 error
@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('index'))

if __name__ == "__main__":
 app.run(debug=True,host="0.0.0.0")
