import logging
import os

from flask import Flask, render_template, request, redirect, url_for
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

from flask_sslify import SSLify

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.debug("Welcome to Docker Guestbook")


SQLALCHEMY_DATABASE_URI = \
    '{engine}://{username}:{password}@{hostname}/{database}'.format(
        engine='mysql+pymysql',
        username=os.getenv('DB_ENV_MYSQL_USER'),
        password=os.getenv('DB_ENV_MYSQL_PASSWORD'),
        hostname=os.getenv('DB_PORT_3306_TCP_ADDR'),
        database=os.getenv('DB_ENV_MYSQL_DATABASE'))


app = Flask(__name__)
app.debug = False
sslify = SSLify(app)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    logger.debug(request.method + " index")
    if request.method == 'POST':
        name = request.form['name']
        guest = Guest(name=name)
        db.session.add(guest)
        db.session.commit()
        return redirect(url_for('index'))

    #return render_template('index.html', guests=Guest.query.all())
    return "Hello There! <br> <script>(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');  ga('create', 'UA-18747469-1', 'auto');  ga('send', 'pageview');</script>"


class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return "[Guest: id={}, name={}]".format(self.id, self.name)


@manager.command
def create_db():
    logger.debug("create_db")
    app.config['SQLALCHEMY_ECHO'] = True
    db.create_all()

@manager.command
def create_dummy_data():
    logger.debug("create_test_data")
    app.config['SQLALCHEMY_ECHO'] = True
    guest = Guest(name='Steve')
    db.session.add(guest)
    db.session.commit()

@manager.command
def drop_db():
    logger.debug("drop_db")
    app.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()


if __name__ == '__main__':
    manager.run()
