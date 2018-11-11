#coding:utf-8
from django.shortcuts import render
from django.http import JsonResponse

from sitebam.models import *
from .models import *

import datetime
import logging
logger = logging.getLogger('django')
# Create your views here.
def handle_login(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if request.method == "POST":
        data_ = request.POST
        action_ = data_.get('opt')
        community_account_ = data_.get('community_account')
        community_pwd_ = data_.get('community_pwd')

        if not community_account_ or not community_pwd_:
            return JsonResponse({"status": 1, 'data': {}})

        qset = Community.objects.filer(
            community_account=community_account_,
            community_pwd=community_pwd_,
        )
        if len(qset):
            request.session['housebam_account'] = community_account_
            request.session['housebam_id'] = qset[0].id
            return JsonResponse({"status": 0, 'data': {}})
        else:
            return JsonResponse({"status": 1, 'data': {}})

def handle_logout(request):
    logger.info(request.POST)
    logger.info(request.GET)
    request.session.pop('housebam_account')
    request.session.pop('housebam_id')
    return JsonResponse({"status": 0, 'data': {}})

def handle_reginfo(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    community_id_ = request.session.get('housebam_id')
    qset_community = Community.objects.filter(id=int(community_id_))
    if not len(qset_community):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        return JsonResponse({"status": 0, 'data': qset_community[0].get_info()})
    elif request.method == 'POST':
        data_ = request.POST
        action_ = request.POST.get('opt')
        if action_ == 'mod':
            if data_.get('oldpwd') != qset_community[0].community_pwd:
                return JsonResponse({"status": 1, 'data': {}})
            else:
                if data_.get('newpwd'):
                    qset_community[0].community_pwd = data_.get('newpwd')
                    qset_community[0].save()
                    return JsonResponse({"status": 0, 'data': {}})
                else:
                    return JsonResponse({"status": 1, 'data': {}})

    return JsonResponse({"status": 1, 'data': {}})

def handle_house(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        info = get_by_filter(House, request.GET)
        ret = {
            "status": 0 if len(info) else 1,
            'data': info
        }
        return JsonResponse(ret)

    elif request.method == 'POST':
        data_ = request.POST
        action_ = data_.get('opt')
        if action_ == 'add':
            house = House()
            data_['community_id'] = request.session.get('housebam_id')
            house.set_info(data_)
            house.addtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            house.save()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'del':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})

            qset = House.objects.filter(id=int(id_))
            if len(qset):
                qset[0].delete()
            return JsonResponse({"status": 0, 'data': {}})

        elif action_ == 'mod':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})

            qset = House.objects.filter(id=int(id_))
            if len(qset):
                qset[0].set_info(request.POST)
                qset[0].save()
                return JsonResponse({"status": 0, 'data': {}})
            else:
                return JsonResponse({"status": 1, 'data': {}})


def handle_fee(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        info = get_by_filter(HouseFee, request.GET)
        ret = {
            "status": 0 if len(info) else 1,
            'data': info
        }
        return JsonResponse(ret)

    elif request.method == 'POST':
        data_ = request.POST
        action_ = request.POST.get('opt')
        if action_ == 'add':
            house_fee = HouseFee()
            data_['community_id'] = request.session.get('housebam_id')
            house_fee.set_info(data_)
            house_fee.save()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'del':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})

            qset = HouseFee.objects.filter(id=int(id_))
            if len(qset):
                qset[0].delete()
            return JsonResponse({"status": 0, 'data': {}})

        elif action_ == 'mod':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})

            qset = HouseFee.objects.filter(id=int(id_))
            if len(qset):
                qset[0].set_info(data_)
                qset[0].save()
                return JsonResponse({"status": 0, 'data': {}})
            else:
                return JsonResponse({"status": 1, 'data': {}})


def handle_fee_basic(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        info = get_by_filter(HouseFeeBasic, request.GET)
        ret = {
            "status": 0 if len(info) else 1,
            'data': info
        }
        return JsonResponse(ret)

    if request.method == 'POST':
        data_ = request.POST
        action_ = request.POST.get('opt')
        if action_ == 'add':
            item = HouseFeeBasic()
            data_['community_id'] = request.session.get('housebam_id')
            item.set_info(data_)
            item.save()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'del':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})

            qset = HouseFeeBasic.objects.filter(id=int(id_))
            if len(qset):
                qset[0].delete()
            return JsonResponse({"status": 0, 'data': {}})

        elif action_ == 'mod':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})

            qset = HouseFeeBasic.objects.filter(id=int(id_))
            if len(qset):
                qset[0].set_info(request.POST)
                qset[0].save()
                return JsonResponse({"status": 0, 'data': {}})
            else:
                return JsonResponse({"status": 1, 'data': {}})

