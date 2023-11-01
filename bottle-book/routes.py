from bottle import Bottle,\
    jinja2_template as template,\
        static_file, request, resirect
from bottle import response
from utils.session import Session
#from utils.auth import Auth

app = Bottle()
sess = Session()
app_sess = sess.create_session(app)

'''
画像、CSS,JS などのコンテンツは
これで処理する
'''

@app.get('/stati/<filePath:path>')
def static(filePath):
    return static_file(filePath, root='./static')
@app.route('/test')
def test():
    aaa = request.query.test
    return aaa