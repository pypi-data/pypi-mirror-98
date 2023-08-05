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
"""Utility for invoking running LHCb applications."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__RCSID__ = "$Id$"

import sys
import os
import shlex

from DIRAC import gLogger
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.Core.Utilities.Subprocess import systemCall


class LbRunError(RuntimeError):
  """Exception for lb-run errors."""
  pass


class LHCbApplicationError(RuntimeError):
  """Exception for application errors."""
  pass


class LHCbDIRACError(RuntimeError):
  """Exception for application errors."""
  pass


class RunApplication(object):
  """Encapsulate logic for running an LHCb application."""

  def __init__(self):
    """ c'tor - holds common variables
    """
    # Standard LHCb scripts
    self.runApp = 'lb-run'
    self.lbrunCommand = ''  # Command that will be constructed at run time

    # What to run
    self.applicationName = ''  # e.g. Gauss
    self.applicationVersion = ''  # e.g v42r1

    # Define the environment
    self.extraPackages = []
    self.systemConfig = 'ANY'
    self.runTimeProject = ''
    self.runTimeProjectVersion = ''
    self.site = ''

    # What to run and how
    self.command = 'gaudirun.py'
    self.commandOptions = []
    self.prodConf = False
    self.prodConfFileName = 'prodConf.py'
    self.step_number = 0
    self.extraOptionsLine = ''
    self.numberOfProcessors = 1

    self.applicationLog = 'applicationLog.txt'
    self.stdError = 'applicationError.txt'

    # Utilities
    self.log = gLogger.getSubLogger("RunApplication")
    self.opsH = Operations()

    # Prmon
    self.prmonPath = '/cvmfs/lhcb.cern.ch/lib/experimental/prmon/bin/prmon'
    self.usePrmon = False

  def run(self):
    """Invokes lb-run (what you call after having setup the object)"""
    self.log.info("Executing application %s %s for binary tag configuration '%s'" % (self.applicationName,
                                                                                     self.applicationVersion,
                                                                                     self.systemConfig))

    lbRunOptions = self.opsH.getValue('GaudiExecution/lbRunOptions', '--siteroot=/cvmfs/lhcb.cern.ch/lib/')

    extraPackagesString, runtimeProjectString, externalsString = self._lbRunCommandOptions()

    # if a binary tag is provided, then only that should be called.
    # This should be safeguarded with the following method.
    # if not, we call "-c best"
    if self.systemConfig.lower() == 'any':
      self.systemConfig = 'best'
    configString = "-c %s" % self.systemConfig

    # App
    app = self.applicationName
    if self.applicationVersion:
      app += '/' + self.applicationVersion

    # Command
    if self.command == 'gaudirun.py':
      command = self._gaudirunCommand()
    else:
      command = self.command

    self.lbrunCommand = ' '.join([self.runApp, lbRunOptions,
                                  configString, extraPackagesString,
                                  runtimeProjectString, externalsString,
                                  app])

    finalCommand = ' '.join([self.lbrunCommand, command])

    # then run it!
    runResult = self._runApp(finalCommand, env=self._getEnv())
    if not runResult['OK']:
      self.log.error("Problem executing lb-run: %s" % runResult['Message'])
      self.log.error("Environment: %s" % os.environ)
      raise LHCbDIRACError("Can not start %s %s" % (self.applicationName, self.applicationVersion))

    if runResult['Value'][0]:  # if exit status != 0
      self.log.error("lb-run or its application exited with status %d" % runResult['Value'][0])
      self.log.error(runResult['Value'][2])

      # this is an lb-run specific error
      if runResult['Value'][0] & 0x40 and not runResult['Value'][0] & 0x80:
        self.log.error("Status %d is an lb-run specific error" % runResult['Value'][0])
        self.log.error("Trying running the same lb-run command with --debug option, it should fail immediately anyway")
        lbrunCommandWithDebug = ' '.join([self.runApp, '--debug', lbRunOptions,
                                          configString, extraPackagesString,
                                          runtimeProjectString, externalsString,
                                          app])
        debugCommand = ' '.join([lbrunCommandWithDebug, command])
        self._runApp(debugCommand)
        raise LbRunError("Problem setting the environment: lb-run exited with status %d" % runResult['Value'][0])

      self.log.error("Status %d is an application (%s %s) error" % (runResult['Value'][0],
                                                                    self.applicationName,
                                                                    self.applicationVersion))
      raise LHCbApplicationError("%s %s exited with status %d" % (self.applicationName,
                                                                  self.applicationVersion,
                                                                  runResult['Value'][0]))

    self.log.info("%s execution completed successfully" % self.applicationName)

    return runResult

  def _lbRunCommandOptions(self):
    """Return lb-run command options."""

    # extra packages (for setup phase) (added using '--use')
    extraPackagesString = ''
    for ep in self.extraPackages:
      if len(ep) == 1:
        epName = ep[0]
        epVer = ''
      elif len(ep) == 2:
        epName, epVer = ep

      if epName.lower() == 'prodconf':
        self.prodConf = True
      if epVer:
        extraPackagesString += ' --use="%s %s" ' % (epName, epVer)
      else:
        extraPackagesString += ' --use="%s"' % epName

    # run time project
    runtimeProjectString = ''
    if self.runTimeProject:
      self.log.verbose('Requested run time project: %s' % (self.runTimeProject))
      runtimeProjectString = ' --runtime-project %s/%s' % (self.runTimeProject, self.runTimeProjectVersion)

    externalsString = ''

    externals = []
    if self.site:
      externals = self.opsH.getValue('ExternalsPolicy/%s' % (self.site), [])
      if externals:
        self.log.info('Found externals policy for %s = %s' % (self.site, externals))
        for external in externals:
          externalsString += ' --ext=%s' % external

    if not externalsString:
      externals = self.opsH.getValue('ExternalsPolicy/Default', [])
      if externals:
        self.log.info('Using default externals policy for %s = %s' % (self.site, externals))
        for external in externals:
          externalsString += ' --ext=%s' % external

    return extraPackagesString, runtimeProjectString, externalsString

  def _gaudirunCommand(self):
    """construct a gaudirun command."""
    command = self.opsH.getValue('/GaudiExecution/gaudirunFlags', 'gaudirun.py')

    # multicore?
    if self.numberOfProcessors > 1:
      command += ' --ncpus %d ' % int(self.numberOfProcessors)

    if self.commandOptions:
      command += ' '
      command += ' '.join(self.commandOptions)

    if self.prodConf:
      command += ' '
      command += self.prodConfFileName

    if self.extraOptionsLine:
      command += ' '
      with open('gaudi_extra_options.py', 'w') as fopen:
        fopen.write(self.extraOptionsLine)
      command += 'gaudi_extra_options.py'

    return command

  def _runApp(self, command, env=None):
    """Safe system call of a command.

    :param command basestring: the command to run
    :param env dict: environment where to run -- maybe the LHCb environment from LbLogin
    """
    if self.applicationName == 'Gauss' and self.usePrmon:
      command = self.prmonPath + ' --json-summary ./prmon_Gauss.json -- ' + command

    print('Command called: \n%s' % command)  # Really printing here as we want to see and maybe cut/paste

    return systemCall(timeout=0,
                      cmdSeq=shlex.split(command),
                      callbackFunction=self.__redirectLogOutput,
                      env=env)

  def _getEnv(self):
    """Get a dictionary containing the environment that should be used for the job
    """
    # Start from the current environment
    env = os.environ.copy()
    # Versions of Brunel used for 2018 data use XGBoost which uses OpenMP to
    # provide parallelism and automatically spawns one thread for each CPU.
    # Use OMP_NUM_THREADS to force it to only use one thread
    env["OMP_NUM_THREADS"] = str(self.numberOfProcessors)
    return env

  def __redirectLogOutput(self, fd, message):
    """Callback function for the Subprocess calls (manages log files)

    Args:
        fd (int): stdin/stderr file descriptor
        message (str): line to log
    """
    sys.stdout.flush()
    if message:
      if 'INFO Evt' in message or 'Reading Event record' in message:  # These ones will appear in the std.out log too
        print(message)
      if self.applicationLog:
        with open(self.applicationLog, 'a') as log:
          log.write(message + '\n')
          log.flush()
      else:
        self.log.error("Application Log file not defined")
      if fd == 1:
        if self.stdError:
          with open(self.stdError, 'a') as error:
            error.write(message + '\n')
            error.flush()
