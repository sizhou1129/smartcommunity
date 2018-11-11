#coding:utf-8
from django.db import models

import datetime

# Create your models here.
class House(models.Model):
    community_id = models.CharField(default='', max_length=255)
    building = models.CharField(default='', max_length=255)  # 楼号
    unit = models.CharField(default='', max_length=255)  # 单元
    floor = models.CharField(default='', max_length=255)  # 楼层
    room = models.CharField(default='', max_length=255)  # 房号
    owner_name = models.CharField(default='', max_length=255)  # 业主
    owner_tel = models.CharField(default='', max_length=255)  # 业主电话
    area = models.CharField(default='', max_length=255)  # 面积
    is_empty = models.CharField(default='', max_length=255)  # 是否空置
    is_lift = models.CharField(default='', max_length=255)  # 是否有电梯
    status = models.CharField(default='', max_length=255)  # 状态
    owner_id = models.CharField(default='', max_length=255)  # 业主id
    addtime = models.CharField(default='', max_length=255)  # 添加时间

    def get_info(self):
        return {
            'building': self.building,
            'unit': self.unit,
            'floor': self.floor,
            'room': self.room,
            'owner_name': self.owner_name,
            'owner_tel': self.owner_tel,
            'area': self.area,
            'is_empty': self.is_empty,
            'is_lift': self.is_lift,
            'status': self.status,
            'owner_id': self.owner_id,
            'addtime': self.addtime,
        }

    def set_info(self, dct_info):
        self.community_id = dct_info.get('community_id') if dct_info.get('community_id') else self.community_id
        self.building = dct_info.get('building') if dct_info.get('building') else self.building
        self.unit = dct_info.get('unit') if dct_info.get('unit') else self.unit
        self.floor = dct_info.get('floor') if dct_info.get('floor') else self.floor
        self.room = dct_info.get('room') if dct_info.get('room') else self.room
        self.owner_name = dct_info.get('owner_name') if dct_info.get('owner_name') else self.owner_name
        self.owner_tel = dct_info.get('owner_tel') if dct_info.get('owner_tel') else self.owner_tel
        self.area = dct_info.get('area') if dct_info.get('area') else self.area
        self.is_empty = dct_info.get('is_empty') if dct_info.get('is_empty') else self.is_empty
        self.is_lift = dct_info.get('is_lift') if dct_info.get('is_lift') else self.is_lift
        self.status = dct_info.get('status') if dct_info.get('status') else self.status
        self.owner_id = dct_info.get('owner_id') if dct_info.get('owner_id') else self.owner_id

