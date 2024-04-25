from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, Email
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(max=120)], render_kw={"placeholder": "Email"})
    submit = SubmitField("Register")

def write_to_csv(email):
    with open('Pyemail.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email])

@app.route('/', methods=['GET', 'POST'])
def home():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        write_to_csv(email)
        return redirect(url_for('success'))
    return render_template('index.html', form=form)

@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == "__main__":
    app.run(debug=True)
