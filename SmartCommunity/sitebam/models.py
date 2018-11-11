#coding:utf-8
from django.db import models

# Create your models here.
class SiteUser(models.Model):
    account = models.CharField(default='', max_length=255)
    pwd = models.CharField(default='', max_length=255)

class Metadata(models.Model):
    fno = models.CharField(default='', max_length=255)
    fname = models.CharField(default='', max_length=255)
    no = models.CharField(default='', max_length=255)
    name = models.CharField(default='', max_length=255)
    note = models.CharField(default='', max_length=255)

    def get_info(self):
        return {
            'id': self.id,
            'fno': self.fno,
            'fname': self.fname,
            'no' : self.no,
            'name' : self.name,
            'note' : self.note
        }

    def set_info(self, dct_info):
        self.fno = dct_info.get('fno') if 'fno' in dct_info else self.fno
        self.fname = dct_info.get('fname') if 'fname' in dct_info else self.fname
        self.no = dct_info.get('no') if 'no' in dct_info else self.no
        self.name = dct_info.get('name') if 'name' in dct_info else self.name
        self.note = dct_info.get('note') if 'note' in dct_info else self.note

class Community(models.Model):
    province = models.CharField(default='', max_length=255)#省
    city = models.CharField(default='', max_length=255)#市
    property_name = models.CharField(default='', max_length=255)#物业名称
    property_manager = models.CharField(default='', max_length=255)#物业负责人
    property_tel = models.CharField(default='', max_length=255)#物业电话
    community_name = models.CharField(default='', max_length=255)#小区名称
    community_addr = models.CharField(default='', max_length=255)#小区地址
    community_manager = models.CharField(default='', max_length=255)#小区管理员
    community_manager_tel = models.CharField(default='', max_length=255)#小区管理员电话
    community_start_time = models.CharField(default='', max_length=255)#小区上线时间
    community_home_num = models.CharField(default='', max_length=255)#业主数量
    community_account = models.CharField(default='', max_length=255)#小区注册账号
    community_pwd = models.CharField(default='', max_length=255)#小区密码
    reg_time = models.CharField(default='', max_length=255)#添加注册时间

    def get_info(self):
        return {
            'id': self.id,
            'province': self.province,
            'city': self.city,
            'property_name': self.property_name,
            'property_manager' : self.property_manager,
            'property_tel' : self.property_tel,
            'community_name' : self.community_name,
            'community_addr' : self.community_addr,
            'community_manager' : self.community_manager,
            'community_manager_tel' : self.community_manager_tel,
            'community_start_time' : self.community_start_time,
            'community_home_num' : self.community_home_num,
            'community_account' : self.community_account,
            'community_pwd' : self.community_pwd,
            'reg_time' : self.reg_time,
        }

    def set_info(self, dct_info):
        self.province = dct_info.get('province') if 'province' in dct_info else self.province
        self.city = dct_info.get('city') if 'city' in dct_info else self.city
        self.property_name = dct_info.get('property_name') if 'property_name' in dct_info else self.property_name
        self.property_manager = dct_info.get('property_manager') if 'property_manager' in dct_info else self.property_manager
        self.property_tel = dct_info.get('property_tel') if 'property_tel' in dct_info else self.property_tel
        self.community_name = dct_info.get('community_name') if 'community_name' in dct_info else self.community_name
        self.community_addr = dct_info.get('community_addr') if 'community_addr' in dct_info else self.community_addr
        self.community_manager = dct_info.get('community_manager') if 'community_manager' in dct_info else self.community_manager
        self.community_manager_tel = dct_info.get('community_manager_tel') if 'community_manager_tel' in dct_info else self.community_manager_tel
        self.community_start_time = dct_info.get('community_start_time') if 'community_start_time' in dct_info else self.community_start_time
        self.community_home_num = dct_info.get('community_home_num') if 'community_home_num' in dct_info else self.community_home_num
        self.community_account = dct_info.get('community_account') if 'community_account' in dct_info else self.community_account
        self.community_pwd = dct_info.get('community_pwd') if 'community_pwd' in dct_info else self.community_pwd
        self.reg_time = dct_info.get('reg_time') if 'reg_time' in dct_info else self.reg_time

class Adv(models.Model):
    picdir = models.CharField(default='', max_length=255)
    picurl = models.CharField(default='', max_length=255)
    advurl = models.CharField(default='', max_length=255)
    addtime = models.CharField(default='', max_length=255)

    def get_info(self):
        return {
            'picdir' : self.picdir,
            'picurl' : self.picurl,
            'advurl' : self.advurl,
            'addtime': self.addtime
        }

    def set_info(self,dct_info):
        self.picdir = dct_info.get('picdir') if 'picdir' in dct_info else self.picdir
        self.picurl = dct_info.get('picurl') if 'picurl' in dct_info else self.picurl
        self.advurl = dct_info.get('advurl') if 'advurl' in dct_info else self.advurl
        self.addtime = dct_info.get('addtime') if 'addtime' in dct_info else self.addtime

class StatisticsItem(models.Model):
    cname = models.CharField(default='', max_length=255)
    ename = models.CharField(default='', max_length=255)
    note = models.CharField(default='', max_length=255)

    def get_info(self):
        return {
            'cname':self.cname,
            'ename':self.ename,
            'note':self.note
        }

    def set_info(self,dct_info):
        self.cname = dct_info.get('cname') if 'cname' in dct_info else self.cname
        self.ename = dct_info.get('ename') if 'ename' in dct_info else self.ename
        self.note = dct_info.get('note') if 'note' in dct_info else self.note

class Commision(models.Model):
    shopid = models.CharField(default='', max_length=255)
    proid = models.CharField(default='', max_length=255)
    commision_ratio = models.CharField(default='', max_length=255)

    def get_info(self):
        return {
            'shopid':self.shopid,
            'proid':self.proid,
            'commision_ratio':self.commision_ratio
        }

    def set_info(self):
        self.shopid = dct_info.get('shopid') if 'shopid' in dct_info else self.shopid
        self.proid = dct_info.get('proid') if 'proid' in dct_info else self.proid
        self.commision_ratio = dct_info.get('commision_ratio') if 'commision_ratio' in dct_info else self.commision_ratio