from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
  user = {'username': 'bryan'}
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
