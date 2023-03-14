from flask import Flask ,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.cli import with_appcontext

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    S_No=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(200), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.S_No} - {self.title}"


@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['description']
        todo= Todo(title=title ,description=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    return render_template('index.html' , altd=alltodo)

@app.route('/cars')
def cars():
    return "<button onclick=\"alert(\'Clicked\')\"><h3>SUVs are my favourite</h3></button>"

@app.route('/Update/<int:S_No>', methods=['GET','POST'])
def Update(S_No):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['description']
        td=Todo.query.filter_by(S_No=S_No).first()
        td.title=title
        td.description=desc
        db.session.add(td)
        db.session.commit()
        return redirect("/")

    td=Todo.query.filter_by(S_No=S_No).first()
    return render_template('Update.html' ,todo=td)

@app.route('/Delete/<int:S_No>')
def Delete(S_No):
    td=Todo.query.filter_by(S_No=S_No).first()
    db.session.delete(td)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True ,port=8000)