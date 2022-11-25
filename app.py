from flask import Flask,render_template
from markupsafe import escape
from flask import url_for,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
import click
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(app.root_path,'data.db')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20))
class Movies(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

@app.cli.command()
@click.option('--drop',is_flag = True,help = "Create after drop")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    db.create_all()
    name = "CHEN Ziang"
    movies =  [
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
    user  = User(name = name)
    db.session.add(user)
    for m in movies:
        Movie = Movies(title=m['title'],year=m['year'])
        db.session.add(Movie)
    db.session.commit()
    click.echo('Done.')

# flash存消息进session，存进cookie，设置密钥
app.config['SECRET_KEY'] = 'dev'

@app.context_processor
def inject_user():
    user = User.query.first().name
    return dict(user = user)

# 1. 主页路由
@app.route("/",methods = ['GET','POST']) # 识别post和get请求
def index():   
    if request.method == "POST":     # 判断是否post请求
        title = request.form["title"]
        year = request.form["year"]
        # 数据验证，flash返回消息，需要设置签名密钥
        if not title or not year or len(year)!=4 or len(title)>60:
            flash('Invalid input.')
            return redirect(url_for('index'))
        # 数据入库
        movie = Movies(title = title,year = year)
        db.session.add(movie)
        db.session.commit()
        flash('item created')
        return redirect(url_for('index'))
    # 渲染jinjia2模板
    movie = Movies.query.all()
    return render_template("index.html",movies = movie)

# 2. 编辑条目路由
@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
# 查询post过来的movie，提取表单中的title和year，并更新到数据库中
def edit(movie_id):
    movie = Movies.query.get_or_404(movie_id)
    if request.method == "POST":
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year)!=4 or len(title)>60:
            flash('Invalid input.')
            return redirect(url_for('edit',movie_id = movie_id))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item Updated.')

        return redirect(url_for('index'))
    return render_template('edit.html',movie = movie)
# 3. 删除条目路由
@app.route("/movie/delete/<int:movie_id>",methods = ["POST"])
def delete(movie_id):
    movie = Movies.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Item deleted.")
    return redirect(url_for('index'))
    



# 404 路由
@app.errorhandler(404)
def page_not_found(e):  # 异常对象为参数
    return render_template('404.html'),404


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


