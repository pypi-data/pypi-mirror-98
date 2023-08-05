# coding=utf-8
from __future__ import absolute_import, print_function

import datetime
import logging
import logging.handlers
import os
import platform

import pytz

import suanpan
from suanpan import api, g, path
from suanpan.utils import functional


class Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.datetime.fromtimestamp(record.created)
        try:
            tz = pytz.timezone(self.tzName)
        except Exception:  # pylint: disable=broad-except
            tz = pytz.utc
        converted = dt.astimezone(tz)
        return converted.strftime(datefmt) if datefmt else converted.isoformat()

    def __init__(
        self,
        fmt="%(asctime)s :: %(levelname)-10s :: %(message)s",
        datefmt=None,
        timezone="UTC",
    ):
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.tzName = timezone


class Logger(logging.Logger):

    FORMATTER = Formatter(timezone=g.timezone)
    STREAM_LOG_LEVEL = logging.DEBUG
    FILE_LOG_LEVEL = logging.DEBUG
    LOGKIT_LOG_LEVEL = logging.DEBUG
    LOG_FILE_MAX_SIZE = 1024 * 1024 * 1024
    BACKUP_COUNT = 5
    LOG_PATH = "logs"
    LOG_FILE = None
    LOGKIT_URL = g.logkitUrl
    LOGKIT_NAMESPACE = g.logkitNamespace
    LOGKIT_EVENTS_APPEND = g.logkitEventsAppend

    def __init__(self, name="suanpan"):
        super().__init__(name=name)
        self.addStreamHandler(level=logging.DEBUG if g.debug else logging.INFO)
        if self.LOGKIT_URL:
            self.addLogkitHandler(level=logging.DEBUG if g.debug else logging.INFO)

    def addStreamHandler(self, level=STREAM_LOG_LEVEL, formatter=FORMATTER):
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(level)
        streamHandler.setFormatter(formatter)
        self.addHandler(streamHandler)
        return streamHandler

    def addFileHandler(
        self,
        level=FILE_LOG_LEVEL,
        formatter=FORMATTER,
        logPath=LOG_PATH,
        logFile=LOG_FILE,
        logFileMaxSize=LOG_FILE_MAX_SIZE,
        backupCount=BACKUP_COUNT,
    ):
        logFile = logFile or f"{self.name}.log"
        logFilePath = os.path.join(logPath, logFile)
        path.mkdirs(logFilePath, parent=True)
        fileHandler = logging.handlers.RotatingFileHandler(
            logFilePath, maxBytes=logFileMaxSize, backupCount=backupCount
        )
        fileHandler.setLevel(level)
        fileHandler.setFormatter(formatter)
        self.addHandler(fileHandler)
        return fileHandler

    def addLogkitHandler(
        self,
        level=LOGKIT_LOG_LEVEL,
        formatter=FORMATTER,
        url=LOGKIT_URL,
        namespace=LOGKIT_NAMESPACE,
        event=LOGKIT_EVENTS_APPEND,
    ):
        logkitHandler = LoggerLogkitHandler(url, namespace, event)
        logkitHandler.setLevel(level)
        logkitHandler.setFormatter(formatter)
        self.addHandler(logkitHandler)
        return logkitHandler

    @functional.onlyonce
    def logDebugInfo(self):
        self.logPythonVersion()
        self.logSdkVersion()

    @functional.onlyonce
    def logSdkVersion(self):
        self.debug("Suanpan SDK (ver: {})".format(suanpan.__version__))

    @functional.onlyonce
    def logPythonVersion(self):
        self.debug("Python (ver: {})".format(platform.python_version()))

    def makeRecord(
        self,
        name,
        level,
        fn,
        lno,
        msg,
        args,
        exc_info,
        func=None,
        extra=None,
        sinfo=None,
    ):
        extra = {"extra": {"app": g.appId, "node": g.nodeId, **(extra or {})}}
        return super().makeRecord(
            name, level, fn, lno, msg, args, exc_info, func, extra, sinfo
        )


class LoggerProxy(object):
    def __init__(self, loggerOrName):
        self.setLogger(loggerOrName)

    def __getattr__(self, key):
        return getattr(self.logger, key)

    def setLogger(self, loggerOrName):
        self.logger = (
            loggerOrName if isinstance(loggerOrName, Logger) else Logger(loggerOrName)
        )


class LoggerLogkitHandler(logging.Handler):
    def __init__(self, url, namespace, event):
        super().__init__()
        self.client = None
        self.url = url
        self.namespace = namespace
        self.event = event

    def makeClient(self):
        return api.sio(self.url, namespaces=self.namespace)

    def send(self, msg):
        if not self.client:
            self.client = self.makeClient()
        elif not self.client.connected:
            self.client.disconnect()
            self.client = self.makeClient()
        self.client.emit(self.event, data=msg, namespace=self.namespace)

    def makePickle(self, record):
        app = record.extra.pop("app")
        json = {
            "app": app,
            "logs": [
                {
                    "level": record.levelname,
                    "title": record.message,
                    "data": record.extra,
                    "time": datetime.datetime.now().isoformat(),
                }
            ],
        }
        return json

    def emit(self, record):
        try:
            msg = self.makePickle(record)
            self.send(msg)
        except Exception:  # pylint: disable=broad-except
            self.handleError(record)

    def close(self):
        """
        Closes the socket.
        """
        self.acquire()
        try:
            if self.client:
                self.client.disconnect()
                self.client = None
            super().close()
        finally:
            self.release()


rootLogger = Logger("suanpan")
logger = LoggerProxy(rootLogger)
