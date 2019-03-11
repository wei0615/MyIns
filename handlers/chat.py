import uuid
import tornado.web
import tornado.websocket
import tornado.httpclient
from tornado.ioloop import IOLoop

from .main import AuthBaseHandler
import tornado.escape
from pycket.session import SessionMixin



def make_chat(msg,img_url=None):
    """
    格式化message.html 的 dict
    :param msg:
    :param img_url:
    :return:
    """
    ret = {
        'id':str(uuid.uuid4()),
        'body': msg,
        'img_url':img_url,
    }
    return ret


class RoomHandler(AuthBaseHandler):
    """
    聊天界面
    """
    def get(self,*args,**kwargs):
        self.render('room.html',messages=ChatSocketHandler.cache)

class ChatSocketHandler(tornado.websocket.WebSocketHandler,SessionMixin):
    """
    处理响应的websocket连接
    """
    waiters = set()
    cache = []
    cache_size = 200

    def get_current_user(self):
        return self.session.get('tudo_user_info')

    def open(self, *args, **kwargs):
        print("new connection:%s" %self)
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        print("close connection:%s" %self)
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls,message):
        cls.cache.append(message)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size]

    @classmethod
    def send_message(cls,message):
        for waiter in cls.waiters:
            waiter.write_message(message)

    def on_message(self, message):
        print("got message:%s" %message)
        paresd = tornado.escape.json_decode(message)
        if paresd['body'] and paresd['body'].startswith('http://') or paresd['body'].startswith('https://'):
            url = paresd['body']
            client = tornado.httpclient.AsyncHTTPClient()
            save_api_url = 'http://39.108.160.235:8000/aync?url={}&user={}&from=room'.format(url,self.current_user)
            IOLoop.current().spawn_callback(client.fetch,save_api_url)

            chat = make_chat("user {},url({}) is processing".format(self.current_user,url))
            chat['html'] = tornado.escape.to_basestring(
                self.render_string('message.html', message=chat)
            )
            self.write_message(chat)
        else:
            chat = make_chat(("[{}]:{}").format(self.current_user, paresd['body']))
            chat['html'] = tornado.escape.to_basestring(
                self.render_string('message.html',message=chat)
            )

            ChatSocketHandler.update_cache(chat)
            ChatSocketHandler.send_message(chat)