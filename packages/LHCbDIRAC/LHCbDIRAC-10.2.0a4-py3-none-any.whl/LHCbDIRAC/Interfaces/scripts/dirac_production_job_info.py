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

import DIRAC
from DIRAC.Core.Utilities.DIRACScript import DIRACScript


def usage():
  """usage Prints script usage."""
  from DIRAC.Core.Base import Script
  print('Usage: %s <Production ID> <Production Job ID>' % Script.scriptName)
  DIRAC.exit(2)


@DIRACScript()
def main():
  from DIRAC.Core.Base import Script
  Script.parseCommandLine(ignoreErrors=True)
  from LHCbDIRAC.Interfaces.API.DiracProduction import DiracProduction

  args = Script.getPositionalArgs()

  if len(args) != 2:
    usage()

  diracProd = DiracProduction()
  prodID = args[0]
  jobID = args[1]
  try:
    prodID = int(prodID)
    jobID = int(jobID)
  except Exception as x:
    print('ERROR ProdID and Production JobID must be integers')
    DIRAC.exit(2)

  result = diracProd.getProdJobInfo(prodID, jobID, printOutput=True)
  if result['OK']:
    DIRAC.exit(0)
  elif 'Message' in result:
    print('Getting production job info failed with message:\n%s' % (result['Message']))
    DIRAC.exit(2)
  else:
    print('Null result for getProdJobInfo() call')
    DIRAC.exit(2)


if __name__ == "__main__":
  main()
