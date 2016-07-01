#! /usr/bin/env python
# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from scrapper_app._exceptions import *
from scrapper_app.scrapper import Scrapper


class Command(BaseCommand):
    """
    [Management Command -> run LinkedIn profile visitor app]
    """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.help = self.style.WARNING("\n" + 70 * "_" + "\n [LinkedIn profile visitor App] help info:\n\n")
        self.help += self.style.MIGRATE_HEADING("Login credentials can be passed:\n") + " * via -l option : python manage.py run -l login:password\n"
        self.help += " * placed in local_settings.py: "
        self.help += self.style.WARNING("\n" + 70 * "_")
        self.USER = {'login': '', 'password': ''}

    def add_arguments(self, parser):
        parser.add_argument('-l', dest='credentials', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        manage.py "run" command handler
        Get credentials and run scrapper app
        """
        self.stdout.write('\n [Django Management Command] -> ' + self.style.SUCCESS('starting LinkedIn visitor scrapper app'))
        if self.get_credentials(self, *args, **options):
            Scrapper(self.USER)
        else:
            self.stdout.write(self.style.ERROR("-> No Valid LinkedIn credentials found! exit."))
            self.stdout.write(self.style.WARNING(' please set LinkedIn credentials and try again... '))

    def get_credentials(self, *args, **options):
        """
        LinkedIn credential handler
        """
        try:
            if options['credentials'] is not None:
                if options['credentials'][0].find(":") > 0:
                    self.USER['login'] = options['credentials'][0].split(":")[0]
                    self.USER['password'] = options['credentials'][0].split(":")[1]
                    self.stdout.write(' credentials passed via -l: ' + self.style.SUCCESS('-> ' + str(options['credentials'][0])))
                    return True
                else:
                    self.stdout.write(self.style.ERROR('-> Invalid Credentials format: ' + str(options['credentials'][0])))
                    self.stdout.write(self.style.WARNING(' credentials passing format example: ') + "'-l login:password'")
                    self.stdout.write(self.style.WARNING(' please try again... '))
            else:
                try:
                    if settings.USER:
                        self.USER['login'] = settings.USER['login']
                        self.USER['password'] = settings.USER['password']
                        if len(self.USER['login']) > 0 and len(self.USER['password']) > 0:
                            self.stdout.write(' credentials from local_settings: ' + self.style.SUCCESS('-> ' + self.USER['login'] + ":" + self.USER['password']))
                            return True
                except Exception as e:
                    self.stdout.write(self.style.ERROR('-> Credentials not found! '))
                    raise CredentialsError(e)
        except Exception as e:
            self.stdout.write(self.style.ERROR("\nException: Login Credentials not found!" + self.help))
