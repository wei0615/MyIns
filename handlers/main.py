import tornado.web
from utils.photo import ImageSave
from pycket.session import SessionMixin
from utils.account import *
import os
from model.db import DBSession

class AuthBaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user_info')

    def prepare(self):
        self.db_session = DBSession()
        self.orm = ORMHandler(self.db_session,self.current_user)

    def on_finish(self):
        self.db_session.close()

class IndexHandler(AuthBaseHandler):
    """
    Home page for user, photo feeds of follow.
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        imgs = self.orm.get_img_from()
        like_counts = []
        for img in imgs:
            like= count_likes(img)
            like_counts.append(like)

        self.render('index.html',imgs=imgs,like_counts=like_counts)


class ExploreHandler(AuthBaseHandler):
    """
    Explore page, photo of other users.
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        imgs = self.orm.get_all_img()
        self.render('explore.html',imgs=imgs)


class  PostHandler(AuthBaseHandler):
    """
    Single photo page, and maybe comments.
    """
    def get(self, post_id):
        img = self.orm.get_img_by(post_id)
        all_comments = self.orm.get_comment_by(post_id)
        if img:
            like_count = self.orm.count_likes(img)
            self.render('post.html', img=img,like_count=like_count,all_comments=all_comments)
        else:
            self.write("Don't have this picture!")

    def post(self, *args, **kwargs):

        pass

class UploadHandler(AuthBaseHandler):
    '''
    处理上传图片的文件，保存到硬盘
    '''
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        self.render('upload.html')

    @tornado.web.authenticated
    def post(self,*args,**kwargs):
        img_files = self.request.files.get("newimg",None)
        img_id = 0
        if img_files:
            for img in img_files:
                img_save = ImageSave(self.settings['static_path'],img['filename'])
                img_save.save_upload(img['body'])
                img_save.make_thumb()

                upload_img = self.orm.add_img(img_save.upload_url,img_save.thumb_url)
                img_id = upload_img.id
            self.redirect('/post/%s' %img_id)
        else:
            self.write("请选择图片！！！")

class ProfileHandler(AuthBaseHandler):
    """
    显示用户上传的图片和喜欢的图片列表
    """
    def get(self,*args,**kwargs):
        username = self.get_argument('username',None)
        if not username:
            username = self.current_user
        self.orm.username = username
        user = self.orm.get_user()
        like_imgs = self.orm.get_like_imgs(user)
        self.render('profile.html',user=user,like_imgs=like_imgs)
