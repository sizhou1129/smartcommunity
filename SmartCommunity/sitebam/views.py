#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from .models import *
from shopbam.models import *

import datetime
import logging
import os

logger = logging.getLogger('django')
import json
# Create your views here.
def handle_test(request):
    return render(request, 'sitebam/index.html')

def handle_login(request):
    logger.info(request.POST)
    logger.info(request.GET)

    data_ = request.POST
    action_ = request.POST.get('opt')
    if not data_.get('account') or not data_.get('pwd'):
        ret = {"status": 1, 'data': {}}
        return JsonResponse(ret)

    qset_siteusr = SiteUser.objects.all()
    if not len(qset_siteusr):
        site_usr = SiteUser(
            account=data_['account'],
            pwd=data_['pwd'],
        )
        site_usr.save()
        request.session['sitebam_account'] = data_['account']
        ret = {"status": 0, 'data': {}}
        return JsonResponse(ret)

    qset_siteusr = SiteUser.objects.filter(
        account=data_['account'],
        pwd=data_['pwd'],
    )
    if len(qset_siteusr):
        request.session['sitebam_account'] = data_['account']
        ret = {"status": 0, 'data': {}}
    else:
        ret = {"status": 1, 'data': {}}
    return JsonResponse(ret)

def handle_logout(request):
    logger.info(request.POST)
    logger.info(request.GET)
    request.session.pop('sitebam_account')
    ret = {"status": 0, 'data': {}}
    return JsonResponse(ret)

def handle_metadata(request):
    logger.info(request.POST)
    logger.info(request.GET)
    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        lst_info = get_by_filter(Metadata, request.GET)
        ret = {
            "status": 0 if len(lst_info) else 1,
            'data': lst_info
        }
        return JsonResponse(ret)

    elif request.method == 'POST':
        data_ = request.POST
        action_ = request.POST.get('opt')
        if not action_:
            ret = {"status": 1, 'data': {}}
            return JsonResponse(ret)
        if action_ == 'add':
            m = Metadata()
            m.set_info(data_)
            m.save()
            ret = {"status": 0, 'data': {}}
            return JsonResponse(ret)
        elif action_ == 'del':
            id_ = data_.get('id')
            if not id_:
                ret = {"status": 1, 'data': {}}
                return JsonResponse(ret)
            qset_metadata = Metadata.objects.filter(id=int(id_))
            if len(qset_metadata):
                qset_metadata[0].delete()
            ret = {"status": 1, 'data': {}}
            return JsonResponse(ret)
        elif action_ == 'mod':
            id_ = data_.get('id')
            if not id_:
                ret = {"status": 1, 'data': {}}
                return JsonResponse(ret)
            qset_metadata = Metadata.objects.filter(id=int(id_))
            if len(qset_metadata):
                qset_metadata[0].set_info(request.POST)
                qset_metadata[0].save()
                ret = {"status": 0, 'data': {}}
                return JsonResponse(ret)
            else:
                ret = {"status": 1, 'data': {}}
                return JsonResponse(ret)

def handle_community(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        lst_info = get_by_filter(Community,request.GET)
        ret = {
            "status": 0 if len(lst_info) else 1,
            'data': lst_info
        }
        return JsonResponse(ret)

    elif request.method == 'POST':
        data_ = request.POST
        action_ = request.POST.get('opt')

        if not action_:
            ret = {"status": 1, 'data': {}}
            return JsonResponse(ret)
        if action_ == 'add':
            m = Community()
            m.set_info(data_)
            m.reg_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            m.save()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'del':
            id_ = request.POST.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})
            qset = Community.objects.filter(id=int(id_))
            if len(qset):
                qset[0].delete()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'mod':
            id_ = request.POST.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})
            qset = Community.objects.filter(id=int(id_))
            if len(qset):
                qset[0].set_info(data_)
                qset[0].save()
                return JsonResponse({"status": 0, 'data': {}})
            else:
                return JsonResponse({"status": 1, 'data': {}})

