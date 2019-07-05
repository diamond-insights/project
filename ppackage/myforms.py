"""This module contains the classes for my web from"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired

class ContactForm(FlaskForm):
    name = StringField("Name ", validators=[DataRequired(message="Name cannot have special characters")])
    email = StringField("Email ", validators=[Email(message="Email address is invalid or not entered correctly")])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField("Email ", validators=[Email(message="Email address is invalid or not entered correctly")])
    pwd = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class Usersignup(FlaskForm):
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpeg','jpg','png'], '.jpg, .png, .jpeg Images Only!')])
    firstname = StringField("Firstname ", validators=[DataRequired()])
    lastname = StringField("Lastname ", validators=[DataRequired()])
    email = StringField("Email ", validators=[Email(message="Email address is invalid or not entered correctly")])
    pwd = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class Payment(FlaskForm):
    custname = StringField("Customer Fullname: ", validators=[DataRequired(message='Pls fill this field')])
    email = StringField("Email: ", validators=[DataRequired(message='Pls fill this field'),Email()])
    phone = StringField("Phone: ", validators=[DataRequired(message='Pls fill this field')])
    submit = SubmitField("Confirm Payment")