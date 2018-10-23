# Herokuify-Scrapyd
This package was mainly developed to make deploying Scrapy spiders to Heroku easy. 
## Features
 - Support Python >=3.6 and Scrapy 1.5.1
 - Support running scrapyd locally
 - Support running scrapyd on Heroku
## Configuration
On your scrapy.cfg file copy & paste the following:
````ini
[scrapyd]
application = herokuify_scrapyd.app.application

[deploy]

url = http://<HEROKU_APP_NAME>.herokuapp.com
project = <PROJECT_NAME>
````
Now on you project root directory create a file called Procfile and inside it write: 
````ini 
web: scrapyd
````
