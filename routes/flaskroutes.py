from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap
from src.loginform import LoginForm
from src.regform import RegisterForm


def configure_routes(app):


    @app.route('/')
    def home():
        return redirect('/login', code=200)

    @app.route('/submissions')
    def examples():
        return render_template('user_submissions.html')

    @app.route('/account')
    def documentation():
        return render_template('account.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # form = LoginForm()
        return render_template('login.html', code=200)



    @app.route('/projects/<variable>')
    def to_do():
        pass

    @app.route("/test")
    def gitpage():
        return redirect('https://github.com/informationvulture/Group2_agile_project/')

    app.run(host='0.0.0.0', port=8080)
