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
"""Bookkeeping Command line interface."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from DIRAC.Core.Utilities.DIRACScript import DIRACScript


@DIRACScript()
def main():
  from DIRAC.Core.Base import Script
  Script.parseCommandLine(ignoreErrors=True)

  from LHCbDIRAC.BookkeepingSystem.Client.LHCbBookkeepingCLI import LHCbBookkeepingCLI

  bk = LHCbBookkeepingCLI()
  bk.cmdloop()


if __name__ == "__main__":
  main()