class HouseFee(models.Model):
    community_id = models.CharField(default='', max_length=255)
    house_id = models.CharField(default='', max_length=255)
    fee_year = models.CharField(default='', max_length=255)
    fee_month = models.CharField(default='', max_length=255)
    fee_name = models.CharField(default='', max_length=255)
    fee_type = models.CharField(default='', max_length=255)
    fee_pri = models.CharField(default='', max_length=255)
    fee_unit = models.CharField(default='', max_length=255)
    fee_ratio = models.CharField(default='', max_length=255)
    fee_amount = models.CharField(default='', max_length=255)
    fee_money = models.CharField(default='', max_length=255)
    fee_status = models.CharField(default='', max_length=255)
    fee_online = models.CharField(default='', max_length=255)
    addtime = models.CharField(default='', max_length=255)

    def get_info(self):
        qset = House.objects.filter(
            community_id=int(self.community_id),
            id=int(self.house_id)
        )
        if not len(qset):
            return {}
        building = qset[0].building
        unit = qset[0].unit
        floor = qset[0].floor
        room = qset[0].room
        owner_name = qset[0].owner_name
        owner_tel = qset[0].owner_tel
        area = qset[0].area
        return {
            'building': building,
            'unit': unit,
            'floor': floor,
            'room': room,
            'owner_name': owner_name,
            'owner_tel': owner_tel,
            'area' : area,
            'fee_year': self.fee_year,
            'fee_month': self.fee_month,
            'fee_name': self.fee_name,
            'fee_type': self.fee_type,
            'fee_pri': self.fee_pri,
            'fee_unit': self.fee_unit,
            'fee_ratio': self.fee_ratio,
            'fee_amount': self.fee_amount,
            'fee_money': self.fee_money,
            'fee_status': self.fee_status,
            'fee_online' : self.fee_online,
            'addtime': self.addtime,
        }

    def set_info(self, dct_info):
        if self.status == '已缴费':
            return
        house_id_ = dct_info.get('house_id')
        if not house_id_:
            return
        community_id_ = dct_info.get('community_id')
        qset = House.objects.filter(
            community_id=int(community_id_),
            id = int(house_id_)
        )
        if not len(qset):
            return
        house = qset[0]

        fee_year_ = dct_info.get('fee_year')
        if not fee_year_:
            return

        fee_month_ = dct_info.get('fee_month')
        if not fee_month_:
            return

        fee_name_ = dct_info.get('fee_name')
        if not fee_name_:
            return

        qset = HouseFeePara.objects.filter(
            house_id = house_id_,
        )
        if not len(qset):
            return

        if qset[0].fee_special_id:
            qset_house_fee = HouseFeeSpecial.objects.filter(
                id = qset[0].fee_special_id
            )
            if not len(qset_house_fee):
                return

        elif qset[0].fee_basic_id:
            qset_house_fee = HouseFeeBasic.objects.filter(
                id = qset[0].fee_basic_id
            )
            if not len(qset_house_fee):
                return
        fee_type_ = qset_house_fee[0].fee_type
        if fee_type_ == '用量收费':
            if not dct_info.get('fee_amount'):
                return
            fee_amount_ = dct_info.get('fee_amount')
        elif fee_type_ == '面积收费':
            fee_amount_ = house.area
        else:
            fee_amount_ = '1.0'

        fee_pri_ = qset[0].fee_pri
        fee_unit_ = qset[0].fee_unit
        fee_ratio_ = qset[0].fee_ratio

        self.house_id = house_id_
        self.fee_year = fee_year_
        self.fee_month = fee_month_
        self.fee_name = fee_name_
        self.fee_type = fee_type_
        self.fee_pri = fee_pri_
        self.fee_unit = fee_unit_
        self.fee_ratio = fee_ratio_
        self.fee_amount = fee_amount_
        self.fee_money = float(fee_pri_)*float(fee_amount_)*float(fee_ratio_)
        self.fee_status = '待缴费'


class HouseFeePara(models.Model):
    house_id = models.CharField(default='', max_length=255)
    fee_basic_id = models.CharField(default='', max_length=255)
    fee_special_id = models.CharField(default='', max_length=255)

class HouseFeeBasic(models.Model):
    community_id = models.CharField(default='', max_length=255)
    fee_name = models.CharField(default='', max_length=255)

    fee_type = models.CharField(default='', max_length=255)#收费方式（面积收费，固定收费，用量收费）
    fee_pri = models.CharField(default='', max_length=255)# 费用单价
    fee_unit = models.CharField(default='', max_length=255) # 单价单位
    fee_ratio = models.CharField(default='', max_length=255)  # 收费比例

    empty_fee_type = models.CharField(default='', max_length=255)
    empty_fee_pri = models.CharField(default='', max_length=255)
    empty_fee_unit = models.CharField(default='', max_length=255)
    empty_fee_ratio = models.CharField(default='', max_length=255)

    fee_period = models.CharField(default='', max_length=255)#产生周期1,2,3,对应月份1号产生

    def get_info(self):
        return {
            'fee_name': self.fee_name,
            'fee_type': self.fee_type,  # 收费方式（面积收费，固定收费，用量收费）
            'fee_pri': self.fee_pri,  # 费用单价
            'fee_unit': self.fee_unit,  # 单价单位
            'fee_ratio': self.fee_ratio,  # 收费比例
            'empty_fee_type': self.empty_fee_type,
            'empty_fee_pri': self.empty_fee_pri,
            'empty_fee_unit': self.empty_fee_unit,
            'empty_fee_ratio': self.empty_fee_ratio,
            'fee_period': self.fee_period,  # 产生周期1,2,3,对应月份1号产生
        }

    def set_info(self, dct_info):
        self.fee_name = dct_info.get('fee_name') if 'fee_name' in dct_info else self.fee_name
        self.fee_type = dct_info.get('fee_type') if 'fee_type' in dct_info else self.fee_type
        self.fee_pri = dct_info.get('fee_pri') if 'fee_pri' in dct_info else self.fee_pri
        self.fee_unit = dct_info.get('fee_unit') if 'fee_unit' in dct_info else self.fee_unit
        self.fee_ratio = dct_info.get('fee_ratio') if 'fee_ratio' in dct_info else self.fee_ratio
        self.empty_fee_type = dct_info.get('empty_fee_type') if 'empty_fee_type' in dct_info else self.empty_fee_type
        self.empty_fee_pri = dct_info.get('empty_fee_pri') if 'empty_fee_pri' in dct_info else self.empty_fee_pri
        self.empty_fee_unit = dct_info.get('empty_fee_unit') if 'empty_fee_unit' in dct_info else self.empty_fee_unit
        self.empty_fee_ratio = dct_info.get('empty_fee_ratio') if 'empty_fee_ratio' in dct_info else self.empty_fee_ratio
        self.fee_period = dct_info.get('fee_period') if 'fee_period' in dct_info else self.fee_period

        qset = HouseFeePara.objects.filter(
            fee_basic_id=self.id
        )
        if not len(qset):
            qset = House.objects.filter(
                community_id=self.community_id
            )
            for q in qset:
                hfp = HouseFeePara(
                    house_id = q.id,
                    fee_basic_id = self.id
                )
                hfp.save()




