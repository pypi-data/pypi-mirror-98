#!/usr/bin/env python
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
"""Returns list of Conditions for a run range, by default only if there is a FULL stream."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__RCSID__ = "$Id$"

from DIRAC.Core.Utilities.DIRACScript import DIRACScript


@DIRACScript()
def main():
  from LHCbDIRAC.DataManagementSystem.Client.DMScript import Script

  Script.registerSwitch('', 'Runs=', 'Run range or list')
  Script.registerSwitch('', 'ByRange', 'List by range rather than by item value')
  Script.registerSwitch('', 'Force', 'Include runs even if no FULL stream is present')
  Script.setUsageMessage(__doc__ + '\n'.join([
      'Usage:',
      '  %s [option|cfgfile] ... ' % Script.scriptName]))

  Script.parseCommandLine(ignoreErrors=True)

  from LHCbDIRAC.BookkeepingSystem.Client.ScriptExecutors import executeRunInfo
  executeRunInfo('DataTakingDescription')


if __name__ == "__main__":
  main()
