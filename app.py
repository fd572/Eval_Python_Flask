from flask import Flask, redirect, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "onePiece"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    lieu = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.DateTime, default=db.func.current_timestamp())


    def __repr__(self):
       return f"Database {self.titre}, {self.type}, {self.date}, {self.lieu}, {self.description}, {self.date_creation}"

with app.app_context():
    db.create_all()

@app.route("/index",methods=["GET"])
def accueil():
    database_entry = Database.query.filter(Database.date >= datetime.now()).order_by(Database.date.asc()).limit(5).all()
    clean_db = []
    for d in database_entry:
        clean_db.append({
        "id": d.id,
        "titre": d.titre,
        "type": d.type,
        "date": d.date,
        "lieu": d.lieu,
        "description": d.description,
        "date_creation": d.date_creation
        })

    return jsonify(
    {
      "database": clean_db
    }
  ), 200

@app.route("/",methods=["POST"])
def accueil_remove():
    
    flash("Merci pour votre message !")
    return redirect(url_for("accueil"))

@app.route("/formulaire",methods=["GET","POST"])
def formulaire():
    if request.method == "POST" :
        titre = request.form.get("titre").strip()
        type = request.form.get("type").strip()
        date = request.form.get("date").strip()
        lieu = request.form.get("lieu").strip()
        description = request.form.get("description").strip()
    return render_template("formulaire.html")

if __name__ == "__main__":
    app.run(debug=True)