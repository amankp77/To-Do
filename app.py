from flask import Flask , render_template , redirect , request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TODO(db.Model):
    srno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(40) , nullable = False)
    desc = db.Column(db.String(200) , nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.now)
    def __repr__(self) -> str:
        return f"{self.srno} {self.title} {self.desc}"

@app.route("/" , methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        todo = TODO(title=title , desc=desc )
        db.session.add(todo)
        db.session.commit()
        redirect("/")
    todos = TODO.query.all()
    return render_template("index.html" , todos = todos)

@app.route("/delete/<int:n>")
def Deletetodo(n):
    todo = TODO.query.filter_by(srno=n).first()
    db.session.delete(todo)
    db.session.commit()
    
    return redirect("/")

@app.route("/update/<int:n>" , methods=["GET", "POST"])
def updatetodo(n):
     if request.method == "POST":
       todo = TODO.query.filter_by(srno=n).first()
       todo.title = request.form.get("title")
       todo.desc = request.form.get("desc")
       db.session.add(todo)
       db.session.commit()
       return redirect("/")
     todo = TODO.query.filter_by(srno=n).first() 
     return render_template("update.html" , todo=todo )

@app.route("/indexhomepage" , methods=["GET", "POST"])
def about():
    return render_template("indexhomepage.html")
@app.route("/contact" , methods=["GET", "POST"])
def contact():
    return render_template("contact.html")

@app.route("/deleteall")
def deleteall():
    srnos = TODO.query.all()
    for i in srnos:
      db.session.delete(i)
      db.session.commit()
    return redirect("/")

@app.route("login")
def login():
    pass

if __name__ == "__main__":
    app.run(debug=True)