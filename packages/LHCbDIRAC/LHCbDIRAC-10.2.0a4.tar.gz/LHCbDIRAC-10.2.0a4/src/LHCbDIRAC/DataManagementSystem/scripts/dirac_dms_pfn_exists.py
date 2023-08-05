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
"""Check existence of a (list of) LHCb LFNs/PFNs given a valid DIRAC SE (or for
all replicas) Only the LFN contained in the PFN is considered, unlike the DIRAC
similar script."""
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
  Script.registerSwitch('', 'Summary', '   Only prints a summary on existing files')
  Script.setUsageMessage('\n'.join([__doc__,
                                    'Usage:',
                                    '  %s [option|cfgfile] ... [URL[,URL2[,URL3...]]] SE[ SE2...]' % Script.scriptName,
                                    'Arguments:',
                                    '  URL:      Logical/Physical File Name or file containing URLs',
                                    '  SE:       Valid DIRAC SE']))
  Script.parseCommandLine(ignoreErrors=True)

  from LHCbDIRAC.DataManagementSystem.Client.ScriptExecutors import executePfnMetadata
  from DIRAC import exit
  exit(executePfnMetadata(dmScript, check=True, exists=True))


if __name__ == "__main__":
  main()
