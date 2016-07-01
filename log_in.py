# coding=utf-8
from __future__ import absolute_import
import os
import time
import random

import requests
from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse

from user_agents import USER_AGENT_LIST


class OutputStore:
    """
    save requested pages
    """
    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

    def set_output_folder(self):
        if os.path.isdir(self.output_folder) is False:
            os.mkdir(self.output_folder)

    def save(self, response_data, filename=None):
        self.set_output_folder()
        if filename is None:
            store_file_name = str(len(os.listdir(self.output_folder)) + 1) + ".html"
        else:
            store_file_name = filename
        store_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', store_file_name))
        file_open = open(store_file_path, 'w+')
        try:
            file_open.write(response_data)
        except Exception as e:
            try:
                file_open.write(response_data.encode('utf8'))
            except Exception as e:
                print e
        file_open.close()


class Connector:
    """
    Connect LinkedIn and process page requesting
    """
    client = requests.Session()
    HOMEPAGE_URL = 'https://www.linkedin.com'
    LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'
    html = client.get(HOMEPAGE_URL).content
    soup = BeautifulSoup(html, "lxml")
    csrf = soup.find(id="loginCsrfParam-login")['value']

    login_information = {
        'session_key': 'michal.f@mail.com',
        'session_password': '',
        'loginCsrfParam': csrf,
    }
    output_store = OutputStore()
    urls_to_parse = ['https://www.linkedin.com/vsearch/f?adv=true&trk=federated_advs']

    def get_url(self):
        """
        request passed url and return response body for data parsing
        """

        self.client.addheaders = [('User-agent', random.choice(USER_AGENT_LIST))]

        self.client.post(self.LOGIN_URL, data=self.login_information)
        if len(self.urls_to_parse) > 0:
            url = self.urls_to_parse.pop()
            response_page = self.client.get(url)
            response_str = ''.join(response_page.text)
            self.output_store.save(response_str)
            self.create_and_parse_response(response_str.encode('utf8'), url)
        else:
            print "no urls to parse"

    def create_and_parse_response(self, html_body, page_url):
        response = HtmlResponse(url=page_url, body=html_body)
        print "Response parsing page:", page_url

        def rc(selector):
            """ simple shortcut - only for convenience"""
            return response.css(selector)

        if len(rc('li.next')) > 0:
            pagination = rc('li.next')
        elif response.body.find("Następna strona") > 0:
            next_page = response.body[response.body.find("Następna strona"):]
            next_page = next_page[next_page.find(":") + 1:next_page.find(',"next')]
            try:
                next_page_int = int(next_page)
            except Exception as e:
                print "next page number not found"

            next_url = self.HOMEPAGE_URL + "/vsearch/f?pt=people&page_num=" + next_page
            self.urls_to_parse.append(next_url)
            print "url parsed, next:", next_page
            time.sleep(random.randrange(30, 600, 1))
            self.get_url()

        print "FINISH PARSING"


def run():
    conn = Connector()
    conn.get_url()
    print "exit"


run()
