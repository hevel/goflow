#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group, User
from goflow.instances.models import Instance

class LeaveRequest(models.Model):
    TYPE_CHOICES = (
            ('Vacation','Vacation'),
            ('Birth or marriage of child','Birth or marriage of child'),
            ('Change of residence','Change of residence'),
            ('Death of a child','Death of a child'),
            ('Death of a relative in the ascending line','Death of a relative in the ascending line'),
            ('Death of parent-in-law, brother or sister','Death of parent-in-law, brother or sister'),
            ('Death of spouse','Death of spouse'),
            ('Marriage','Marriage'),
            ('Maternity','Maternity'),
            ('Serious illness of a child','Serious illness of a child'),
            ('Serious illness of a relative in the asc line','Serious illness of a relative in the asc line'),
            ('Serious illness of a parent-in-law','Serious illness of a parent-in-law'),
            ('Serious illness of spouse','Serious illness of spouse'))
    date = models.DateTimeField(auto_now=True)
    day_start = models.DateField()
    day_end = models.DateField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Vacation')
    reason = models.TextField(null=True, blank=True)
    reason_denial = models.TextField(null=True, blank=True, verbose_name='reason of denial')
    requester = models.ForeignKey(User, null=True, blank=True)
    
    def __str__(self):
        return 'leaverequest-%s' % str(self.pk)

    class Admin:
        fields = (
                  (None, {'fields':(('day_start', 'day_end'), 'type', 'requester', 'reason', 'reason_denial')}),
                  )
        list_display = ('type', 'date', 'day_start', 'day_end', 'requester')
        list_filter = ('type', 'requester')

class Manager(models.Model):
    user = models.ForeignKey(User, related_name='manager_set', edit_inline=True, num_in_admin=3, min_num_in_admin=1, num_extra_on_change=1)
    category = models.CharField(max_length=50, core=True, help_text='secretary, supervisor, ...')
    users = models.ManyToManyField(User, related_name='managers')
    def __str__(self):
        return '%s as %s' % (self.user.username, self.category)
    class Admin:
        pass
    
class Account(models.Model):
    user = models.ForeignKey(User, related_name='accounts', edit_inline=True, num_in_admin=1, min_num_in_admin=1, num_extra_on_change=1)
    category = models.CharField(max_length=50, core=True, help_text='vacations, rtt, ..')
    days = models.IntegerField(default=0)
    
    def __str__(self):
        return '%s-%s' % (self.user.username, self.category)
    class Admin:
        list_display = ('user', 'category', 'days')
