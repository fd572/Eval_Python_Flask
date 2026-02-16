from flask import Flask, redirect, render_template, request, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "onePiece"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evenement.db'

db = SQLAlchemy(app)

class Evenement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    lieu = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.DateTime, default=db.func.current_timestamp())


    def __repr__(self):
       return f"Evenement {self.titre}, {self.type}, {self.date}, {self.lieu}, {self.description}, {self.date_creation}"

with app.app_context():
    db.create_all()



@app.route("/",methods=["GET"])
def index():
    evenements = Evenement.query.all()
    return render_template("index.html", evenements=evenements)


@app.route("/supprimer-evenement/<int:even_id>", methods=["POST"])
def supprimer_evenement(even_id): 
    even = Evenement.query.get(even_id)
    if even:
        db.session.delete(even)
        db.session.commit()
    flash("Événement supprimé avec succès!", "success")
    return redirect(url_for("index"))

@app.route("/formulaire",methods=["GET","POST"])
def formulaire():
    if request.method == "POST" :
        titre = request.form.get("titre").strip()
        type = request.form.get("type_evenement")
        date = request.form.get("date")
        lieu = request.form.get("lieu").strip()
        description = request.form.get("description").strip()

        has_errors = False
        
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date() 
        except ValueError:
            flash("Le format de la date est invalide. Le format attendu DD/MM/AAAA.", "error")
            has_errors = True

        if not titre:
            flash("Le titre est requis.", "error")
            has_errors = True
        if not type:
            flash("Le type d'événement est requis.", "error")
            has_errors = True
        if not date:
            flash("La date est requise.", "error")
            has_errors = True
        if not lieu:
            flash("Le lieu est requis.", "error")
            has_errors = True
        if not description:
            flash("La description de l'événement est requise.", "error")
            has_errors = True

        if has_errors:
            return redirect ("/formulaire")

        nouvel_evenement = Evenement(titre=titre, type=type, date=date, lieu=lieu, description=description)
        db.session.add(nouvel_evenement)
        db.session.commit()

        flash("Événement ajouté avec succès!", "success")
        return redirect("/")
    
    return render_template("formulaire.html")


@app.route("/evenement/<date_evenement>",methods=["GET"])
def afficher_evenement(date_evenement):
    date_choisie = datetime.strptime(date_evenement, "%Y-%m-%d").date()
    Evenement_entry = Evenement.query.filter(Evenement.date >= date_choisie).order_by(Evenement.date.asc()).limit(5).all()
    clean_db = []
    for e in Evenement_entry:
        clean_db.append({
        "id": e.id,
        "titre": e.titre,
        "type": e.type,
        "date": e.date,
        "lieu": e.lieu,
        "description": e.description,
        "date_creation": e.date_creation
        })

    return jsonify(
    {
      "evenements": clean_db
    }
  ), 200



if __name__ == "__main__":
    app.run(debug=True)