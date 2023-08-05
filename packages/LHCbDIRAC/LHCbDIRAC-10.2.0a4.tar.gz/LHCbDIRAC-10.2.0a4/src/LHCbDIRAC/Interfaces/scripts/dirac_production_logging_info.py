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
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__RCSID__ = "$Id$"

import DIRAC
from DIRAC.Core.Utilities.DIRACScript import DIRACScript


def usage():
  """usage Prints script usage."""
  from DIRAC.Core.Base import Script
  print('Usage: %s <Production ID> |<Production ID>' % Script.scriptName)
  DIRAC.exit(2)


@DIRACScript()
def main():
  from DIRAC.Core.Base import Script
  Script.parseCommandLine(ignoreErrors=True)

  from LHCbDIRAC.Interfaces.API.DiracProduction import DiracProduction

  args = Script.getPositionalArgs()

  if len(args) < 1:
    usage()

  diracProd = DiracProduction()
  exitCode = 0
  errorList = []

  for prodID in args:
    result = diracProd.getProductionLoggingInfo(prodID, printOutput=True)
    if 'Message' in result:
      errorList.append((prodID, result['Message']))
      exitCode = 2
    elif not result:
      errorList.append((prodID, 'Null result for getProduction() call'))
      exitCode = 2
    else:
      exitCode = 0

  for error in errorList:
    print("ERROR %s: %s" % error)

  DIRAC.exit(exitCode)


if __name__ == "__main__":
  main()
