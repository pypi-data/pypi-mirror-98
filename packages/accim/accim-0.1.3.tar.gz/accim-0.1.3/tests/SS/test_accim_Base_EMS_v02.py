# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 17:03:48 2021

@author: Daniel
"""

from eppy import modeleditor
from eppy.modeleditor import IDF

import pytest

from accim.sim import accim_Base_EMS

# from accim.sim import accis
# accis.addAccis('sz', 'standard', 'ep94', [1], [3], [3], 0.1, 0.1, 0.1)

def lookfor(self, name, objectType):
    """
    Look for name in objectType list.
    """
    listToSearchIn = ([x.Name for x in self.idf0.idfobjects[objectType]])

    if name in listToSearchIn:
        return True
    else:
        return False


def test_addEMSProgramsBase(self, filename_temp):
    from accim.sim import accim_Main
    
    from eppy import modeleditor
    from eppy.modeleditor import IDF

    iddfile = 'C:/EnergyPlusV9-4-0/Energy+.idd'
    IDF.setiddname(iddfile)

    fname1 = filename_temp+'.idf'
    self.idf0 = IDF(fname1)
    self.idf0.savecopy(filename_temp+'_pymod.idf')

    self.filename = filename_temp+'_pymod'
    fname1 = self.filename+'.idf'
    self.idf1 = IDF(fname1)
    self.filename = filename_temp+'_pymod'

    print(self.filename)

    self.zonenames_orig = ([zone.Name for zone in self.idf1.idfobjects['ZONE']])
    # print(self.zonenames_orig)

    self.zonenames = ([sub.replace(':', '_') for sub in ([zone.Name for zone in self.idf1.idfobjects['ZONE']])])
    # print(self.zonenames)
    
    z = accim_Main.accimobj_SingleZone_Ep94('TestModel_SingleZone')
    z.addEMSProgramsBase()

    programlist = ([program.Name for program in self.idf1.idfobjects['EnergyManagementSystem:Program']])
    print(programlist)
    
    
    
    # lookfor('SetComfTemp','EnergyManagementSystem:Program')
    
    # listToSearchIn = ([x.Name for x in self.idf1.idfobjects['EnergyManagementSystem:Program']])

    # if 'SetComfTemp' in listToSearchIn:
    #     return True
    # else:
    #     return False
    
test_addEMSProgramsBase()