class HouseFeeSpecial(models.Model):
    community_id = models.CharField(default='', max_length=255)

    building = models.CharField(default='', max_length=255)  # 楼号
    unit = models.CharField(default='', max_length=255)  # 单元
    floor = models.CharField(default='', max_length=255)  # 楼层
    room = models.CharField(default='', max_length=255)  # 房号
    owner_name = models.CharField(default='', max_length=255)  # 业主

    fee_name = models.CharField(default='', max_length=255)# 费用名称
    fee_type = models.CharField(default='', max_length=255)#建面收费，固定收费，用量收费/area,fixed,quantity
    fee_pri = models.CharField(default='', max_length=255)# 费用单价
    fee_unit = models.CharField(default='', max_length=255) # 单价单位
    fee_ratio = models.CharField(default='', max_length=255)  # 收费比例

    def get_info(self):
        return {
            'building': self.building,
            'unit': self.unit,
            'floor': self.floor,
            'room': self.room,
            'owner_name': self.owner_name,
            'fee_name': self.fee_name,
            'fee_type': self.fee_type,
            'fee_pri': self.fee_pri,
            'fee_unit': self.fee_unit,
            'fee_ratio': self.fee_ratio,
        }

    def set_info(self, dct_info):
        self.building = dct_info.get('building') if 'building' in dct_info else self.building
        self.unit = dct_info.get('unit') if 'unit' in dct_info else self.unit
        self.floor = dct_info.get('floor') if 'floor' in dct_info else self.floor
        self.room = dct_info.get('room') if 'room' in dct_info else self.room
        self.owner_name = dct_info.get('owner_name') if 'owner_name' in dct_info else self.owner_name
        self.fee_name = dct_info.get('fee_name') if 'fee_name' in dct_info else self.fee_name
        self.fee_type = dct_info.get('fee_type') if 'fee_type' in dct_info else self.fee_type
        self.fee_pri = dct_info.get('fee_pri') if 'fee_pri' in dct_info else self.fee_pri
        self.fee_unit = dct_info.get('fee_unit') if 'fee_unit' in dct_info else self.fee_unit
        self.fee_ratio = dct_info.get('fee_ratio') if 'fee_ratio' in dct_info else self.fee_ratio


        qset = House.objects.filter(
            community_id=self.community_id
        )
        if len(qset) and self.building:
            qset = qset.filter(building=self.building)
        if len(qset) and self.unit:
            qset = qset.filter(unit=self.unit)
        if len(qset) and self.floor:
            qset = qset.filter(floor=self.floor)
        if len(qset) and self.room:
            qset = qset.filter(room=self.room)
        if len(qset):
            for house in qset:
                paras = HouseFeePara.objects.filter(
                    house_id=house.house_id,
                )
                if not len(paras):
                    new_para = HouseFeePara(
                        house_id=house.house_id,
                        fee_special_id = self.id,
                    )
                    new_para.save()
                else:
                    paras[0].fee_special_id = self.id
                    paras[0].save()


