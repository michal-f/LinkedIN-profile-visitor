# -*- coding: utf-8 -*-
import sys
import time
import datetime
import random

import requests

from bs4 import BeautifulSoup

from constance import config

from utils import DBQuery, log
from user_agents import USER_AGENT_LIST
from _exceptions import *


def get_time():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


class Scrapper:
    """
    Connect LinkedIn and process page requesting
    """
    client = requests.Session()
    homepage_url = 'https://www.linkedin.com'
    login_url = homepage_url + '/uas/login-submit'
    html = client.get(homepage_url).content
    soup = BeautifulSoup(html, "lxml")
    csrf = soup.find(id="loginCsrfParam-login")['value']
    headers = {'Connection': 'keep-alive'}
    current_listpage = 0
    proxies, counter, profiles_to_visit = {}, 0, []
    user = {'login': '', 'password': ''}

    dbquery = DBQuery()

    def __init__(self, USER, proxy=None):
        if proxy is not None:
            self.proxies.update({'http': "http://" + proxy})

        try:
            self.user['login'] = USER['login'],
            self.user['password'] = USER['password'],
        except CredentialsError as e:
            raise CredentialsError(e, "NO Valid credentials found! exit!")

        self.create_session()
        self.set_previous_status()
        self.request_processor()

    def create_session(self):
        session_key = self.user['login'],
        session_password = self.user['password']

        login_information = {'session_key': session_key,
                             'session_password': session_password,
                             'loginCsrfParam': self.csrf}

        self.client.addheaders = [('User-agent', random.choice(USER_AGENT_LIST))]
        self.client.post(self.login_url, data=login_information)

    def set_previous_status(self):
        try:
            last_listpage = self.dbquery.last_listpage_url()
            if len(last_listpage) > 0:
                self.current_listpage = int(last_listpage[0][last_listpage[0].find('page_num=') + 9:])
                self.profiles_to_visit = self.dbquery.not_yet_visited()
                log("continuation of last run..")
                self.print_statistics()
            else:
                log("New scrapper start..")
        except Exception:
            pass
            log("New scrapper start..")

    def print_statistics(self):
        visited_profiles = self.dbquery.count_visited()
        statistics = '\n' + 70 * '-' + '\n' + ' Current scrapper statistics:\n '
        statistics += '* visited profiles: ' + str(visited_profiles[0]) + '  (status 200: ' + str(visited_profiles[1]) + ")\n "
        statistics += '* exceptions count: ' + str(self.dbquery.count_exceptions()) + "\n "
        statistics += '* current list page number: ' + str(self.current_listpage) + "\n " + 70 * '-'
        log(statistics)

    def random_sleep(self):
        randomized_time_sleep_interval = random.randrange(config.MIN_INTERVAL, config.MAX_INTERVAL, 1)
        log('randomized sleep: ', str(randomized_time_sleep_interval), " sec.")
        time.sleep(randomized_time_sleep_interval)

    def _set_user_agent(self):
        self.user_agent = random.choice(USER_AGENT_LIST)
        self.headers.update({'User-Agent': self.user_agent})

    def get_next_list_page(self):
        try:
            self.current_listpage += 1
            return self.homepage_url + "/vsearch/p?f_N=S&page_num=" + str(self.current_listpage)
        except NextPageNotFound:
            raise NextPageNotFound(self.current_listpage)

    def get_next_url(self):
        try:
            if len(self.profiles_to_visit) > 0:
                return self.profiles_to_visit.pop()
            else:
                return self.get_next_list_page()
        except Exception as e:
            raise NoUrlsToParse(e)

    def request_processor(self):
        self.counter += 1
        url = self.get_next_url()
        log("[request processor][counter:" + str(self.counter) + "]=>get:" + url)

        self.client.headers.update(self.headers)
        if self.counter > 1:
            self.random_sleep()
        try:
            response_object = self.client.get(url, headers=self.headers, verify=False, proxies=self.proxies)
        except requests.exceptions.RequestException as e:
            self.dbquery.save_exception(url, e.errno, e.message, e.request)
            raise ConnectionErrorException(e)

        if url.find("/vsearch/p?f_N=S&page_num=") > 0:
            self.parse_list_page_response(response_object, url)
        else:
            self.visited_profile_response(response_object, url)

    def visited_profile_response(self, response_object, url):
        """ visited profile response handler """
        status_code = response_object.status_code
        content = response_object.text
        headers = response_object.headers
        exception, profile_name = None, None

        def get_profile_fullname(html_content):
            if html_content.find('class="full-name"') > 0:
                temp_str = html_content[html_content.find('class="full-name"') + 16:]
                profile_name = temp_str[temp_str.find(">") + 1:temp_str.find("<")]
                return profile_name

        if status_code != 200:
            exception = self.dbquery.save_exception(url, status_code, content, headers)
            print InvalidResponseStatus(exception)
            log("[response status != 200 : exiting run]")
            sys.exit(1)
        else:
            profile_name = get_profile_fullname(content)
        self.dbquery.save_profile_request_result(url, status_code, exception, profile_name)
        self.request_processor()

    def parse_list_page_response(self, response_object, url):
        """ parse response list page response"""

        def get_links(input_string):
            """ get profile links """
            splitter_term = 'secondaryActionsList":[{"link_nprofile_view_9":"https://www.linkedin.com/profile/view?'
            temp_list = input_string.split(splitter_term)
            link_list = []
            for num, item in enumerate(temp_list):
                if num > 0:
                    link_list.append('https://www.linkedin.com/profile/view?' + item[:item.find('","') - 1])
            return link_list

        status_code = response_object.status_code
        content = response_object.text
        headers = response_object.headers
        exception = None

        if status_code != 200:
            exception = self.dbquery.save_exception(url, status_code, content, headers)
            self.dbquery.create_listpage(url, status_code, exception)
        else:
            listpage = self.dbquery.create_listpage(url, status_code, exception)
            for profile_link in get_links(content):
                link = profile_link.decode("unicode_escape")
                self.profiles_to_visit.append(link)
                self.dbquery.new_profile(link, listpage)

        self.request_processor()
