from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from client.client import Client
import time
import threading

app = Flask(__name__)
app.secret_key = "dev"

NAME_KEY = "name"
client = None
messages = []

def disconnect():
    global client
    if client is not None:
        client.disconnect()
        client = None

@app.route('/login', methods=["POST", "GET"])
def login():
    disconnect()
    if request.method == "POST":
        session[NAME_KEY] = request.form["name"]
        flash({"login": True, "name": session[NAME_KEY]})
        return redirect(url_for("home"))
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop(NAME_KEY, None)
    flash({"login": False})
    return redirect(url_for("login"))

@app.route('/')
@app.route('/home')
def home():
    global client
    if NAME_KEY not in session:
        return redirect(url_for("login"))
    name = session[NAME_KEY]
    client = Client(name)
    return render_template('index.html')

@app.route("/run", methods=['POST'])
def run():
    data = request.json.get('data')
    global client
    if client is not None:
        client.send_message(data)
    return "done"

@app.route("/get_messages")
def get_messages():
    global messages
    messages_copy = messages[:]
    return jsonify({"messages": messages_copy})

def update_messages():
    global messages
    run = True
    while run:
        try:
            time.sleep(0.1)
            if not client:
                continue
            new_messages = client.get_messages()
            messages.extend(new_messages)
            for msg in new_messages:
                print(msg)
                if msg == "{quit}":
                    run = False
                    break
        except Exception as e:
            print(e)

if __name__ == "__main__":
    threading.Thread(target=update_messages, daemon=True).start()
    app.run(debug=True , host="0.0.0.0")
