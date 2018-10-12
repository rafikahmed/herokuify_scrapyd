from twisted.application.service import Application
from twisted.application.internet import TimerService, TCPServer
from twisted.web import server
from twisted.python import log

from scrapy.utils.misc import load_object

from scrapyd.interfaces import IEggStorage, IPoller, ISpiderScheduler, IEnvironment
from scrapyd.eggstorage import FilesystemEggStorage
from scrapyd.scheduler import SpiderScheduler
from scrapyd.poller import QueuePoller
from scrapyd.environ import Environment
from scrapyd.config import Config
import os

def application(config):
    app = Application("Scrapyd")
    http_port = config.getint('http_port', 6800)

    if 'PORT' in os.environ:
        http_port = int(os.environ.get('PORT'))

    bind_address = '0.0.0.0' if 'PORT' in os.environ else config.get('bind_address', '127.0.0.1')

    poll_interval = config.getfloat('poll_interval', 5)

    poller = QueuePoller(config)
    eggstorage = FilesystemEggStorage(config)
    scheduler = SpiderScheduler(config)
    environment = Environment(config)

    app.setComponent(IPoller, poller)
    app.setComponent(IEggStorage, eggstorage)
    app.setComponent(ISpiderScheduler, scheduler)
    app.setComponent(IEnvironment, environment)

    laupath = config.get('launcher', 'scrapyd.launcher.Launcher')
    laucls = load_object(laupath)
    launcher = laucls(config, app)

    webpath = config.get('webroot', 'scrapyd.website.Root')
    webcls = load_object(webpath)

    timer = TimerService(poll_interval, poller.poll)
    webservice = TCPServer(http_port, server.Site(webcls(config, app)), interface=bind_address)
    log.msg(format="Scrapyd web console available at http://%(bind_address)s:%(http_port)s/",
            bind_address=bind_address, http_port=http_port)

    launcher.setServiceParent(app)
    timer.setServiceParent(app)
    webservice.setServiceParent(app)

    return app