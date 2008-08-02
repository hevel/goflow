#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from models import ProcessInstance, WorkItem

from goflow.utils.decorators import login_required

@login_required
def mywork(request, template='goflow/mywork.html'):
    me = request.user
    workitems = WorkItem.objects.get_all_by(user=me, notstatus='complete', noauto=True)
    return render_to_response(template, {'user':me, 'workitems':workitems})

@login_required
def otherswork(request, template='goflow/otherswork.html'):
    worker = request.GET['worker']
    workitems = WorkItem.objects.get_all_by(username=worker, notstatus='complete', noauto=False)
    return render_to_response(template, {'worker':worker, 'workitems':workitems})

@login_required
def instancehistory(request, template='goflow/instancehistory.html'):
    id = int(request.GET['id'])
    instance = ProcessInstance.objects.get(id=id)
    return render_to_response(template, {'instance':instance})

@login_required
def myrequests(request, template='goflow/myrequests.html'):
    inst_list = ProcessInstance.objects.filter(user=request.user)
    return render_to_response(template, {'user':request.user, 'instances':inst_list})

@login_required
def activate(request, id):
    workitem = WorkItem.objects.get_by(id=int(id), user=request.user)
    workitem.activate(request.user)
    return _app_response(workitem)

@login_required
def complete(request, id):
    workitem = WorkItem.objects.get_by(id=int(id), user=request.user)
    return _app_response(workitem)

def _app_response(workitem):
    id = workitem.id
    activity = workitem.activity
    if not activity.process.enabled:
        return HttpResponse('process %s disabled.' % activity.process.title)
        
    if activity.kind == 'subflow':
        sub_workitem = workitem.start_subflow(workitem.user)
        return _app_response(sub_workitem)
    
    # no application: default_app
    if not activity.application:
        url = '../../../default_app'
        return HttpResponseRedirect('%s/%d/' % (url, id))
    
    if activity.kind == 'standard':
        # standard activity
        return HttpResponseRedirect(activity.application.get_app_url(workitem))
    return HttpResponse('completion page.')

