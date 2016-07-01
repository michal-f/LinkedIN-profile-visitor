[TOC]
______________________________________________________________________________________________________________________________________________________
______________________________________________________________________________________________________________________________________________________
##**REQUIREMENTS**##

* requests

* django

* bs4 (BeautifulSoup4)

* django-constance

* pytz


##**HOW TO GET SET UP?**##

* ```pip install -r requirements.txt```

* ```python manage.py migrate```


##**RUN SCRAPPER**##

to start the scrapper must first provide LinkedIn credentials. There are 2 ways to pass:

####First way:

* pass LinkedIn credentials directly to the command line  run command. [via -l parameter] example:

``` 
python manage.py run -l login_name:login_password 
```

####Second way:

* create local_settings.py -> a file in project root with credentials (a python object named USER with 'login' and 'password' fields). example of **local_settings.py**:

```    
USER = {'login': 'profile_login', 'password': 'profile_password'}
```

then run with command:

```
python manage.py run
```



##**SETTINGS**##

Some settings are available in django admin panel -> in Config:

```
DEBUG_CONSOLE_LOGS : yes or No
MAX_INTERVAL (Maximum time interval between requests) : 180 (default)	
MIN_INTERVAL (Minimum time interval between requests) : 30 (default)
```

This config settings are executed dynamically




##**ADDITIONAL INFO**##

After stopping or breaking a scrapper run: next run is continuing from previous state