def handle_merchant(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        lst_info = get_by_filter(Merchant,request.GET)
        ret = {
            "status": 0 if len(lst_info) else 1,
            'data': lst_info
        }
        return JsonResponse(ret)

    elif request.method == 'POST':
        data_ = request.POST
        action_ = request.POST.get('opt')

        if not action_:
            return JsonResponse({"status": 1, 'data': {}})
        elif action_ == 'mod':
            id_ = data_.get('id')
            status_ = data_.get('status')
            if not id_ or not status_:
                return JsonResponse({"status": 1, 'data': {}})

            qset = Merchant.objects.filter(id=int(id_))
            if len(qset):
                qset[0].set_status(status_)
                qset[0].save()
                return JsonResponse({"status": 0, 'data': {}})
            else:
                return JsonResponse({"status": 1, 'data': {}})
        else:
            return JsonResponse({"status": 1, 'data': {}})

def handle_product(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        lst_info = get_by_filter(Product, request.GET)
        ret = {
            "status": 0 if len(lst_info) else 1,
            'data': lst_info
        }
        return JsonResponse(ret)

    elif request.method == 'POST':
        data_ = request.POST
        action_ = request.POST.get('opt')

        if not action_:
            return JsonResponse({"status": 1, 'data': {}})
        elif action_ == 'mod':
            merchant_id_ = data_.get('shopid')
            if not merchant_id_:
                return JsonResponse({"status": 1, 'data': {}})
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})
            status_ = data_.get('status')
            if not status_:
                return JsonResponse({"status": 1, 'data': {}})

            qset = Product.objects.filter(id=int(id_), merchant_id = int(merchant_id_))
            if len(qset):
                qset[0].status = status_
                qset[0].save()
                return JsonResponse({"status": 0, 'data': {}})
            else:
                return JsonResponse({"status": 1, 'data': {}})
        else:
            return JsonResponse({"status": 1, 'data': {}})

def handle_adv(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        lst_info = get_by_filter(Adv, request.GET)
        ret = {
            "status": 0 if len(lst_info) else 1,
            'data': lst_info
        }
        return JsonResponse(ret)

    elif request.method == 'POST':
        data_ = request.POST
        action_ = request.POST.get('opt')

        if not action_:
            return JsonResponse({"status": 1, 'data': {}})
        elif action_ == 'add':
            file_adv_pic_ = data_.get('file_adv_pic')
            if not file_adv_pic_:
                return JsonResponse({"status": 1, 'data': {}})
            file_path = save_file(file_adv_pic_, '../upload/file_adv_pic')
            adv = Adv()
            data_['picdir'] = file_path
            data_['addtime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            adv.set_info(data_)
            adv.save()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'del':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})
            qset = Adv.objects.filter(id=int(id_))
            if len(qset):
                qset[0].delete()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'mod':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})
            file_adv_pic_ = data_.get('file_adv_pic')
            if file_adv_pic_:
                file_path = save_file(file_adv_pic_, '../upload/file_adv_pic')
                data_['picdir'] = file_path
            qset = Adv.objects.filter(id=int(id_))
            if not len(qset):
                return JsonResponse({"status": 1, 'data': {}})
            else:
                qset[0].set_info(data_)
                qset[0].save()
                return JsonResponse({"status": 0, 'data': {}})

def handle_index(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        lst_info = get_by_filter(StatisticsItem, request.GET)
        ret = {
            "status": 0 if len(lst_info) else 1,
            'data': lst_info
        }
        return JsonResponse(ret)
    elif request.method == 'POST':
        data_ = request.POST
        action_ = data_.get('opt')

        if not action_:
            return JsonResponse({"status": 1, 'data': {}})
        elif action_ == 'add':
            stat_item = StatisticsItem()
            stat_item.set_info(data_)
            stat_item.save()
        elif action_ == 'del':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})
            qset = StatisticsItem.objects.filter(id=int(id_))
            if not len(qset):
                qset[0].delete()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'mod':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})
            qset = StatisticsItem.objects.filter(id=int(id_))
            if not len(qset):
                qset[0].set_info(data_)
                return JsonResponse({"status": 0, 'data': {}})
            else:
                return JsonResponse({"status": 1, 'data': {}})

def handle_commision(request):
    logger.info(request.POST)
    logger.info(request.GET)

    if not request.session.get('housebam_id'):
        return JsonResponse({"status": 1, 'data': {}})

    if request.method == 'GET':
        lst_info = get_by_filter(Commision, request.GET)
        ret = {
            "status": 0 if len(lst_info) else 1,
            'data': lst_info
        }
        return JsonResponse(ret)
    elif request.method == 'POST':
        data_ = request.POST
        action_ = data_.get('opt')

        if not action_:
            return JsonResponse({"status": 1, 'data': {}})
        elif action_ == 'add':
            comm = Commision()
            comm.set_info()
            comm.save()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'del':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})
            qset = Commision.objects.filter(id=int(id_))
            if len(qset):
                qset[0].delete()
            return JsonResponse({"status": 0, 'data': {}})
        elif action_ == 'mod':
            id_ = data_.get('id')
            if not id_:
                return JsonResponse({"status": 1, 'data': {}})
            qset = Commision.objects.filter(id=int(id_))
            if not len(qset):
                return JsonResponse({"status": 1, 'data': {}})
            else:
                qset[0].set_info(data_)
                qset[0].save()
                return JsonResponse({"status": 0, 'data': {}})



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

def save_file(file_data, local_path, name):
    file_path = os.path.join(local_path, file_data.name)
    destination = open(file_path, 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in file_data.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    return file_path