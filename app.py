from flask import Flask,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager,login_required,logout_user,current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='thisisasecretkey'

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="Login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(40), nullable=False,unique=True)
    password=db.Column(db.String(40), nullable=False)


class RegisterForm(FlaskForm):
    username=StringField(validators=[InputRequired(),length(
min=4, max=20)],render_kw={"placeholder":"Username"})   

password=StringField(validators=[InputRequired(),length(
min=4, max=20)],render_kw={"placeholder":"Password"}) 

submit=SubmitField("Register")

class LoginForm(FlaskForm):
 username=StringField(validators=[InputRequired(),length(
min=4, max=20)],render_kw={"placeholder":"Username"})   

password=StringField(validators=[InputRequired(),length(
min=4, max=20)],render_kw={"placeholder":"Password"}) 

submit=SubmitField("Login")

def validate_username(self,username):
    existing_user_username=User.query.filter_by(
    username=username.data).first()

    if existing_user_username:
        raise ValidationError(
       "That username already exists. Please choose a different one.")

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    form=RegisterForm()

    if form.validate_on_submit():
      hashed_password=bcrypt.generate_password_hash(form.password.data)
      new_user=User(username=form.username.data, password=hashed_password)
      db.session.add(new_user)
      db.session.commit()
      return redirect(url_for('login'))

    return render_template('userregister.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    return render_template('UserLogin.html',form=form)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__=='__main__':
    app.run(debug=True)