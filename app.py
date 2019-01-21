import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from handlers import main,auth,chat,service



define('port', default='8000', help='Listening port', type=int)

class MainHandler(tornado.web.Application):
    pass

#路由。。
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', main.IndexHandler),
            ('/explore', main.ExploreHandler),
            ('/post/(?P<post_id>[0-9]+)', main.PostHandler),
            ('/upload', main.UploadHandler),
            ('/profile', main.ProfileHandler),
            ('/login',auth.LoginHandler),
            ('/signup',auth.SignupHandler),
            ('/logout',auth.LogoutHandler),
            ('/room',chat.RoomHandler),
            ('/ws',chat.ChatSocketHandler),

            #同步与异步测试url https://source.unsplash.com/random
            ('/sync',service.SyncUrlHandler),
            ('/aync',service.AsynUrlHandler),

        ]
        settings = dict(
            debug=True,
            template_path='templates',
            static_path='static',
            login_url='/login',
            cookie_secret='sdjfalkfjlajl48039815',
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    'port': 6379,
                    # 'password': '',
                    'db_sessions': 5,  # redis db index
                    'db_notifications': 11,
                    'max_connections': 2 ** 30,
                },
                'cookies': {
                    'expires_days': None,
                },
            }
        )

        super(Application, self).__init__(handlers, **settings)


application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    print("Server start on port {}".format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()

