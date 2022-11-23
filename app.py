from flask import Flask,render_template
from markupsafe import escape
from flask import url_for
name = 'CHEN Ziang'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]



app = Flask(__name__)
@app.route("/")
# def hello():
#     return "<h1>My First Flask!</h1><br><h4>欢迎来到我的Watchlist!</h4>"
# @app.route("/<name>")
# def user_page(name):
#     return f'User: {escape(name)}'
# @app.route("/test")
# def test_url_for():
#     print(url_for("hello"))
#     print(url_for("user_page",name = "chenziang"))
#     return "Test page"
def index():
    return render_template("index.html",name = name,movies = movies)
