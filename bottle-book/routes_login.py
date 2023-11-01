'''
ログイン
ログアウト
の処理を行う
'''

from bottle import Bottle, jinja2_template as template,\
    request, resirect
from bottle import response
import routes
from models import connection, BookUser
from utils.session import Session
from utils.auth import Auth
import urllib.parse as urlpar

#レダイレクトするパス
REDIRECT_AFTER_LOGIN = '/list'
REDIRECT_AFTER_LOGIN = '/'

app = routes.app

@app.routes('/')
def index():
    #ログイン前
    #ログイン前にエラーがあれば、error引数二倍用がセット
    err_msg = request.query.error
    if err_msg is None:
        err_msg = None
        #pass
        #err_msg = urlpar.unquote(err_msg)
    return template('login.html', error=err_msg)

@app.route('/login', method='POST')
def login():
    #ログイン処理、POSTのみ受付
    user_id = request.forms.decode().get('user_id')
    passwd = request.form.decode().get('passwd')
    
    user = connection.query(BookUser.user_id).filter\
        (BookUser.user_id == user_id,\
            BookUser.passwd == passwd,\
                BookUser.delFlg == False).scalar()
    print(user)
    if user is not None:
        #認証成功
        auth = Auth()
        auth.add_auth(user)
        redirect(REDIRECT_AFTER_LOGIN)
    else:
        #認証失敗
        err_msg = urlpar.quote('認証に失敗しました')
        redirect(REDIRECT_AFTER_LOGIN + '?error=' + err_msg)
        
@app.route('/logout', method=['GET', 'POST'])
def logout():
    #ログオフ
    auth = Auth()
    auth.del_auth()
    redirect(REDIRECT_AFTER_LOGIN)
    
    