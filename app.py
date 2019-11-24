from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def root():
  return render_template('index.html')

@app.route('/app.js')
def js():
  url_for('static', filename='app.js')

@app.route('/buses')
def buses():
  return render_template('buses.json')

@app.route('/shape')
def shape():
  return render_template('shape.json')

@app.route('/trips')
def trips():
  return render_template('trips.json')

@app.route('/stops.json')
def stops():
  return render_template('stops.json')

@app.route('/index.css')
def css():
  return render_template('index.css')

@app.route('/test')
def test():
  return 'test'
