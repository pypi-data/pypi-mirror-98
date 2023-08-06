###############################################################################
# (c) Copyright 2013 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
'''
Module containing the classes and functions used to verify preconditions for
building a slot.

@author Marco Clemencic <marco.clemencic@cern.ch>
'''

import os
import logging

from datetime import datetime, timedelta
from time import sleep
from os.path import exists

from LbNightlyTools.Scripts.Common import PlainScript


def waitForFile(path, timeout=timedelta(hours=17), max_age=None):
    '''
    Wait until a file becomes available, but not more than the timedelta
    specified as timeout.
    If max_age is not None, it must be a timedelta and an existing file is
    ignored if it is older than that age.

    @return: True if a valid file appeared within the timeout, False otherwise
    '''
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)

    logging.debug('waiting for file %s', path)

    def fileTime(path):
        '''helper to return the datetime of last modification of a file'''
        return datetime.fromtimestamp(os.path.getmtime(path))

    now = datetime.now()

    when_to_stop = now + timeout

    if max_age:
        min_file_date = now - max_age
    else:
        min_file_date = datetime.fromtimestamp(0)

    while datetime.now() < when_to_stop:
        if exists(path) and fileTime(path) > min_file_date:
            return True
        sleep(60)

    return False


def lcgNightly(path, required, timeout=timedelta(hours=17)):
    '''
    Compare the externals declared in the file LCG_externals_<platform>.txt
    specified and the list of ones, waiting until all the required externals
    are present. Note: the check is case insensitive.

    @return: True if the condition is met within the timeout, False otherwise
    '''
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)

    required = set(req.lower() for req in required)

    logging.debug('waiting for externals in %s', path)

    when_to_stop = datetime.now() + timeout
    two_days_ago = datetime.now() - timedelta(days=2)

    def created(path):
        '''
        Return datetime of creation of a file.
        '''
        return datetime.fromtimestamp(os.stat(path).st_ctime)

    found = None
    while datetime.now() < when_to_stop:
        # we ignore missing or too old files
        if exists(path) and created(path) > two_days_ago:
            with open(path) as ext:
                found = set(l.split(';', 1)[0].strip().lower() for l in ext)
            if required.issubset(found):
                return True
        sleep(60)

    if found is None:
        msg = '{0} missing or too old'.format(path)
    else:
        msg = ('some required libs are missing: {0}'.format(', '.join(
            sorted(required - found))))
    logging.warning(msg)
    return False


class Script(PlainScript):
    '''
    Script to check slot preconditions.
    '''
    __usage__ = '%prog [options] <slot name or config file>'
    __version__ = ''

    def main(self):
        '''
        Script main function.
        '''
        if len(self.args) != 1:
            self.parser.error('wrong number of arguments')

        from LbNightlyTools.Configuration import findSlot
        slot = findSlot(self.args[0])

        from LbNightlyTools.Utils import setDayNamesEnv
        setDayNamesEnv()

        starttime = datetime.now()
        for precond in slot.preconditions:
            name = precond['name']
            args = precond.get('args', {})
            f = globals()[name]
            self.log.info('running %s(%s)', name, args)
            if f(**args):
                self.log.debug('precondition met')
            else:
                self.log.error('precondition failed')
                return 1

        self.log.info('all preconditions are met (time taken: %s).',
                      datetime.now() - starttime)
        return 0
