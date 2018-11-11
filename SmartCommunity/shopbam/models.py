#coding:utf-8
from django.db import models

# Create your models here.

class Merchant(models.Model):
    province = models.CharField(default='', max_length=255)#省
    city = models.CharField(default='', max_length=255)#市
    name = models.CharField(default='', max_length=255)#公司名称
    boss = models.CharField(default='', max_length=255)#公司负责人
    tel = models.CharField(default='', max_length=255)#电话
    addr = models.CharField(default='', max_length=255)#地址
    license = models.CharField(default='', max_length=255)#执照照片
    account = models.CharField(default='', max_length=255)#账号
    pwd = models.CharField(default='', max_length=255)#密码
    regtime = models.CharField(default='', max_length=255)#注册时间
    status = models.CharField(default='', max_length=255)#状态

    def get_info(self):
        return {
            u'id': self.id,
            u'province': self.province,
            u'city': self.city,
            u'name': self.name,
            u'boss': self.boss,
            u'tel': self.tel,
            u'addr': self.addr,
            u'license': self.license,
            u'account': self.account,
            u'pwd': self.pwd,
            u'regtime': self.regtime,
            u'status': self.status,
        }

    def set_info(self, dct_info):
        self.province = dct_info.get('province', '')
        self.city = dct_info.get('city', '')
        self.name = dct_info.get('name', '')
        self.boss = dct_info.get('boss', '')
        self.tel = dct_info.get('tel', '')
        self.addr = dct_info.get('addr', '')
        self.license = dct_info.get('license', '')
        self.account = dct_info.get('account', '')
        self.pwd = dct_info.get('pwd', '')
        self.regtime = dct_info.get('regtime', '')
        self.status = dct_info.get('status', '')

    def set_status(self, status_):
        if status_ == '关闭':
            qset = Product.objects.filter(merchant_id = str(self.id))
            for q in qset:
                q.status = '已下架'



class Product(models.Model):
    merchant_id = models.CharField(default='', max_length=255)  # 商家公司id
    title = models.CharField(default='', max_length=255)  # 商品标题
    desc = models.CharField(default='', max_length=255)  # 描述
    oldpri = models.CharField(default='', max_length=255)  # 原价
    newpri = models.CharField(default='', max_length=255)  # 现价
    standard = models.CharField(default='', max_length=255)  # 规格包装
    place = models.CharField(default='', max_length=255)  # 产地
    store = models.CharField(default='', max_length=255)  # 库存
    aftersale = models.CharField(default='', max_length=255)  # 售后
    paras = models.CharField(default='', max_length=255)  # 参数
    detail = models.CharField(default='', max_length=255)  # 图文详情
    status = models.CharField(default='', max_length=255)  # 状态
    addtime = models.CharField(default='', max_length=255)  # 添加时间

    def get_info(self):
        qset = Merchant.objects.filter(id=int(self.merchant_id))
        if not len(qset):
            return {}
        return {
            'merchant_id': self.merchant_id,  # 商家公司id
            'merchant_name': qset[0].name,
            'title': self.title,  # 商品标题
            'desc': self.desc,  # 描述
            'oldpri': self.oldpri,  # 原价
            'newpri': self.newpri,  # 现价
            'standard': self.standard , # 规格包装
            'place': self.place,  # 产地
            'store': self.store,  # 库存
            'aftersale': self.aftersale,  # 售后
            'paras': self.paras,  # 参数
            'detail': self.detail,  # 图文详情
            'status': self.status,  # 状态
            'addtime': self.addtime,  # 添加时间
        }
