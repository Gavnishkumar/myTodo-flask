from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
with app.app_context():
    db.create_all()
# defining schema
class ToDo(db.Model):
    sno= db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String(200),nullable=False)
    desc= db.Column(db.String(500),nullable=False)
    date_created= db.Column(db.DateTime,default= datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.title},{self.desc}"
@app.route('/',methods=["GET","POST"] )
def hello_world():
    if request.method=="POST":
        title=request.form.get("title")
        desc= request.form.get("desc")
        todo = ToDo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=ToDo.query.all()
    return render_template("index.html",allToDo = alltodo)
@app.route('/delete/<int:sno>')
def DeleteTask(sno):
    todo= ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>')
def Update(sno):
    toupdate= ToDo.query.filter_by(sno=sno).first()
    return render_template('update.html',toupdate=toupdate)
@app.route('/updateing/<int:sno>',methods=["GET","POST"])
def Updateing(sno):
    if request.method=="POST":
        toupdate= ToDo.query.filter_by(sno=sno).first()
        toupdate.title= request.form.get('title')
        toupdate.desc= request.form.get('description')
        db.session.commit()
    return redirect('/')
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False,port=8000)