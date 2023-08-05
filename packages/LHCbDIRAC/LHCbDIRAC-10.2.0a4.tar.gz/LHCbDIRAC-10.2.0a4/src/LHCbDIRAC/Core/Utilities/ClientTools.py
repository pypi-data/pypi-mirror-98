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
"""The ClientTools module provides additional functions for use by users of the
DIRAC client in the LHCb environment."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tempfile

from DIRAC import gLogger, S_OK, S_ERROR
from DIRAC.Core.Utilities.List import breakListIntoChunks

from LHCbDIRAC.Core.Utilities.RunApplication import RunApplication

__RCSID__ = "$Id$"


def _errorReport(error, message=None):
  """Internal function to return errors and exit with an S_ERROR()"""
  if not message:
    message = error

  gLogger.warn(error)
  return S_ERROR(message)


def mergeRootFiles(outputFile, inputFiles):
  """Merge several ROOT files.

  Args:
      outputFile (str): output file name
      inputFiles (list): list of input files
  """
  if not isinstance(inputFiles, list):
    return _errorReport("please provide a list of input files")

  # Performs the merging
  chunkSize = 20

  if len(inputFiles) > chunkSize:  # 2-steps merge
    lists = breakListIntoChunks(inputFiles, chunkSize)
    tempFiles = []
    for filelist in lists:
      fd, fn = tempfile.mkstemp()
      os.close(fd)
      tempFiles.append(fn)
      res = _mergeRootFiles(fn, filelist)
      if not res['OK']:
        return _errorReport(res['Message'], "Failed to perform ROOT merger")
    res = _mergeRootFiles(outputFile, tempFiles)
    if not res['OK']:
      return _errorReport(res['Message'], "Failed to perform final ROOT merger")
    # Cleaning up temporary files
    for filename in tempFiles:
      if os.path.exists(filename):
        os.remove(filename)

  else:  # merge in one go
    res = _mergeRootFiles(outputFile, inputFiles)
    if not res['OK']:
      return _errorReport(res['Message'], "Failed to perform ROOT merger")

  return S_OK(outputFile)

#############################################################################


def _mergeRootFiles(outputFile, inputFiles):
  """Merge ROOT files.

  Args:
      outputFile (str): output file name
  """
  cmd = "hadd -f %s " % outputFile + ' '.join(inputFiles)

  ra = RunApplication()
  ra.applicationName = 'ROOT'
  ra.command = cmd

  try:
    ra.run()
    return S_OK()
  except RuntimeError:
    return _errorReport("Failed to merge root files")
