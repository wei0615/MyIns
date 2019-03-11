import tornado.web
from .main import AuthBaseHandler
from utils.account import authenticate,register


class LoginHandler(AuthBaseHandler):
    """
    登录接口
    """
    def get(self,*args,**kwargs):
        next_url = self.get_argument('next','/')
        self.render("login.html",next_url=next_url)

    def post(self,*args,**kwargs):
        username = self.get_argument('username',None)
        password = self.get_argument('password',None)
        next_url = self.get_argument('next','/')


        logined = authenticate(username,password,self.db_session)
        if logined:
            self.session.set('tudo_user_info',username)
            self.redirect(next_url)
        else:
            self.redirect('/login')


class SignupHandler(AuthBaseHandler):
    def get(self,*args,**kwargs):
        self.render('login.html',msg='')

    def post(self,*args,**kwargs):
        username = self.get_argument('username','')
        nickname = self.get_argument('nickname','')
        password1 = self.get_argument('password1','')
        password2 = self.get_argument('password2','')

        if username and nickname and password1 and password2:
            if password1 == password2:
                ret = register(username,nickname,password1)
                if ret['msg'] == 'ok':
                    self.session.set('tudo_user_info',username)
                    self.redirect('/')
                else:
                    self.write(ret)
            else:
                self.write({'msg':'两次输入密码不匹配'})
        else:
            self.render('signup.html',msg={'register fail'})

class LogoutHandler(AuthBaseHandler):
    def get(self,*args,**kwargs):
        self.session.delete('tudo_user_info')
        self.redirect('/login')