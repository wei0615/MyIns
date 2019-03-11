import hashlib
from model.account import User,Img,session,Like,Comment

def hashed(pwd):
    """
    将密码生成对应的hash值
    :param pwd:
    :return:
    """
    hash_pwd = hashlib.md5(pwd.encode('utf8')).hexdigest()
    return hash_pwd

def authenticate(username,password,db_session):
    """
    校验用户密码
    :param username:
    :param password:
    :return:
    """
    if username and password:
        db_password = User.get_pass(username,db_session)

        judged = (hashed(password) == db_password)
        return judged
    else:
        return False

def register(username,nickname,password):
    """
    注册用户
    :param username:
    :param nickname:
    :param password:
    :return:
    """
    if User.is_exists(username):
        return {'msg':'username is exists'}

    hash_pass = hashed(password)
    User.add_user(username,nickname,hash_pass)
    return {'msg':'ok'}

#数据库操作工具类
class ORMHandler:
    def __init__(self,db_session,username):
        self.db = db_session
        self.user = username

    def get_user(self):
        user = self.db.query(User).filter_by(username=self.user).first()
        return user

    def change_userinfo(self,username,nickname,user_img):
        """
        完善用户信息
        :param nickname:
        :param username:
        :param password:
        :param user_img:
        :return:
        """
        user = self.get_user()
        user_info = self.db.query(User).filter_by(username=username).first()
        if user.username == username:
            user_info.nickname = nickname
            user_info.user_img = user_img
            self.db.commit()


    def add_img(self, image_url, thumb_url,describe):
        """
        保存用户上传的图片信息
        :return:
        """
        user = self.get_user()
        save_img = Img(image_url=image_url, thumb_url=thumb_url, user=user,describe=describe)
        self.db.add(save_img)
        self.db.commit()
        return save_img

    def get_all_img(self):
        """
        获取所有图片
        :return:
        """
        imgs = self.db.query(Img).order_by(Img.upload_time.desc()).all()
        return imgs

    def get_img_from(self):
        """
        根据用户获取用户上传的图片
        :param username:
        :return:
        """
        user = self.get_user()
        if user:
            imgs = self.db.query(Img).filter_by(user_id=user.id).order_by(Img.upload_time.desc()).all()
            return imgs
        else:
            return []

    def delete_img_from(self,img_id):
        """
        删除用户自己上传的图片
        :return:
        """
        img = self.db.query(Img).filter_by(id=img_id).first()
        self.db.delete(img)
        self.db.commit()


    def get_img_by(self,post_id):
        """
        获取具体的图片信息
        :param post_id:
        :return:
        """
        img = self.db.query(Img).filter_by(id=post_id).first()
        return img


    def get_like_imgs(self,user):
        """
        获取用户喜欢的图片
        :param user:
        :return:
        """
        # user = self.db.query(Like).filter_by(user_id = username).all()
        like_imgs = self.db.query(Img).filter(Like.user_id == user.id, Img.id == Like.likeimg_id,
                                              Img.user_id != user.id).all()
        return like_imgs

    def collect_img(self,img_id):
        """
        收藏喜欢的图片
        :param img_id:
        :return:
        """
        user = self.get_user()
        if user:
            like_img = Like(user_id=user.id,likeimg_id=img_id)
            self.db.add(like_img)
            self.db.commit()

    def cancel_clc_img(self,img_id):
        """
        取消收藏喜欢的图片
        :param img_id:
        :return:
        """
        user = self.get_user()
        if user:
            cancel_img = self.db.query(Like).filter_by(likeimg_id=img_id,user_id=user.id).first()
            self.db.delete(cancel_img)
            self.db.commit()


    def count_likes(self,img):
        """
        获取图片的受喜欢的数
        :param img:
        :return:
        """
        counts = self.db.query(Like).filter_by(likeimg_id=img.id).count()
        return counts

    def get_comment_by(self,post_id):
        """
        获取图片相关评论
        :param post_id:
        :return:
        """
        comments = self.db.query(Comment).filter_by(img_id=post_id).all()
        return comments

    def save_comments(self,post_id,comments):
        """
        保存用户评论
        :param post_id:
        :return:
        """
        user = self.get_user()
        save_comment = Comment(img_id=post_id,user_id=user.id,comments=comments)
        self.db.add(save_comment)
        self.db.commit()

    def del_comments(self,comment_id):
        """
        删除用户评论
        :param comment_id:
        :return:
        """
        del_comment = self.db.query(Comment).filter_by(id=comment_id).first()
        self.db.delete(del_comment)
        self.db.commit()




















































def add_img(username,image_url,thumb_url):
    """
    保存用户上传的图片信息
    :return:
    """
    user = session.query(User).filter_by(username=username).first()
    save_img = Img(image_url=image_url,thumb_url=thumb_url,user=user)
    session.add(save_img)
    session.commit()
    return save_img

def get_all_img():
    """
    获取所有图片
    :return:
    """
    imgs = session.query(Img).order_by(Img.upload_time.desc()).all()
    return imgs

def get_img_from(username):
    """
    根据用户获取用户上传的图片
    :param username:
    :return:
    """
    user = session.query(User).filter_by(username=username).first()
    if user:
        return user.imgs
    else:
        return []

def get_img_by(post_id):
    """
    获取具体的图片信息
    :param post_id:
    :return:
    """
    img = session.query(Img).filter_by(id=post_id).first()
    return img

def get_user(username):
    user = session.query(User).filter_by(username=username).first()
    return user

def get_like_imgs(user):
    """
    获取用户喜欢的图片
    :param user:
    :return:
    """
    # user = session.query(Like).filter_by(user_id = username).all()
    like_imgs = session.query(Img).filter(Like.user_id==user.id,Img.id==Like.likeimg_id,Img.user_id!=user.id).all()
    return like_imgs

def count_likes(img):
    """
    获取图片的受喜欢的数
    :param img:
    :return:
    """
    counts = session.query(Like).filter_by(likeimg_id = img.id).count()
    return counts

def get_comment_by(post_id):
    """
    获取图片相关评论
    :param post_id:
    :return:
    """
    comments = session.query(Comment).filter_by(img_id = post_id).all()
    return comments