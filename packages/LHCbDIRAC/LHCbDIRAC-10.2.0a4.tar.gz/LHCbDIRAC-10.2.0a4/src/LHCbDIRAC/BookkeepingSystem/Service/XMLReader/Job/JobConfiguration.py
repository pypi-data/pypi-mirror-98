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
"""stores the job configuration."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__RCSID__ = "$Id$"


class JobConfiguration:

  """JobConfiguration class."""
  #############################################################################

  def __init__(self):
    """initialize the class members."""
    self.configName_ = ""  # None
    self.configVersion_ = ""  # None
    self.date_ = ""  # None
    self.time_ = ""  # None

  #############################################################################
  def setConfigName(self, name):
    """sets the configuration name."""
    self.configName_ = name

  #############################################################################
  def getConfigName(self):
    """returns the configuration name."""
    return self.configName_

  #############################################################################
  def setConfigVersion(self, version):
    """sets the configuration version."""
    self.configVersion_ = version

  #############################################################################
  def getConfigVersion(self):
    """returns the configuration version."""
    return self.configVersion_

  #############################################################################
  def setDate(self, date):
    """sets the creation data."""
    self.date_ = date

  #############################################################################
  def getDate(self):
    """returns the creation data."""
    return self.date_

  #############################################################################
  def setTime(self, time):
    """sets the creation time."""
    self.time_ = time

  #############################################################################
  def getTime(self):
    """returns the creation time."""
    return self.time_

  #############################################################################
  def __repr__(self):
    """formats the output of the print."""
    result = 'JobConfiguration: \n'
    result += 'ConfigName:' + self.configName_ + '\n'
    result += 'ConfigVersion:' + self.configVersion_ + '\n'
    result += 'Date and Time:' + self.date_ + ' ' + self.time_
    return result

  def writeToXML(self):
    """creates an xml string."""
    result = '<Job ConfigName="' + self.getConfigName() + \
        '" ConfigVersion="' + self.getConfigVersion() + \
        '" Date="' + self.getDate() + \
        '" Time="' + self.getTime() + '">\n'
    return result

  #############################################################################
