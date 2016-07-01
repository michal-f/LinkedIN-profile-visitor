# -*- coding: utf-8 -*-
import time
import datetime

from constance import config

from scrapper_app.models import ListPage, ProfilePage, RequestException
from _exceptions import *


def get_time():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def get_time_name():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')


def log(*args):
    if config.DEBUG_CONSOLE_LOGS == "yes":
        try:
            print('[debug log]: %s' % (
                ', '.join(['%s' % et for et in args]),
            ))
        except Exception:
            pass


def writer(path, data):
    try:
        with open(path, "a+") as f:
            f.write(data + "\n")
    except Exception:
        try:
            with open(path, "a+") as f:
                f.write(data.encode("utf8") + "\n")
        except Exception as e:
            log(e)


class DBQuery:
    def create_listpage(self, url, response_code, exception=None):
        try:
            new_listpage, created = ListPage.objects.update_or_create(
                url=url,
                response_code=response_code,
                exception=exception
            )

            return new_listpage
        except Exception as e:
            raise CreateListPageException(e)

    def new_profile(self, url, list_page):
        try:
            new_profilepage = ProfilePage(
                url=url,
                parent=list_page,
                visited=False,
            )
            new_profilepage.save()
        except Exception as e:
            raise CreateProfileException(e)

    def save_profile_request_result(self, url, response_code, exception=None, profile_name=None):
        try:
            profile_page = ProfilePage.objects.get(url=url)
            profile_page.visited = True
            profile_page.response_code = response_code
            profile_page.exception = exception
            profile_page.name = profile_name
            profile_page.save()
            return True
        except Exception as e:
            raise UpdateProfileFailed(e)

    def count_visited(self):
        visited_profiles_count = ProfilePage.objects.all().filter(visited=True).count()
        status_code_200_count = ProfilePage.objects.all().filter(visited=True).filter(response_code=200).count()
        return [visited_profiles_count, status_code_200_count]

    def not_yet_visited(self):
        not_yet_visited = []
        for profile in ProfilePage.objects.values_list('url', flat=True).filter(visited=False):
            not_yet_visited.append(profile)
        return not_yet_visited

    def last_listpage_url(self):
        last = ListPage.objects.values_list('url', flat=True).order_by("id").reverse()[:1]
        return last

    def count_exceptions(self):
        return RequestException.objects.all().count()

    def get_exceptions(self):
        return RequestException.objects.all()

    def save_exception(self, url, status_code, response_content, response_header):
        try:
            new_exception = RequestException(
                url=url,
                status_code=status_code,
                response_content=response_content,
                response_header=response_header,
            )
            new_exception.save()
            return new_exception
        except Exception as e:
            raise CreateRequestException(e)
