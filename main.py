from flask import Flask, render_template, redirect, request
app = Flask('app')

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/examples')
def examples():
  return render_template('examples.html')

@app.route('/documentation')
def documentation():
  return render_template('documentation.html')



@app.route('/projects/<variable>')
def to_do():
  pass

@app.route("/test")
def gitpage():
  return redirect('https://github.com/R0ck-1t/Group2_agile_project')

app.run(host='0.0.0.0', port=8080)




