from flask import Flask,render_template,url_for,redirect,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager,login_user,UserMixin

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mydatabase.db'
app.config['SECRET_KEY']='thisisasecretkey'
db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80), unique=True, nullable=False)
    email=db.Column(db.String,  nullable=False)
    password=db.Column(db.String, nullable=False)
    def __repr__(self):
       return '<User %r>' % self.username 

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
      id=request.form.get('id')
      username=request.form.get('ename')
      email=request.form.get('email')
      password=request.form.get('password')
      user=User(id=id,username=username,email=email,password=password)
      db.session.add(user)
      db.session.commit()
      flash('User has been registered successfully','success')
      return redirect(url_for('login'))

    return render_template('AddTeacher.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
      username=request.form.get('username')
      password=request.form.get('password')
      user=User.query.filter_by(username=username).first()
      if user and password==user.password:
        login_user(user)
        return redirect(url_for('/home'))
      else:
        flash('Invalid Credentials','warning')
        return redirect(url_for('UserLogin'))

    return render_template('UserLogin.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__=='__main__':
    app.run(debug=True)