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
"""Remove the given file or a list of files from the File Catalog and from the
storage."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__RCSID__ = "$Id$"

from DIRAC.Core.Utilities.DIRACScript import DIRACScript


@DIRACScript()
def main():
  from LHCbDIRAC.DataManagementSystem.Client.DMScript import DMScript, Script

  dmScript = DMScript()
  dmScript.registerBKSwitches()
  dmScript.registerFileSwitches()

  Script.registerSwitch(
      '',
      'IncludeProcessedFiles',
      '  Forced to set Removed the files in status Processed (default:not reset)')
  Script.setUsageMessage('\n'.join([__doc__,
                                    'Usage:',
                                    '  %s [option|cfgfile] [<LFN>] [<LFN>...]' % Script.scriptName, ]))

  Script.parseCommandLine()

  from LHCbDIRAC.DataManagementSystem.Client.ScriptExecutors import executeRemoveFiles
  from DIRAC import exit
  exit(executeRemoveFiles(dmScript))


if __name__ == "__main__":
  main()
