# -*- coding: utf-8 -*-
from django.db import models


class RequestException(models.Model):
    """
    Exception info -> if request status code != 200
    """
    url = models.URLField(max_length=1000)
    status_code = models.IntegerField(null=True)
    response_content = models.TextField(null=True)
    response_header = models.TextField(null=True)
    visited_date = models.DateTimeField(auto_now=True)


class ListPage(models.Model):
    """
    contact list page
    """
    url = models.URLField("URL", unique=True, max_length=1000)
    response_code = models.IntegerField()
    visited_date = models.DateTimeField(auto_now=True)
    exception = models.ForeignKey(RequestException, null=True)

    def __str__(self):
        return self.url.encode('utf8')


class ProfilePage(models.Model):
    """
    profile page
    """
    name = models.TextField(null=True)
    url = models.URLField("URL", unique=True, max_length=1000)
    response_code = models.IntegerField(null=True)
    visited_date = models.DateTimeField(auto_now=True)
    visited = models.BooleanField(default=False)
    parent = models.ForeignKey(ListPage)
    exception = models.ForeignKey(RequestException, null=True)

    def __str__(self):
        return self.url.encode('utf8')