def handle_fee_special(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        info = get_by_filter(HouseFeeSpecial, request.GET)
        ret = {
            "status": 0 if len(info) else 1,
            'data': info
        }
        return JsonResponse(ret)

    if request.method == 'POST':
        data_ = request.POST
        action_ = data_.get('opt')
        if action_ == 'add':
            item = HouseFeeSpecial()
            data_['community_id'] = request.session.get('housebam_id')
            item.set_info(data_)
            item.save()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'del':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})

            qset = HouseFeeSpecial.objects.filter(id=int(id_))
            if len(qset):
                qset[0].delete()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'mod':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})

            qset = HouseFeeSpecial.objects.filter(id=int(id_))
            if len(qset):
                qset[0].set_info(request.POST)
                qset[0].save()
                return JsonResponse({"status": 0, 'data': {}})
            else:
                return JsonResponse({"status": 1, 'data': {}})

def handle_repair(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        info = get_by_filter(Repair, request.GET)
        ret = {
            "status": 0 if len(info) else 1,
            'data': info
        }
        return JsonResponse(ret)

    elif request.method == 'POST':
        data_ = request.POST
        action_ = data_['opt']
        if action_ == 'add':
            item = Repair()
            data_['commnunity_id'] = request.session.get('housebam_id')
            item.set_info(data_)
            item.save()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'mod':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})

            qset = Repair.objects.filter(id=int(id_))
            if len(qset):
                qset[0].set_info(data_)
                qset[0].save()
                return JsonResponse({"status": 0, 'data': {}})
            else:
                return JsonResponse({"status": 1, 'data': {}})


def handle_housemanager(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        info = get_by_filter(HouseManager, request.GET)
        ret = {
            "status": 0 if len(info) else 1,
            'data': info
        }
        return JsonResponse(ret)
    elif request.method == 'POST':
        data_ = request.POST
        action_ = data_.get('opt')
        if action_ == 'add':
            item = HouseManager()
            data_['commnunity_id'] = request.session.get('housebam_id')
            data_['addtime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item.set_info(data_)
            item.save()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'del':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})
            qset = HouseManager.objects.filter(id=int(id_))
            if len(qset):
                qset[0].delete()
            return JsonResponse({"status": 0, 'data': {}})

        elif action_ == 'mod':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})

            qset = HouseManager.objects.filter(id=int(id_))
            if len(qset):
                qset[0].set_info(data_)
                qset[0].save()
                return JsonResponse({"status": 0, 'data': {}})
            else:
                return JsonResponse({"status": 1, 'data': {}})


def handle_aroundservice(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        info = get_by_filter(AroundService, request.GET)
        ret = {
            "status": 0 if len(info) else 1,
            'data': info
        }
        return JsonResponse(ret)

    elif request.method == 'POST':
        data_ = request.POST
        action_ = data_.get('opt')
        if action_ == 'add':
            item = AroundService()
            data_['commnunity_id'] = request.session.get('housebam_id')
            data_['addtime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item.set_info(data_)
            item.save()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'del':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})
            qset = AroundService.objects.filter(id=int(id_))
            if len(qset):
                qset[0].delete()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'mod':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})
            qset = AroundService.objects.filter(id=int(id_))
            if len(qset):
                qset[0].set_info(data_)
                qset[0].save()
                return JsonResponse({"status": 0, 'data': {}})
            else:
                return JsonResponse({"status": 1, 'data': {}})


def get_by_filter(clss, dct_filter):
    '''
    如果过滤的键值对和一条记录的内容能匹配上，则这条记录需要输出
    :param clss: 对应模型名
    :param dct_filter: 过滤的键值对
    :return: [{},{}]匹配结果
    '''
    qset = clss.objects.all()
    lst_ret = []
    for item in qset:
        dct_ret = item.get_info()
        if not dct_filter:
            lst_ret.append(dct_ret)
        else:
            match = True
            for key in dct_filter:
                if key in dct_ret and dct_filter[key] != dct_ret[key]:
                    match = False
                    break
            if match:
                lst_ret.append(dct_ret)
    return lst_ret

def return_response(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Credentials"] = "true"
    return response
