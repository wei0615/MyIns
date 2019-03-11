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
            like= self.orm.count_likes(img)
            like_counts.append(like)

        self.render('index.html',imgs=imgs,like_counts=like_counts)


class PersonHandler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        user = self.orm.get_user()
        self.render('personcenter.html',user=user)

    def post(self, *args, **kwargs):
        username = self.get_argument('username', '')
        nickname = self.get_argument('nickname', '')
        user_imgs = self.request.files.get('user_img',None)

        if username and nickname and user_imgs:
            if user_imgs:
                for user_img in user_imgs:
                    img_save = ImageSave(self.settings['static_path'],user_img['filename'])
                    user_img_url = img_save.save_userimg(user_img['body'])

                    if self.current_user == username:
                        self.orm.change_userinfo(username,nickname,user_img_url)
                    self.redirect('/person')

class ExploreHandler(AuthBaseHandler):
    """
    Explore page, photo of other users.
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        imgs = self.orm.get_all_img()
        self.render('explore.html',imgs=imgs)


class PostHandler(AuthBaseHandler):
    """
    Single photo page, and maybe comments.
    """
    def get(self, post_id):
        likes_user_id = []
        img = self.orm.get_img_by(post_id)
        all_comments = self.orm.get_comment_by(post_id)
        likes = self.db_session.query(Like).filter_by(likeimg_id=post_id).all()

        for like in likes:
            user = self.db_session.query(User).filter_by(id=like.user_id).first()
            likes_user_id.append(user.username)

        if img:
            like_count = self.orm.count_likes(img)
            self.render('post.html', img=img,like_count=like_count,all_comments=all_comments,likes_user_id=likes_user_id)
        else:
            self.write("Don't have this picture!")


class CommentHandler(AuthBaseHandler):
    """
    评论功能
    """
    def post(self,post_id):
        comments = self.get_argument('comment','')
        if comments:
            self.orm.save_comments(post_id,comments)
            self.redirect('/post/%s' %post_id)
        else:
            self.redirect('/post/%s' % post_id)

class DelCommentHandler(AuthBaseHandler):
    """
    删除评论
    """
    def get(self):
        comment_id = self.get_argument("comment_id",None)
        # post_id = self.db_session.query(Comment).filter_by(id=comment_id).first()
        self.orm.del_comments(comment_id)

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
        describe =  self.get_argument('describe',None)
        img_id = 0
        if img_files and describe:
            for img in img_files:
                img_save = ImageSave(self.settings['static_path'],img['filename'])
                img_save.save_upload(img['body'])
                img_save.make_thumb()

                upload_img = self.orm.add_img(img_save.upload_url,img_save.thumb_url,describe)
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

class DelImgHandler(AuthBaseHandler):
    """
    删除用户上传图片
    """
    def get(self):
        img_id = self.get_argument('img_id',None)
        if img_id:
            self.orm.delete_img_from(img_id)
            # self.redirect('/profile')


class CollectionHandler(AuthBaseHandler):
    """
    收藏和取消喜欢的图片
    """
    def get(self):
        collect_id = self.get_argument("collect_id",None)
        self.orm.collect_img(collect_id)

    def post(self):
        collect_id = self.get_argument("collect_id",None)
        self.orm.cancel_clc_img(collect_id)
