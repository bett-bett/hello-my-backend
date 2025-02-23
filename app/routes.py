from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
  user = {'username': 'Bryan'}
  items = [
      {
          'topic': {'title': 'css and js in flask'},
          'body': 'css and js are usually in the static folder, unless configured otherwise'
      },
      {
          'topic': {'title': 'flask'},
          'body': 'Flask is nice and easy to get ideas up and running'
      }
  ]
  return render_template('index.html', title='Home', user=user, items=items)

@app.route('/about')
def about():
    return render_template('index.html', content='Flask web app.')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)