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
"""Gaudi Application Script Class.

This allows the execution of a simple python script in a given LHCb project environment,
e.g. python <script> <arguments>. GaudiPython / Bender scripts can be executed very simply
in this way.

To make use of this module the LHCbJob method setApplicationScript can be called by users.

This is usually the main module run by user jobs.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__RCSID__ = "$Id$"

import re
import os

from DIRAC import S_OK, S_ERROR, gLogger
from DIRAC.Core.Utilities import DErrno

from LHCbDIRAC.Core.Utilities.RunApplication import RunApplication, LbRunError, LHCbApplicationError, LHCbDIRACError
from LHCbDIRAC.Workflow.Modules.ModuleBase import ModuleBase


class GaudiApplicationScript(ModuleBase):

  #############################################################################

  def __init__(self, bkClient=None, dm=None):
    self.version = __RCSID__
    self.log = gLogger.getSubLogger("GaudiApplicationScript")
    super(GaudiApplicationScript, self).__init__(self.log, bkClientIn=bkClient, dm=dm)

    # Set defaults for all workflow parameters here
    self.script = None
    self.arguments = ''
    self.systemConfig = ''
    self.applicationLog = ''
    self.applicationName = ''
    self.applicationVersion = ''
    self.poolXMLCatName = 'pool_xml_catalog.xml'

  #############################################################################

  def _resolveInputVariables(self):
    """By convention the workflow parameters are resolved here."""

    super(GaudiApplicationScript, self)._resolveInputVariables()
    super(GaudiApplicationScript, self)._resolveInputStep()

    if 'script' in self.step_commons:
      self.script = self.step_commons['script']
    else:
      self.log.warn('No script defined')

    if 'arguments' in self.step_commons:
      self.arguments = self.step_commons['arguments']

    if 'poolXMLCatName' in self.step_commons:
      self.poolXMLCatName = self.step_commons['poolXMLCatName']

  #############################################################################

  def execute(self, production_id=None, prod_job_id=None, wms_job_id=None,
              workflowStatus=None, stepStatus=None,
              wf_commons=None, step_commons=None,
              step_number=None, step_id=None):
    """The main execution method of the module.

    It runs a gaudi script app using RunApplication module. This is
    usually the main module run by user jobs.
    """

    try:

      super(GaudiApplicationScript, self).execute(self.version,
                                                  production_id, prod_job_id, wms_job_id,
                                                  workflowStatus, stepStatus,
                                                  wf_commons, step_commons,
                                                  step_number, step_id)

      self._resolveInputVariables()

      if not self.applicationName or not self.applicationVersion:
        raise RuntimeError('No Gaudi Application defined')
      if not self.systemConfig:
        raise RuntimeError('No binary tag selected')
      if not self.script:
        raise RuntimeError('No script defined')
      if not self.applicationLog:
        self.applicationLog = '%s.log' % (os.path.basename(self.script))

      self.log.info("Executing application %s %s for binary tag %s" % (self.applicationName,
                                                                       self.applicationVersion,
                                                                       self.systemConfig))

      gaudiCmd = []
      if re.search('.py$', self.script):
        gaudiCmd.append('python')
        gaudiCmd.append(os.path.basename(self.script))
        gaudiCmd.append(self.arguments)
      else:
        gaudiCmd.append(os.path.basename(self.script))
        gaudiCmd.append(self.arguments)
      command = ' '.join(gaudiCmd)

      # How to run the application
      ra = RunApplication()
      # lb-run stuff
      ra.applicationName = self.applicationName
      ra.applicationVersion = self.applicationVersion
      ra.systemConfig = self.systemConfig
      # actual stuff to run
      ra.command = command
      ra.applicationLog = self.applicationLog
      ra.numberOfProcessors = self.numberOfProcessors

      # Now really running
      self.setApplicationStatus(self.applicationName)
      ra.run()  # This would trigger an exception in case of failure, or application status != 0

      self.setApplicationStatus('%s Successful' % os.path.basename(self.script))
      return S_OK('%s Successful' % os.path.basename(self.script))

    except LbRunError as lbre:  # This is the case for lb-run/environment errors
      self.setApplicationStatus(repr(lbre))
      return S_ERROR(DErrno.EWMSRESC, str(lbre))
    except LHCbApplicationError as lbae:  # This is the case for real application errors
      self.setApplicationStatus(repr(lbae))
      return S_ERROR(str(lbae))
    except LHCbDIRACError as lbde:  # This is the case for LHCbDIRAC errors (e.g. subProcess call failed)
      self.setApplicationStatus(repr(lbde))
      return S_ERROR(str(lbde))
    except Exception as e:  # pylint:disable=broad-except
      self.log.exception("Failure in GaudiApplicationScript execute module", lException=e)
      self.setApplicationStatus("Error in GaudiApplicationScript module")
      return S_ERROR(str(e))
    finally:
      super(GaudiApplicationScript, self).finalize(self.version)
