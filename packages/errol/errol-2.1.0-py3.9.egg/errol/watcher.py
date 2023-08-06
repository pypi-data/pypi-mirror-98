#!/usr/bin/env python
# Copyright (c) 2021 errol project
# This code is distributed under the GPLv3 License

import asyncio
import os
import logging

from hachiko.hachiko import AIOWatchdog, AIOEventHandler

from . import xmpp


logging.getLogger("asyncio").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

MAX_SEND_COUNTER = 60  # todo  we should have a way to count successfull sended files and retry the errors
WATCHER_INTERVAL = 15  # depends on usecase

class ErrolHandler(AIOEventHandler):

    def __init__(self, loop=None):
        super().__init__(loop)
        self.path = None
        self.xmpp_handler = None
        self.count = 0
        self.errol_error = None
        self.xmpp_instance = None
        self.file_list = []
        self.error = None

    def prepare(self, path, conf_xmpp):
        logger.debug('Errol Watcher:Prepare Errol Handler')
        self.path = path
        self.xmpp_handler = xmpp.XmppHandler()
        logger.info("Errol Watcher: prepare for file %s", path)
        self.xmpp_handler.prepare(path=path, file_list='test.tmp', action='send_file',
                                  forever=False, xmpp_conf=conf_xmpp)
        self.count = 0

    async def file_sender(self):
        self.count += 1
        file_list = set(self.file_list)
        logger.info("Errol Watcher: new batch of %s files : %s", len(file_list), file_list)
        self.file_list = []
        self.xmpp_handler.update_filename(file_list)
        await self.xmpp_handler.update_xmpp_instance()
        logger.info("Errol Watcher: launch handler")
        self.xmpp_instance = self.xmpp_handler.get_xmpp_instance()
        self.xmpp_instance.connect()
        self.errol_error = self.xmpp_instance.errol_error

    async def on_modified(self, event):
        logger.debug(f'Errol Watcher: event type: {event.event_type}  path : {event.src_path}')
        if not os.path.isdir(event.src_path):
            self.file_list.append(event.src_path)

    async def on_created(self, event):
        logger.debug(f'Errol Watcher: event type: {event.event_type}  path : {event.src_path}')
        if not os.path.isdir(event.src_path):
            self.file_list.append(event.src_path)

    def get_counter(self):
        return self.count

    def get_error(self):
        self.errol_error = self.xmpp_instance and self.xmpp_instance.errol_error
        return self.errol_error

    def reset_error(self):
        self.error = None
        if self.xmpp_instance:
            self.xmpp_instance.errol_error = None

    async def restart_sending(self):
        # The file could not be sent. Retry
        logger.error("Errol Watcher: We could not send the file. Retry...")
        # await self._xmpp_handler(self.filename)
        # arj fixme test, we do nothing now to understand


class Watcher:
    def __init__(self):
        self.loop = None
        self.observer = None
        self.task = None
        self.path = None
        self.count = 0
        self.xmpp_handler = None
        self.conf_xmpp = None
        self.event_handler = None
        self.max_events = 0
        self.watch = None

    async def prepare(self, path, conf_xmpp, events):
        self.path = path
        self.conf_xmpp = conf_xmpp
        self.max_events = events
        loop = asyncio.get_event_loop()
        self.event_handler = ErrolHandler(loop)
        self.watch = AIOWatchdog(path, event_handler=self.event_handler)
        self.event_handler.prepare(path=path, conf_xmpp=conf_xmpp)
        self.max_events = events

    async def run(self, debug):
        logger.info("Errol Watcher: Start Watching")
        self.watch.start()
        count = 0
        try:
            while count < self.max_events:
                count = self.event_handler.get_counter()
                await asyncio.sleep(WATCHER_INTERVAL)
                file_list = set(self.event_handler.file_list)
                if file_list:
                    await self.event_handler.file_sender()
                    send_counter = 0
                    while not self.event_handler.xmpp_instance.sent_event.is_set() and send_counter < MAX_SEND_COUNTER:
                        await asyncio.sleep(3)
                        send_counter += 1
                if self.event_handler.xmpp_instance:
                    self.event_handler.xmpp_instance.sent_event.clear()
        except KeyboardInterrupt:
            self.watch.stop()
        return


async def watch(path='', debug=False, events=1000, xmpp_conf=None):
    wa = Watcher()
    await wa.prepare(path, xmpp_conf, events)
    logger.info("Errol Watcher: Running Watcher")
    await wa.run(debug)
    return
