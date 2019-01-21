from datetime import datetime
import tornado.web
import tornado.gen
import tornado.httpclient
import requests
import tornado.escape

from handlers.chat import ChatSocketHandler,make_chat
from utils.photo import ImageSave
from utils.account import add_img
from .main import AuthBaseHandler



class AsynUrlHandler(AuthBaseHandler):
    """
    异步保存图片
    """
    # @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self,*args,**kwargs):
        resp = yield self.fetch_image()

        if not resp.body:
            self.write('empty data')

        img_saver = ImageSave(self.settings['static_path'], 'x.jpg')
        img_saver.save_upload(resp.body)
        img_saver.make_thumb()

        user = self.get_argument('user','')
        is_from_room = self.get_argument('from','') == 'room'
        if user and is_from_room:
            img = add_img(user, img_saver.upload_url, img_saver.thumb_url)
            chat = make_chat("{} post:http://192.168.253.128:8000/post/{}".format(user,img.id), img_saver.thumb_url)
            chat['html'] = tornado.escape.to_basestring(
                self.render_string('message.html', message=chat)
            )

            ChatSocketHandler.update_cache(chat)
            ChatSocketHandler.send_message(chat)
        else:
            self.write("No User")


    @tornado.gen.coroutine
    def fetch_image(self):
        url = self.get_argument('url','')
        client = tornado.httpclient.AsyncHTTPClient()
        resp = yield client.fetch(url)
        return resp


class SyncUrlHandler(AuthBaseHandler):
    """
    同步保存图片
    """
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        # python 3.6以后无法使用httpClient,同步使用requests
        # client = tornado.httpclient.HTTPClient()
        # resp = client.fetch(url)

        url = self.get_argument('url','')
        resp = requests.get(url)

        img_saver = ImageSave(self.settings['static_path'],'x.jpg')
        img_saver.save_upload(resp.content)
        img_saver.make_thumb()
        img = add_img(self.current_user,img_saver.upload_url,img_saver.thumb_url)

        self.redirect('/post/{}'.format(img.id))