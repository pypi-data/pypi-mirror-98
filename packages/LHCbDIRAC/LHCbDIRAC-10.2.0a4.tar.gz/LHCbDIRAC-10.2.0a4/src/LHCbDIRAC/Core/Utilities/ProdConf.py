###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""ProdConf is a utility to manipulate a ProdConf file.

If the file does not exist, it will be created. If it exists and has
options, new ones will be put in if not existing, or override the old
ones if already existing. This is used by the production API to create
production workflows but also provides lists of options files for test
jobs.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__RCSID__ = "$Id$"

import os
import re


class ProdConf(object):
  """Class for managing ProdConf objects."""

  def __init__(self, fileName='prodConf.py', log=None):
    """initialize a ProdConf object, setting some relevant info."""

    self.optionsDict = {'Application': 'string',
                        'AppVersion': 'string',
                        'OptionFormat': 'string',
                        'InputFiles': 'list',
                        'OutputFilePrefix': 'string',
                        'OutputFileTypes': 'list',
                        'XMLFileCatalog': 'string',
                        'XMLSummaryFile': 'string',
                        'HistogramFile': 'string',
                        'DDDBTag': 'string',
                        'CondDBTag': 'string',
                        'DQTag': 'string',
                        'NOfEvents': 'integer',
                        'RunNumber': 'integer',
                        'FirstEventNumber': 'integer',
                        'TCK': 'string',
                        'ProcessingPass': 'string'}

    if not log:
      from DIRAC import gLogger
      self.log = gLogger.getSubLogger('ProdConf')
    else:
      self.log = log

    self.fileName = fileName

    if not os.path.exists(fileName):
      self.log.verbose('Creating ProdConf file %s from scratch' % fileName)
      with open(fileName, 'a'):
        os.utime(fileName, None)

    self.whatsIn = {}
    self._getWhatsIn()

  def _getWhatsIn(self):
    """Get what's in, as options, and fill the dictionary."""

    with open(self.fileName, 'r') as fopen:
      fileString = fopen.read()

    lines = re.split('\n+', fileString)
    for line in lines:
      for option, pcType in self.optionsDict.items():
        if re.match('[ ]*' + option + '[a-z,A-Z,0-9.]*', line):
          optionValues = re.split(option + '=+', line)
          for optionValue in optionValues:
            optionValue = optionValue.strip(' ')
            if optionValue:
              if pcType == 'list':
                optionValueEls = optionValue.split('[')
              else:
                optionValueEls = optionValue.split(',')
              for optionValueEl in optionValueEls:
                if optionValueEl:
                  value = optionValueEl.replace('"', '').replace(']', '').replace("'", '').strip(' ')
                  if pcType == 'list':
                    if value == ',':
                      value = []
                    else:
                      value = [x.strip() for x in value.split(',')]
                      value.remove('')
                  elif pcType == 'integer':
                    value = int(value)
                  self.whatsIn[option] = value

  def putOptionsIn(self, optionsDict, freshStart=False):
    """Put options, specified in the optionsDict, in the options file."""

    if freshStart:
      try:
        os.remove(self.fileName)
        self._getWhatsIn()
      except OSError:
        pass

    optsThatWillGoIn = self._buildOptions(optionsDict)
    stringToPut = self._getOptionsString(optsThatWillGoIn)
    self.log.debug("Going to write in %s" % self.fileName)
    self.log.debug(stringToPut)

    # Easier to re-write it completely
    with open(self.fileName, 'w') as fopen:
      fopen.write(stringToPut)

    self._getWhatsIn()

  def _buildOptions(self, optionsDict):
    """just build the options Dict."""
    optsThatWillGoIn = optionsDict
    for optAlreadyIn in self.whatsIn:
      if optAlreadyIn in optsThatWillGoIn:
        self.log.warn('Option %s of %s will be overwritten' % (optAlreadyIn, self.fileName))
      else:
        optsThatWillGoIn[optAlreadyIn] = self.whatsIn[optAlreadyIn]

    return optsThatWillGoIn

  def _getOptionsString(self, optsThatWillGoIn):
    """Build a string with the options that will go in."""
    string = 'from ProdConf import ProdConf\n\n'
    string = string + 'ProdConf(\n'
    for opt, value in optsThatWillGoIn.items():
      if self.optionsDict[opt] == 'list':
        string = string + '  ' + opt + '=' + str(value) + ',' + '\n'
      elif self.optionsDict[opt] == 'string':
        string = string + '  ' + opt + "='" + value + "'," + '\n'
      else:
        string = string + '  ' + opt + "=" + str(value) + "," + '\n'
    string = string + ')'

    return string
