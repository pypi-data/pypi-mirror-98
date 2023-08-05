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
"""stores the input files."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from LHCbDIRAC.BookkeepingSystem.Service.XMLReader.Job.File import File

__RCSID__ = "$Id$"

#############################################################################


class InputFile(File):
  """InputFile class."""
  #############################################################################

  def writeToXML(self):
    """creates an xml string."""
    result = '  <InputFile    Name="' + self.getFileName() + '"/>\n'
    return result
