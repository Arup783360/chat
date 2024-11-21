from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)

# Database Models
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(20), nullable=False)
    receiver = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(255), nullable=False)

# Predefined Users
users = {
    "arup": "sarkar",
    "tol": "mandal"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/chat")
        else:
            return render_template("index.html", error="Incorrect username or password")
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" not in session:
        return redirect("/")
    user = session["user"]
    partner = "tol" if user == "arup" else "arup"

    if request.method == "POST":
        message = request.form["message"]
        new_message = Message(sender=user, receiver=partner, content=message)
        db.session.add(new_message)
        db.session.commit()

    messages = Message.query.filter(
        (Message.sender == user) & (Message.receiver == partner) |
        (Message.sender == partner) & (Message.receiver == user)
    ).all()
    return render_template("chat.html", user=user, partner=partner, messages=messages)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the database and tables are created
    app.run(debug=True)
