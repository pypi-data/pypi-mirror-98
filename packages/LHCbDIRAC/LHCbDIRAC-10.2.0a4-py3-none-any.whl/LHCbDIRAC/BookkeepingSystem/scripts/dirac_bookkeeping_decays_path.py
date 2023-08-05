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
"""Get Bookkeeping paths given a decay.

@author Vanya BELYAEV Ivan.Belyaev@itep.ru
        Federico Stagni fstagni@cern.ch
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__RCSID__ = "$Id$"

import six
import DIRAC
from DIRAC import gLogger
from DIRAC.Core.Utilities.DIRACScript import DIRACScript


@DIRACScript()
def main():
  from DIRAC.Core.Base import Script
  from LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient import BookkeepingClient

  Script.setUsageMessage(__doc__ + '\n'.join([
      'Usage:',
      '  %s eventType  ' % Script.scriptName]))

  Script.registerSwitch('p', 'production', "Obtain the paths in ``Production format'' for Ganga")
  Script.parseCommandLine(ignoreErrors=True)

  productionFormat = False
  for p, _v in Script.getUnprocessedSwitches():
    if p.lower() in ('p', 'production'):
      productionFormat = True
    break

  args = Script.getPositionalArgs()
  if len(args) < 1:
    Script.showHelp(exitCode=1)

  eventType = args[0]

  bkClient = BookkeepingClient()

  # # get productions for given event type
  res = bkClient.getProductionSummaryFromView({'EventType': eventType, 'Visible': True})
  if not res['OK']:
    gLogger.error('Could not retrieve production summary for event %s' % eventType, res['Message'])
    DIRAC.exit(1)
  prods = res['Value']

  # # get production-IDs
  prodIDs = [p['Production'] for p in prods]

  # # loop over all productions
  for prodID in sorted(prodIDs):

    res = bkClient.getProductionInformation(prodID)
    if not res['OK']:
      gLogger.error('Could not retrieve production infos for production %s' % prodID, res['Message'])
      continue
    prodInfo = res['Value']
    steps = prodInfo['Steps']
    if isinstance(steps, six.string_types):
      continue
    files = prodInfo["Number of files"]
    events = prodInfo["Number of events"]
    path = prodInfo["Path"]
    dddb = prodInfo["Steps"][0][4]
    conddb = prodInfo["Steps"][0][5]

    evts = 0
    ftype = None
    for i in events:
      if i[0] in ['GAUSSHIST', 'LOG', 'SIM', 'DIGI']:
        continue
      evts += i[1]
      if not ftype:
        ftype = i[0]

    nfiles = 0
    for f in files:
      if f[1] in ['GAUSSHIST', 'LOG', 'SIM', 'DIGI']:
        continue
      if f[1] != ftype:
        continue
      nfiles += f[0]

    p0, n, p1 = path.partition('\n')
    if n:
      path = p1

    if productionFormat:
      p, s, e = path.rpartition('/')
      if s and e:
        path = '/%d/%d/%s' % (prodID, int(eventType), e)
    print(path, dddb, conddb, nfiles, evts, prodID)


if __name__ == "__main__":
  main()
