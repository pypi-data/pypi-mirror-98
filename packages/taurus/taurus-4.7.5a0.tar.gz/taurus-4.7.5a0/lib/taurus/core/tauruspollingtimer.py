#!/usr/bin/env python

#############################################################################
##
# This file is part of Taurus
##
# http://taurus-scada.org
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Taurus is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Taurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""This module contains the polling class"""

import weakref
import threading
import time

from .util.log import Logger
from .util.containers import CaselessWeakValueDict, CaselessDict


__all__ = ["TaurusPollingTimer"]

__docformat__ = "restructuredtext"



class TaurusPollingTimer(Logger):
    """ Polling timer manages a list of attributes that have to be polled in
    the same period """

    def __init__(self, period, parent=None):
        """Constructor

           :param period: (int) polling period (miliseconds)
           :param parent: (Logger) parent object (default is None)
        """
        name = "TaurusPollingTimer[%d]" % period
        super(TaurusPollingTimer, self).__init__(name=name, parent=parent)
        self._period = period / 1000.  # we store it internally in seconds
        self.dev_dict = {}
        self.attr_nb = 0
        self.timer = None
        self.lock = threading.Lock()
        self.__thread = threading.Thread(target=self.__run, name=name)
        self.__thread.setDaemon(True)
        self._started = True
        self.__thread.start()

    def __run(self):
        """ Private Thread Function """
        next_time = time.time() + self._period
        while True:
            if not self._started:
                # emulate stopped
                time.sleep(self._period)
                continue
            self._pollAttributes()
            curr_time = time.time()
            nap = max(0, next_time - curr_time)
            if curr_time > next_time:
                self.warning(
                    "loop function took more than loop interval (%ss)",
                    self._period
                )
            next_time += self._period
            time.sleep(nap)

    def start(self):
        """ Starts the polling timer """
        self.deprecated("TaurusPollingTimer.start()", rel="4.7.1")
        self._started = True

    def stop(self, sync=False):
        """ Stop the polling timer"""
        self.deprecated("TaurusPollingTimer.stop()", rel="4.7.1")
        self._started = False

    def containsAttribute(self, attribute):
        """Determines if the polling timer already contains this attribute

           :param attribute: (taurus.core.taurusattribute.TaurusAttribute) the attribute

           :return: (bool) True if the attribute is registered for polling or
                    False otherwise
        """
        dev, attr_name = attribute.getParentObj(), attribute.getSimpleName()
        with self.lock:
            attr_dict = self.dev_dict.get(dev)
            return attr_dict and attr_name in attr_dict

    def getAttributeCount(self):
        """Returns the number of attributes registered for polling

           :return: (int) the number of attributes registered for polling
        """
        return self.attr_nb

    def addAttribute(self, attribute, auto_start=None):
        """Registers the attribute in this polling.

           :param attribute: (taurus.core.taurusattribute.TaurusAttribute) the attribute to be added
           :param auto_start: (bool) if True (default) it tells the polling timer
                              that it should startup as soon as there is at least
                              one attribute registered.
        """
        if auto_start == False:
            self.deprecated(
                "TaurusPollingTimer.addAttribute auto_start argument",
                rel="4.7.1")

        with self.lock:
            dev, attr_name = attribute.getParentObj(), attribute.getSimpleName()
            attr_dict = self.dev_dict.get(dev)
            if attr_dict is None:
                if attribute.factory().caseSensitive:
                    self.dev_dict[dev] = attr_dict = weakref.WeakValueDictionary()
                else:
                    self.dev_dict[dev] = attr_dict = CaselessWeakValueDict()
            if attr_name not in attr_dict:
                attr_dict[attr_name] = attribute
                self.attr_nb += 1

    def removeAttribute(self, attribute):
        """Unregisters the attribute from this polling. If the number of registered
           attributes decreses to 0 the polling is stopped automatically in order
           to save resources.

           :param attribute: (taurus.core.taurusattribute.TaurusAttribute) the attribute to be added
        """
        with self.lock:
            dev, attr_name = attribute.getParentObj(), attribute.getSimpleName()
            attr_dict = self.dev_dict.get(dev)
            if attr_dict is None:
                return
            if attr_name in attr_dict:
                del attr_dict[attr_name]
                self.attr_nb -= 1
            if not attr_dict:
                del self.dev_dict[dev]

    def _pollAttributes(self):
        """Polls the registered attributes. This method is called by the timer
           when it is time to poll. Do not call this method directly
        """
        with self.lock:
            req_ids = {}
            dev_dict = {}
            for dev, attrs in self.dev_dict.items():
                if dev.factory().caseSensitive:
                    dev_dict[dev] = dict(attrs)
                else:
                    dev_dict[dev] = CaselessDict(attrs)

        for dev, attrs in dev_dict.items():
            try:
                req_id = dev.poll(attrs, asynch=True)
                req_ids[dev] = attrs, req_id
            except Exception as e:
                self.error("poll_asynch error")
                self.debug("Details:", exc_info=1)

        for dev, (attrs, req_id) in req_ids.items():
            try:
                dev.poll(attrs, req_id=req_id)
            except Exception as e:
                self.error("poll_reply error %r", e)