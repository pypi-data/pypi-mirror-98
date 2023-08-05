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
"""interpret the data taking conditions."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
__RCSID__ = "$Id$"

#############################################################################


class Context(object):
  """the data taking condition."""

  def __init__(self, cond, part='LHCb'):
    """initialize the variables."""
    self.__input = cond
    self.__output = ''
    self.__partition = part

  def getInput(self):
    """get input."""
    return self.__input

  def setOutput(self, text):
    """output string."""
    if text is not None:
      self.__output += str(text)

  def getOutput(self):
    """get output."""
    return self.__output.strip('-')

  def getParticionName(self):
    """partition."""
    return self.__partition

#############################################################################


class Conditions(object):
  """different conditions."""

  def __init__(self):
    """initialize the variables."""
    self.__condition = 'NOT INCLUDED'

  def getCondition(self):
    """conditions."""
    return self.__condition

  def interpret(self, context):
    """interpret the context."""
    if self.beamCond() in context.getInput():
      context.setOutput(self.template(context.getInput()[self.beamCond()]))

    if self.beamenergy() in context.getInput():
      context.setOutput(self.template(context.getInput()[self.beamenergy()]))

    if self.veloCond() in context.getInput():
      if context.getParticionName().upper() == 'LHCB' or context.getParticionName().upper() == 'VELO':
        context.setOutput(self.template(context.getInput()[self.veloCond()]))

    if self.magneticField() in context.getInput():
      context.setOutput(self.template(context.getInput()[self.magneticField()]))

    if self.ecal() in context.getInput():
      if context.getInput()[self.ecal()] == self.getCondition():
        if context.getParticionName().upper() == 'LHCB':
          self.excl(context)
          context.setOutput(self.template(context.getInput()[self.ecal()]))

    if self.hcal() in context.getInput():
      if context.getInput()[self.hcal()] == self.getCondition():
        if context.getParticionName().upper() == 'LHCB':
          self.excl(context)
          context.setOutput(self.template(context.getInput()[self.hcal()]))

    if self.hlt() in context.getInput():
      if context.getInput()[self.hlt()] == self.getCondition():
        if context.getParticionName().upper() == 'LHCB':
          self.excl(context)
          context.setOutput(self.template(context.getInput()[self.hlt()]))

    if self.it() in context.getInput():
      if context.getInput()[self.it()] == self.getCondition():
        if context.getParticionName().upper() == 'LHCB':
          self.excl(context)
          context.setOutput(self.template(context.getInput()[self.it()]))

    if self.lo() in context.getInput():
      if context.getInput()[self.lo()] == self.getCondition():
        if context.getParticionName().upper() == 'LHCB':
          self.excl(context)
          context.setOutput(self.template(context.getInput()[self.lo()]))

    if self.muon() in context.getInput():
      if context.getInput()[self.muon()] == self.getCondition():
        if context.getParticionName().upper() == 'LHCB':
          self.excl(context)
          context.setOutput(self.template(context.getInput()[self.muon()]))

    if self.ot() in context.getInput():
      if context.getInput()[self.ot()] == self.getCondition():
        if context.getParticionName().upper() == 'LHCB':
          self.excl(context)
          context.setOutput(self.template(context.getInput()[self.ot()]))

    if self.rich1() in context.getInput():
      if context.getInput()[self.rich1()] == self.getCondition():
        if context.getParticionName().upper() == 'LHCB':
          self.excl(context)
          context.setOutput(self.template(context.getInput()[self.rich1()]))

    if self.rich2() in context.getInput():
      if context.getInput()[self.rich2()] == self.getCondition():
        if context.getParticionName().upper() == 'LHCB':
          self.excl(context)
          context.setOutput(self.template(context.getInput()[self.rich2()]))

    if self.spd_prs() in context.getInput():
      if context.getInput()[self.spd_prs()] == self.getCondition():
        if context.getParticionName().upper() == 'LHCB':
          self.excl(context)
          context.setOutput(self.template(context.getInput()[self.spd_prs()]))

    if self.tt() in context.getInput():
      if context.getInput()[self.tt()] == self.getCondition():
        if context.getParticionName().upper() == 'LHCB':
          self.excl(context)
          context.setOutput(self.template(context.getInput()[self.tt()]))

    if self.velo() in context.getInput():
      if context.getInput()[self.velo()] == self.getCondition():
        if context.getParticionName().upper() == 'LHCB':
          self.excl(context)
          context.setOutput(self.template(context.getInput()[self.velo()]))

  def beamCond(self):
    """define a condition."""
    pass

  def beamenergy(self):
    """define a condition."""
    pass

  def velo(self):
    """define a condition."""
    pass

  def magneticField(self):
    """define a condition."""
    pass

  def ecal(self):
    """define a condition."""
    pass

  def hcal(self):
    """define a condition."""
    pass

  def hlt(self):
    """define a condition."""
    pass

  def it(self):
    """define a condition."""
    pass

  def lo(self):
    """define a condition."""
    pass

  def muon(self):
    """define a condition."""
    pass

  def ot(self):
    """define a condition."""
    pass

  def rich1(self):
    """define a condition."""
    pass

  def rich2(self):
    """define a condition."""
    pass

  def spd_prs(self):
    """define a condition."""
    pass

  def tt(self):
    """define a condition."""
    pass

  def veloCond(self):
    """define a condition."""
    pass

  def template(self, value):
    """define a condition."""
    pass

  def template2(self, value):
    """define a condition."""
    return ''

  @staticmethod
  def excl(context):
    """define a condition."""
    if context.getOutput().find('Excl') < 0:
      context.setOutput('Excl-')

#############################################################################


class BeamCondition(Conditions):
  """condition class."""

  def beamCond(self):
    """beamcondition."""
    return 'BeamCond'

  def template(self, value):
    """template method."""
    return value

#############################################################################


class BeamEnergyCondition(Conditions):
  """Energy."""

  def beamenergy(self):
    """beam energy."""
    return 'BeamEnergy'

  def template(self, value):
    """Template method."""
    try:
      if value is not None:
        if (value.strip() != 'None'):
          if value == 'UNKOWN' or float(value) == 0 or float(value) == 7864 or float(value) >= 7864:
            return 'BeamOff-'
          else:
            return 'Beam' + str(int(float(value))) + 'GeV-'
    except Exception as e:
      print(e)
    return 'BeamOff-'

#############################################################################


class MagneticFieldCondition(Conditions):
  """magnetic field."""

  def magneticField(self):
    """magfild."""
    return 'MagneticField'

  def template(self, value):
    """..."""
    if value.upper() == 'OFF':
      return 'MagOff-'
    elif value.upper() == 'DOWN':
      return 'MagDown-'
    elif value.upper() == 'UP':
      return 'MagUp-'
    else:
      return 'Mag' + value + '-'

#############################################################################


class VeloPosition(Conditions):
  """Velo position class."""

  def velo(self):
    """Open or Closed."""
    return 'VELO'

  def template(self, value):
    """tempalte method."""
    if value == self.getCondition():
      return 'VE-'

#############################################################################


class EcalCondition(Conditions):
  """ECAL class."""

  def ecal(self):
    """status of the subdetector."""
    return 'ECAL'

  def template(self, value):
    """template method."""
    if value == self.getCondition():
      return 'EC-'
#############################################################################


class HcalCondition(Conditions):
  """HCAL class."""

  def hcal(self):
    """status of the subdetector."""
    return 'HCAL'

  def template(self, value):
    """template method."""
    if value == self.getCondition():
      return 'HC-'

#############################################################################


class HltCondition(Conditions):
  """HLT class."""

  def Hhlt(self):
    """status of the subdetector."""
    return 'HLT'

  def template(self, value):
    """template methos."""
    if value == self.getCondition():
      return 'HL-'

#############################################################################


class ItCondition(Conditions):
  """It class."""

  def it(self):
    """status of the subdetector."""
    return 'IT'

  def template(self, value):
    """template method."""
    if value == self.getCondition():
      return 'IT-'

#############################################################################


class LoCondition(Conditions):
  """Lo class."""

  def lo(self):
    """status of the subdetector."""
    return 'LO'

  def template(self, value):
    """template method."""
    if value == self.getCondition():
      return 'LO-'

#############################################################################


class MuonCondition(Conditions):
  """Muon class."""

  def muon(self):
    """status of the subdetector."""
    return 'MUON'

  def template(self, value):
    """template method."""
    if value == self.getCondition():
      return 'MU-'

#############################################################################


class OtCondition(Conditions):
  """Ot class."""

  def ot(self):
    """status of the subdetector."""
    return 'OT'

  def template(self, value):
    """template method."""
    if value == self.getCondition():
      return 'OT-'

#############################################################################


class Rich1Condition(Conditions):
  """RICH1 class."""

  def rich1(self):
    """status of the subdetector."""
    return 'RICH1'

  def template(self, value):
    """template method."""
    if value == self.getCondition():
      return 'R1-'

#############################################################################


class Rich2Condition(Conditions):
  """RICH2 class."""

  def rich2(self):
    """status of the subdetector."""
    return 'RICH2'

  def template(self, value):
    """template method."""
    if value == self.getCondition():
      return 'R2-'

#############################################################################


class Spd_prsCondition(Conditions):
  """SPD class."""

  def spd_prs(self):
    """status of the subdetector."""
    return 'SPD_PRS'

  def template(self, value):
    """template method."""
    if value == self.getCondition():
      return 'SP-'

#############################################################################


class TtCondition(Conditions):
  """TT class."""

  def tt(self):
    """status of the subdetector."""
    return 'TT'

  def template(self, value):
    """template method."""
    if value == self.getCondition():
      return 'TT-'

#############################################################################


class VeloCondition(Conditions):
  """Velo class."""

  def veloCond(self):
    """status of the subdetector."""
    return 'VeloPosition'

  def template(self, value):
    """template method."""
    if value.upper() == 'OPEN':
      return 'VeloOpen-'
    elif value.upper() == 'CLOSED':
      return 'VeloClosed-'
    else:
      return 'Velo' + value + '-'

#############################################################################


if __name__ == "__main__":
  datataking = {'Description': 'Blalbla',
                'BeamCond': 'UNKNOWN',
                'BeamEnergy': '0.0',
                'MagneticField': 'OFF',
                'VELO': 'NOT INCLUDED',
                'IT': 'NOT INCLUDED',
                'TT': 'NOT INCLUDED',
                'OT': 'NOT INCLUDED',
                'RICH1': 'NOT INCLUDED',
                'RICH2': 'NOT INCLUDED',
                'SPD_PRS': 'INCLUDED',
                'ECAL': 'NOT INCLUDED',
                'HCAL': 'NOT INCLUDED',
                'MUON': 'NOT INCLUDED',
                'L0': 'NOT INCLUDED',
                'HLT': 'UNKOWN',
                'VeloPosition': 'OPEN'}

  datataking = {'VELO': 'INCLUDED',
                'RICH2': 'INCLUDED',
                'RICH1': 'INCLUDED',
                'BeamEnergy': '4000.0',
                'SPD_PRS': 'INCLUDED',
                'ECAL': 'INCLUDED',
                'TT': 'INCLUDED',
                'MagneticField': 'DOWN',
                'IT': 'INCLUDED',
                'BeamCond': 'UNKNOWN',
                'MUON': 'INCLUDED',
                'L0': 'INCLUDED',
                'HLT': 'UNKNOWN',
                'HCAL': 'INCLUDED',
                'VeloPosition': 'CLOSED',
                'OT': 'INCLUDED'}
  print(datataking)

  context = Context(datataking, 'PRS')
  conditions = [BeamEnergyCondition(), VeloCondition(), MagneticFieldCondition(),
                EcalCondition(), HcalCondition(), HltCondition(), ItCondition(), LoCondition(),
                MuonCondition(), OtCondition(), Rich1Condition(), Rich2Condition(), Spd_prsCondition(),
                TtCondition(), VeloPosition()]

  for condition in conditions:
    condition.interpret(context)

  print(context.getOutput())
