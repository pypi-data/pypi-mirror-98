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
"""Set a (set of) LFNs as problematic in the FC and in the BK and
transformation system if all replicas are problematic."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__RCSID__ = "$Id$"

from DIRAC.Core.Utilities.DIRACScript import DIRACScript


@DIRACScript()
def main():
  from LHCbDIRAC.DataManagementSystem.Client.DMScript import DMScript, Script

  dmScript = DMScript()
  dmScript.registerFileSwitches()
  dmScript.registerSiteSwitches()

  Script.registerSwitch('', 'Reset', '   Reset files to OK')
  Script.registerSwitch('', 'Full', '   Give full list of files')
  Script.registerSwitch('', 'NoAction', '   No action taken, just give stats')

  Script.setUsageMessage(__doc__ + '\n'.join([
      'Usage:',
      '  %s [option|cfgfile] [<LFN>] [<LFN>...]' % Script.scriptName, ]))

  Script.parseCommandLine(ignoreErrors=False)

  from LHCbDIRAC.DataManagementSystem.Client.ScriptExecutors import executeSetProblematicFiles
  from DIRAC import exit
  exit(executeSetProblematicFiles(dmScript))


if __name__ == "__main__":
  main()