class Repair(models.Model):
    community_id = models.CharField(default='', max_length=255)

    user_name = models.CharField(default='', max_length=255)
    user_tel = models.CharField(default='', max_length=255)
    pos = models.CharField(default='', max_length=255)
    want_time = models.CharField(default='', max_length=255)
    desc = models.CharField(default='', max_length=255)
    pics = models.CharField(default='', max_length=255)
    addtime = models.CharField(default='', max_length=255)
    accept_time = models.CharField(default='', max_length=255)
    accept_note = models.CharField(default='', max_length=255)
    finish_time = models.CharField(default='', max_length=255)
    finish_note = models.CharField(default='', max_length=255)
    status = models.CharField(default='', max_length=255)

    def get_info(self):
        return {
            'usr' : self.user_name,
            'tel' : self.user_tel,
            'pos' : self.pos,
            'want_time' : self.want_time,
            'desc' : self.desc,
            'pics' : self.pics,
            'addtime' : self.addtime,
            'accept_time' : self.accept_time,
            'accept_note' : self.accept_note,
            'finish_time' : self.finish_time,
            'finish_note' : self.finish_note,
            'status' : self.status,
        }

    def set_info(self, dct_info):
        if 'accept_note' in dct_info:
            self.accept_note = dct_info['dct_info']
            self.accept_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            self.status = '已受理'
        elif 'finish_note' in dct_info:
            self.finish_note = dct_info['finish_note']
            self.finish_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            self.status = '已完成'
        else:
            self.community_id = dct_info['community_id'] if 'community_id' in dct_info else self.community_id
            self.user_name = dct_info['usr'] if 'usr' in dct_info else self.user_name
            self.user_tel = dct_info['tel'] if 'tel' in dct_info else self.user_tel
            self.pos = dct_info['pos'] if 'pos' in dct_info else self.pos
            self.want_time = dct_info['want_time'] if 'want_time' in dct_info else self.want_time
            self.desc = dct_info['desc'] if 'desc' in dct_info else self.desc
            self.pics = dct_info['pics'] if 'pics' in dct_info else self.pics

class HouseManager(models.Model):
    community_id = models.CharField(default='', max_length=255)

    building = models.CharField(default='', max_length=255)
    manager = models.CharField(default='', max_length=255)
    tel = models.CharField(default='', max_length=255)
    wx = models.CharField(default='', max_length=255)
    addtime = models.CharField(default='', max_length=255)


    def get_info(self):
        return {
            'id':self.id,
            'building':self.building,
            'manager':self.manager,
            'tel':self.tel,
            'wx':self.wx,
            'addtime':self.addtime
        }

    def set_info(self, dct_info):
        self.community_id = dct_info['community_id'] if 'community_id' in dct_info else self.community_id
        self.building = dct_info['building'] if 'building' in dct_info else self.building
        self.manager = dct_info['manager'] if '' in dct_info else self.manager
        self.tel = dct_info['tel'] if 'tel' in dct_info else self.tel
        self.wx = dct_info['wx'] if 'wx' in dct_info else self.wx
        self.addtime = dct_info['addtime'] if 'addtime' in dct_info else self.addtime

class AroundService(models.Model):
    community_id = models.CharField(default='', max_length=255)
    catalog = models.CharField(default='', max_length=255)
    srv_name = models.CharField(default='', max_length=255)
    addr = models.CharField(default='', max_length=255)
    tel = models.CharField(default='', max_length=255)
    addtime = models.CharField(default='', max_length=255)

    def get_info(self):
        return{
            'id':self.id,
            'catalog':self.catalog,
            'srv_name':self.srv_name,
            'addr':self.addr,
            'tel':self.tel,
            'addtime':self.addtime
        }

    def set_info(self, dct_info):
        self.community_id = dct_info['community_id'] if 'community_id' in dct_info else self.community_id
        self.catalog = dct_info['catalog'] if 'catalog' in dct_info else self.catalog
        self.srv_name = dct_info['srv_name'] if 'srv_name' in dct_info else self.srv_name
        self.addr = dct_info['addr'] if 'addr' in dct_info else self.addr
        self.tel = dct_info['tel'] if 'tel' in dct_info else self.tel
        self.addtime = dct_info['addtime'] if 'addtime' in dct_info else self.addtime
