import os
import glob
from PIL import Image
import uuid

class ImageSave(object):
    """
    辅助保存用户图片信息，生成缩略图
    """
    userimg_dir = 'user_img'
    upload_dir = 'upload'
    thumb_dir = 'thumbs'
    size = (200,200)

    def __init__(self,static_path,name):
        self.static_path = static_path
        self.old_name = name
        self.new_name = self.get_new_name()

    def get_new_name(self):
        """
        使用uuid生成唯一的图片名
        :return:
        """
        _,ext = os.path.splitext(self.old_name)
        return uuid.uuid4().hex + ext

    @property
    def upload_url(self):
        return os.path.join(self.upload_dir,self.new_name)

    @property
    def upload_path(self):
        return os.path.join(self.static_path,self.upload_url)

    def save_upload(self,content):
        print("图片地址%s" %self.upload_path)
        with open(self.upload_path,'wb') as f:
            f.write(content)

    def save_userimg(self,content):
        userimg_url = os.path.join(self.userimg_dir,self.new_name)
        userimg_path = os.path.join(self.static_path,userimg_url)

        with open(userimg_path,'wb') as f:
            f.write(content)
        return userimg_url

    @property
    def thumb_url(self):
        filename,ext = os.path.splitext(self.new_name)
        thumb_name = '{}_{}x{}{}'.format(filename,*self.size,ext)
        thumb_url = os.path.join(self.upload_dir,self.thumb_dir,thumb_name)
        return thumb_url

    def make_thumb(self):
        im = Image.open(self.upload_path)
        im.thumbnail(self.size)
        save_thumb_to = os.path.join(self.static_path, self.thumb_url)
        im.save(save_thumb_to, 'JPEG')


#旧方法
# def get_images(path):
#     """
#     获取static目录下 path 目录里的所有图片
#     :param path:
#     :return:
#     """
#     os.chdir('static')
#     names = glob.glob('upload/thumbs/*.jpg'.format(path))
#     os.chdir('..')
#     return names

# def make_thumb(path):
#     im = Image.open(path)
#     size = (200,200)
#     im.thumbnail(size)
#     dirname = os.path.dirname(path)
#     filename = os.path.basename(path)
#     file, ext = os.path.splitext(filename)
#     save_thumb_to = os.path.join(dirname, 'thumbs','{}_{}x{}{}'.format(file,*size,ext))
#     im.save(save_thumb_to, 'JPEG')
#     # print(save_thumb_to)
#     return save_thumb_to