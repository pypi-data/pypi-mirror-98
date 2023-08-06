"""Generate IDFs."""


def inputdataSingleZone(self):
    """Input data for IDF generation in SingleZone."""
    fullAdapStandList = [0, 1, 2]
    self.AdapStand_List = list(int(num) for num in input("Enter the Adaptive Standard numbers separated by space (0 = CTE; 1 = EN16798-1; 2 = ASHRAE 55): ").split())
    while len(self.AdapStand_List) == 0 or not all(elem in fullAdapStandList for elem in self.AdapStand_List):
        print('          Adaptive Standard numbers are not correct. Please enter the numbers again.')
        self.AdapStand_List = list(int(num) for num in input("     Enter the Adaptive Standard numbers separated by space: ").split())
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        self.AdapStand_List = list(int(num) for num in input("     Enter the Adaptive Standard numbers separated by space: ").split())
        while len(self.AdapStand_List) == 0 or not all(elem in fullAdapStandList for elem in self.AdapStand_List):
            print('          Adaptive Standard numbers are not correct. Please enter the numbers again.')
            self.AdapStand_List = list(int(num) for num in input("     Enter the Adaptive Standard numbers separated by space: ").split())

    fullCATlist = [1, 2, 3, 80, 90]
    self.CAT_List = list(int(num) for num in input("Enter the Category numbers separated by space (1 = CAT I; 2 = CAT II; 3 = CAT III; 80 = 80% ACCEPT; 90 = 90% ACCEPT): ").split())
    while len(self.CAT_List) == 0 or not all(elem in fullCATlist for elem in self.CAT_List):
        print('          Category numbers are not correct. Please enter the numbers again.')
        self.CAT_List = list(int(num) for num in input("Enter the Category numbers separated by space: ").split())
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        self.CAT_List = list(int(num) for num in input("     Enter the Category numbers separated by space: ").split())
        while len(self.CAT_List) == 0 or not all(elem in fullCATlist for elem in self.CAT_List):
            print('          Category numbers are not correct. Please enter the numbers again.')
            self.CAT_List = list(int(num) for num in input("Enter the Category numbers separated by space: ").split())

    fullComfModList = [0, 1, 2, 3]
    self.ComfMod_List = list(int(num) for num in input("Enter the Comfort Mode numbers separated by space (0 = Static; 1 = OUT-CTE; 2 = OUT-SEN16798/SASHRAE55; 3 = OUT-AEN16798/AASHRAE55): ").split())
    while len(self.ComfMod_List) == 0 or not all(elem in fullComfModList for elem in self.ComfMod_List):
        print('          Comfort Mode numbers are not correct. Please enter the numbers again.')
        self.ComfMod_List = list(int(num) for num in input("     Enter the Comfort Mode numbers separated by space: ").split())
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        self.ComfMod_List = list(int(num) for num in input("     Enter the Comfort Mode numbers separated by space: ").split())
        while len(self.ComfMod_List) == 0 or not all(elem in fullComfModList for elem in self.ComfMod_List):
            print('          Comfort Mode numbers are not correct. Please enter the numbers again.')
            self.ComfMod_List = list(int(num) for num in input("     Enter the Comfort Mode numbers separated by space: ").split())

    try:
        self.ASTtol_value_from = float(input('Enter the ASTtol value from (if omitted, will be 0.1): '))
    except ValueError:
        self.ASTtol_value_from = float(0.1)
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        try:
            self.ASTtol_value_from = float(input('     Enter the ASTtol value from (if omitted, will be 0.1): '))
        except ValueError:
            self.ASTtol_value_from = float(0.1)

    try:
        self.ASTtol_value_to_input = float(input('Enter the ASTtol value to (if omitted, will be 0.1): '))
    except ValueError:
        self.ASTtol_value_to_input = float(0.1)
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        try:
            self.ASTtol_value_to_input = float(input('     Enter the ASTtol value to (if omitted, will be 0.1): '))
        except ValueError:
            self.ASTtol_value_to_input = float(0.1)

    try:
        self.ASTtol_value_steps = float(input('Enter the ASTtol value steps (if omitted, will be 0.1): '))
    except ValueError:
        self.ASTtol_value_steps = float(0.1)
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        try:
            self.ASTtol_value_steps = float(input('     Enter the ASTtol value steps (if omitted, will be 0.1): '))
        except ValueError:
            self.ASTtol_value_steps = float(0.1)



def inputdataMultipleZone(self):
    """Input data for IDF generation in MultipleZone."""
    fullAdapStandList = [0, 1, 2]
    self.AdapStand_List = list(int(num) for num in input("Enter the Adaptive Standard numbers separated by space (0 = CTE; 1 = EN16798-1; 2 = ASHRAE 55): ").split())
    while len(self.AdapStand_List) == 0 or not all(elem in fullAdapStandList for elem in self.AdapStand_List):
        print('          Adaptive Standard numbers are not correct. Please enter the numbers again.')
        self.AdapStand_List = list(int(num) for num in input("     Enter the Adaptive Standard numbers separated by space: ").split())
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        self.AdapStand_List = list(int(num) for num in input("     Enter the Adaptive Standard numbers separated by space: ").split())
        while len(self.AdapStand_List) == 0 or not all(elem in fullAdapStandList for elem in self.AdapStand_List):
            print('          Adaptive Standard numbers are not correct. Please enter the numbers again.')
            self.AdapStand_List = list(int(num) for num in input("     Enter the Adaptive Standard numbers separated by space: ").split())

    fullCATlist = [1, 2, 3, 80, 90]
    self.CAT_List = list(int(num) for num in input("Enter the Category numbers separated by space (1 = CAT I; 2 = CAT II; 3 = CAT III; 80 = 80% ACCEPT; 90 = 90% ACCEPT): ").split())
    while len(self.CAT_List) == 0 or not all(elem in fullCATlist for elem in self.CAT_List):
        print('          Category numbers are not correct. Please enter the numbers again.')
        self.CAT_List = list(int(num) for num in input("Enter the Category numbers separated by space: ").split())
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        self.CAT_List = list(int(num) for num in input("     Enter the Category numbers separated by space: ").split())
        while len(self.CAT_List) == 0 or not all(elem in fullCATlist for elem in self.CAT_List):
            print('          Category numbers are not correct. Please enter the numbers again.')
            self.CAT_List = list(int(num) for num in input("Enter the Category numbers separated by space: ").split())

    fullComfModList = [0, 1, 2, 3]
    self.ComfMod_List = list(int(num) for num in input("Enter the Comfort Mode numbers separated by space (0 = Static; 1 = OUT-CTE; 2 = OUT-SEN16798/SASHRAE55; 3 = OUT-AEN16798/AASHRAE55): ").split())
    while len(self.ComfMod_List) == 0 or not all(elem in fullComfModList for elem in self.ComfMod_List):
        print('          Comfort Mode numbers are not correct. Please enter the numbers again.')
        self.ComfMod_List = list(int(num) for num in input("     Enter the Comfort Mode numbers separated by space: ").split())
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        self.ComfMod_List = list(int(num) for num in input("     Enter the Comfort Mode numbers separated by space: ").split())
        while len(self.ComfMod_List) == 0 or not all(elem in fullComfModList for elem in self.ComfMod_List):
            print('          Comfort Mode numbers are not correct. Please enter the numbers again.')
            self.ComfMod_List = list(int(num) for num in input("     Enter the Comfort Mode numbers separated by space: ").split())

    fullHVACmodeList = [0, 1, 2]
    self.HVACmode_List = list(int(num) for num in input("Enter the HVAC Mode numbers separated by space (0 = Fully Air-conditioned; 1 = Naturally ventilated; 2 = Mixed Mode): ").split())
    while len(self.HVACmode_List) == 0 or not all(elem in fullHVACmodeList for elem in self.HVACmode_List):
        print('          HVACmode numbers are not correct. Please enter the numbers again.')
        self.HVACmode_List = list(int(num) for num in input("     Enter the HVACmode numbers separated by space: ").split())
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        self.HVACmode_List = list(int(num) for num in input("     Enter the HVACmode numbers separated by space: ").split())
        while len(self.HVACmode_List) == 0 or not all(elem in fullHVACmodeList for elem in self.HVACmode_List):
            print('          HVACmode numbers are not correct. Please enter the numbers again.')
            self.HVACmode_List = list(int(num) for num in input("     Enter the HVACmode numbers separated by space: ").split())

    fullVentCtrlList = [0, 1]
    self.VentCtrl_List = list(int(num) for num in input("Enter the Ventilation Control numbers separated by space (0 = Ventilates above neutral temperature; 1 = Ventilates above upper comfort limit): ").split())
    while len(self.VentCtrl_List) == 0 or not all(elem in fullVentCtrlList for elem in self.VentCtrl_List):
        print('          Ventilation Control numbers are not correct. Please enter the numbers again.')
        self.VentCtrl_List = list(int(num) for num in input("     Enter the Ventilation Control numbers separated by space: ").split())
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        self.VentCtrl_List = list(int(num) for num in input("     Enter the Ventilation Control numbers separated by space: ").split())
        while len(self.VentCtrl_List) == 0 or not all(elem in fullVentCtrlList for elem in self.VentCtrl_List):
            print('          Ventilation Control numbers are not correct. Please enter the numbers again.')
            self.VentCtrl_List = list(int(num) for num in input("     Enter the Ventilation Control numbers separated by space: ").split())

    self.VSToffset_List = list(float(num) for num in input("Enter the VSToffset numbers separated by space (if omitted, will be 0): ").split())
    if len(self.VSToffset_List) == 0:
        self.VSToffset_List = [float(0)]
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        self.VSToffset_List = list(float(num) for num in input("     Enter the VSToffset numbers separated by space (if omitted, will be 0): ").split())
        if len(self.VSToffset_List) == 0:
            self.VSToffset_List = [float(0)]

    self.MinOToffset_List = list(float(num) for num in input("Enter the MinOToffset numbers separated by space (if omitted, will be 50): ").split())
    if len(self.MinOToffset_List) == 0:
        self.MinOToffset_List = [float(50)]
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        self.MinOToffset_List = list(float(num) for num in input("     Enter the MinOToffset numbers separated by space (if omitted, will be 50): ").split())
        if len(self.MinOToffset_List) == 0:
            self.MinOToffset_List = [float(50)]

    self.MaxWindSpeed_List = list(float(num) for num in input("Enter the MaxWindSpeed numbers separated by space (if omitted, will be 50): ").split())
    if len(self.MaxWindSpeed_List) == 0:
        self.MaxWindSpeed_List = [float(50)]
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        self.MaxWindSpeed_List = list(float(num) for num in input("     Enter the MaxWindSpeed numbers separated by space (if omitted, will be 50): ").split())
        if len(self.MaxWindSpeed_List) == 0:
            self.MaxWindSpeed_List = [float(50)]

    try:
        self.ASTtol_value_from = float(input('Enter the ASTtol value from (if omitted, will be 0.1): '))
    except ValueError:
        self.ASTtol_value_from = float(0.1)
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        try:
            self.ASTtol_value_from = float(input('     Enter the ASTtol value from (if omitted, will be 0.1): '))
        except ValueError:
            self.ASTtol_value_from = float(0.1)

    try:
        self.ASTtol_value_to_input = float(input('Enter the ASTtol value to (if omitted, will be 0.1): '))
    except ValueError:
        self.ASTtol_value_to_input = float(0.1)
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        try:
            self.ASTtol_value_to_input = float(input('     Enter the ASTtol value to (if omitted, will be 0.1): '))
        except ValueError:
            self.ASTtol_value_to_input = float(0.1)

    try:
        self.ASTtol_value_steps = float(input('Enter the ASTtol value steps (if omitted, will be 0.1): '))
    except ValueError:
        self.ASTtol_value_steps = float(0.1)
    while input('          Are you sure the numbers are correct? [y or [] / n]: ') == 'n':
        try:
            self.ASTtol_value_steps = float(input('     Enter the ASTtol value steps (if omitted, will be 0.1): '))
        except ValueError:
            self.ASTtol_value_steps = float(0.1)


def genIDFSingleZone(self,
                     AdapStand=None,
                     CAT=None,
                     ComfMod=None,
                     ASTtol_start=0.1,
                     ASTtol_end_input=0.1,
                     ASTtol_steps=0.1,
                     NameSuffix='',
                     verboseMode: bool =True,
                     confirmGen: bool =None
                     ):
    """Generate IDFs in SingleZone."""
    import os
    from os import listdir
    import numpy
    from eppy import modeleditor
    from eppy.modeleditor import IDF

    arguments = (AdapStand is None,
                 CAT is None,
                 ComfMod is None,
                 ASTtol_start == 0.1,
                 ASTtol_end_input == 0.1,
                 ASTtol_steps == 0.1)

    if all(arguments):
        self.ASTtol_value_to = self.ASTtol_value_to_input+self.ASTtol_value_steps
    else:
        ASTtol_end = ASTtol_end_input + ASTtol_steps

    if all(arguments):
        pass
    else:
        self.AdapStand_List = AdapStand
        self.CAT_List = CAT
        self.ComfMod_List = ComfMod
        self.ASTtol_value_from = ASTtol_start
        self.ASTtol_value_to = ASTtol_end
        self.ASTtol_value_steps = ASTtol_steps

    if NameSuffix == '':
        suffix = ''
    else:
        suffix = '[' + NameSuffix

    filelist_pymod = ([file for file in listdir() if file.endswith('_pymod.idf')])
    filelist_pymod = ([file.split('.idf')[0] for file in filelist_pymod])
    # print(filelist_pymod)

    outputlist = []
    for file in filelist_pymod:
        filename = file
        for AdapStand_value in self.AdapStand_List:
            if AdapStand_value == 0:
                for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                    outputname = (
                            filename
                            + '[AS_CTE'
                            + '[CA_X'
                            + '[CM_X'
                            + '[AT_' + repr(ASTtol_value)
                            + suffix
                            + '.idf'
                    )
                    outputlist.append(outputname)
            elif AdapStand_value == 1:
                for CAT_value in self.CAT_List:
                    if CAT_value not in range(0, 4):
                        continue
                    else:
                        for ComfMod_value in self.ComfMod_List:
                            for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                outputname = (
                                    filename
                                    + '[AS_EN16798'
                                    + '[CA_'+repr(CAT_value)
                                    + '[CM_'+repr(ComfMod_value)
                                    + '[AT_'+repr(ASTtol_value)
                                    + suffix
                                    + '.idf'
                                    )
                                outputlist.append(outputname)
            elif AdapStand_value == 2:
                for CAT_value in self.CAT_List:
                    if CAT_value not in range(80, 91, 10):
                        continue
                    else:
                        for ComfMod_value in self.ComfMod_List:
                            for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                outputname = (
                                    filename
                                    + '[AS_ASHRAE55'
                                    + '[CA_'+repr(CAT_value)
                                    + '[CM_'+repr(ComfMod_value)
                                    + '[AT_'+repr(ASTtol_value)
                                    + suffix
                                    + '.idf'
                                    )
                                outputlist.append(outputname)

    if verboseMode:
        print('The list of output IDFs is going to be:')
        print(*outputlist, sep="\n")
        print(f'And the total number of output IDFs is going to be {len(outputlist)}')

    if confirmGen is None:
        confirmGen = input('Do you still want to run ACCIS? [y/n]: ')
        if confirmGen == 'y':
            confirmGen = True
        else:
            confirmGen = False

    if confirmGen == True:
        for file in filelist_pymod:
            filename = file

            fname1 = filename+'.idf'
            if verboseMode:
                print(fname1)
            idf1 = IDF(fname1)

            # print(filename)
            SetInputData = ([program for program in idf1.idfobjects['EnergyManagementSystem:Program'] if program.Name == 'SetInputData'])
            # Making IDFs: the output file path can not contain the following characters: & ^ , = % " \ / : * ? " < > |
            for AdapStand_value in self.AdapStand_List:
                SetInputData[0].Program_Line_1 = 'set AdapStand  =  '+repr(AdapStand_value)
                if AdapStand_value == 0:
                    SetInputData[0].Program_Line_2 = 'set CAT = 1'
                    SetInputData[0].Program_Line_3 = 'set ComfMod = 0'
                    for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                        SetInputData[0].Program_Line_4 = 'set ACSTtol = '+repr(-ASTtol_value)
                        SetInputData[0].Program_Line_5 = 'set AHSTtol = '+repr(ASTtol_value)
                        outputname = (
                            filename
                            + '[AS_CTE'
                            + '[CA_X'
                            + '[CM_X'
                            + '[AT_' + repr(ASTtol_value)
                            + suffix
                            + '.idf'
                        )
                        if verboseMode:
                            print(outputname)
                        idf1.savecopy(outputname)
                elif AdapStand_value == 1:
                    for CAT_value in self.CAT_List:
                        if CAT_value not in range(0, 4):
                            continue
                        else:
                            SetInputData[0].Program_Line_2 = 'set CAT = '+repr(CAT_value)
                            for ComfMod_value in self.ComfMod_List:
                                SetInputData[0].Program_Line_3 = 'set ComfMod = '+repr(ComfMod_value)
                                for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                    SetInputData[0].Program_Line_4 = 'set ACSTtol = '+repr(-ASTtol_value)
                                    SetInputData[0].Program_Line_5 = 'set AHSTtol = '+repr(ASTtol_value)
                                    outputname = (
                                        filename
                                        + '[AS_EN16798'
                                        + '[CA_'+repr(CAT_value)
                                        + '[CM_'+repr(ComfMod_value)
                                        + '[AT_'+repr(ASTtol_value)
                                        + suffix
                                        + '.idf'
                                        )
                                    if verboseMode:
                                        print(outputname)
                                    idf1.savecopy(outputname)
                elif AdapStand_value == 2:
                    for CAT_value in self.CAT_List:
                        if CAT_value not in range(80, 91, 10):
                            continue
                        else:
                            SetInputData[0].Program_Line_2 = 'set CAT = '+repr(CAT_value)
                            for ComfMod_value in self.ComfMod_List:
                                SetInputData[0].Program_Line_3 = 'set ComfMod = '+repr(ComfMod_value)
                                for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                    SetInputData[0].Program_Line_4 = 'set ACSTtol = '+repr(-ASTtol_value)
                                    SetInputData[0].Program_Line_5 = 'set AHSTtol = '+repr(ASTtol_value)
                                    outputname = (
                                        filename
                                        + '[AS_ASHRAE55'
                                        + '[CA_'+repr(CAT_value)
                                        + '[CM_'+repr(ComfMod_value)
                                        + '[AT_'+repr(ASTtol_value)
                                        + suffix
                                        + '.idf'
                                        )
                                    if verboseMode:
                                        print(outputname)
                                    idf1.savecopy(outputname)
    elif confirmGen == False:
        if verboseMode:
            print('IDF generation has been shut down')

    filelist_pymod = ([file for file in listdir() if file.endswith('_pymod.idf')])
    for file in filelist_pymod:
        os.remove(file)

    # del SetInputData


def genIDFMultipleZone(self,
                       AdapStand=None,
                       CAT=None,
                       ComfMod=None,
                       HVACmode=None,
                       VentCtrl=None,
                       VSToffset=[0],
                       MinOToffset=[50],
                       MaxWindSpeed=[50],
                       ASTtol_start=0.1,
                       ASTtol_end_input=0.1,
                       ASTtol_steps=0.1,
                       NameSuffix='',
                       verboseMode: bool = True,
                       confirmGen: bool = None
                       ):
    """Generate IDFs in MultipleZone."""
    import os
    from os import listdir
    import numpy
    from eppy import modeleditor
    from eppy.modeleditor import IDF
    import time
    from accim.misc.progressBar import progressBar

    arguments = (AdapStand is None,
                 CAT is None,
                 ComfMod is None,
                 HVACmode is None,
                 VentCtrl is None,
                 VSToffset == [0],
                 MinOToffset == [50],
                 MaxWindSpeed == [50],
                 ASTtol_start == 0.1,
                 ASTtol_end_input == 0.1,
                 ASTtol_steps == 0.1)

    if all(arguments):
        self.ASTtol_value_to = self.ASTtol_value_to_input+self.ASTtol_value_steps
    else:
        ASTtol_end = ASTtol_end_input + ASTtol_steps

    if all(arguments):
        pass
    else:
        self.AdapStand_List = AdapStand
        self.CAT_List = CAT
        self.ComfMod_List = ComfMod
        self.HVACmode_List = HVACmode
        self.VentCtrl_List = VentCtrl
        self.VSToffset_List = VSToffset
        self.MinOToffset_List = MinOToffset
        self.MaxWindSpeed_List = MaxWindSpeed
        self.ASTtol_value_from = ASTtol_start
        self.ASTtol_value_to = ASTtol_end
        self.ASTtol_value_steps = ASTtol_steps

    if NameSuffix == '':
        suffix = ''
    else:
        suffix = '[' + NameSuffix

    filelist_pymod = ([file for file in listdir() if file.endswith('_pymod.idf')])
    filelist_pymod = ([file.split('.idf')[0] for file in filelist_pymod])
    # print(filelist_pymod)

    outputlist = []
    for file in filelist_pymod:
        filename = file
        for AdapStand_value in self.AdapStand_List:
            if AdapStand_value == 0:
                for HVACmode_value in self.HVACmode_List:
                    if HVACmode_value == 0:
                        for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                            outputname = (
                                filename
                                + '[AS_CTE'
                                + '[CA_X'
                                + '[CM_X'
                                + '[HM_' + repr(HVACmode_value)
                                + '[VC_X'
                                + '[VO_X'
                                + '[MT_X'
                                + '[MW_X'
                                + '[AT_' + repr(ASTtol_value)
                                + suffix
                                + '.idf'
                                )
                            outputlist.append(outputname)
                    else:
                        for VentCtrl_value in self.VentCtrl_List:
                            for VSToffset_value in self.VSToffset_List:
                                for MinOToffset_value in self.MinOToffset_List:
                                    for MaxWindSpeed_value in self.MaxWindSpeed_List:
                                        for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                            outputname = (
                                                filename
                                                + '[AS_CTE'
                                                + '[CA_X'
                                                + '[CM_X'
                                                + '[HM_' + repr(HVACmode_value)
                                                + '[VC_' + repr(VentCtrl_value)
                                                + '[VO_' + repr(VSToffset_value)
                                                + '[MT_' + repr(MinOToffset_value)
                                                + '[MW_' + repr(MaxWindSpeed_value)
                                                + '[AT_' + repr(ASTtol_value)
                                                + suffix
                                                + '.idf'
                                                )
                                            outputlist.append(outputname)
            elif AdapStand_value == 1:
                for CAT_value in self.CAT_List:
                    if CAT_value not in range(0, 4):
                        continue
                    else:
                        for ComfMod_value in self.ComfMod_List:
                            for HVACmode_value in self.HVACmode_List:
                                if HVACmode_value == 0:
                                    for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                        outputname = (
                                            filename
                                            + '[AS_EN16798'
                                            + '[CA_' + repr(CAT_value)
                                            + '[CM_' + repr(ComfMod_value)
                                            + '[HM_' + repr(HVACmode_value)
                                            + '[VC_X'
                                            + '[VO_X'
                                            + '[MT_X'
                                            + '[MW_X'
                                            + '[AT_' + repr(ASTtol_value)
                                            + suffix
                                            + '.idf'
                                            )
                                        outputlist.append(outputname)
                                else:
                                    for VentCtrl_value in self.VentCtrl_List:
                                        for VSToffset_value in self.VSToffset_List:
                                            for MinOToffset_value in self.MinOToffset_List:
                                                for MaxWindSpeed_value in self.MaxWindSpeed_List:
                                                    for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                                        outputname = (
                                                            filename
                                                            + '[AS_EN16798'
                                                            + '[CA_' + repr(CAT_value)
                                                            + '[CM_' + repr(ComfMod_value)
                                                            + '[HM_' + repr(HVACmode_value)
                                                            + '[VC_' + repr(VentCtrl_value)
                                                            + '[VO_' + repr(VSToffset_value)
                                                            + '[MT_' + repr(MinOToffset_value)
                                                            + '[MW_' + repr(MaxWindSpeed_value)
                                                            + '[AT_' + repr(ASTtol_value)
                                                            + suffix
                                                            + '.idf'
                                                            )
                                                        outputlist.append(outputname)
            elif AdapStand_value == 2:
                for CAT_value in self.CAT_List:
                    if CAT_value not in range(80, 91, 10):
                        continue
                    else:
                        for ComfMod_value in self.ComfMod_List:
                            for HVACmode_value in self.HVACmode_List:
                                if HVACmode_value == 0:
                                    for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                        outputname = (
                                            filename
                                            + '[AS_EN16798'
                                            + '[CA_' + repr(CAT_value)
                                            + '[CM_' + repr(ComfMod_value)
                                            + '[HM_' + repr(HVACmode_value)
                                            + '[VC_X'
                                            + '[VO_X'
                                            + '[MT_X'
                                            + '[MW_X'
                                            + '[AT_' + repr(ASTtol_value)
                                            + suffix
                                            + '.idf'
                                            )
                                        outputlist.append(outputname)
                                else:
                                    for VentCtrl_value in self.VentCtrl_List:
                                        for VSToffset_value in self.VSToffset_List:
                                            for MinOToffset_value in self.MinOToffset_List:
                                                for MaxWindSpeed_value in self.MaxWindSpeed_List:
                                                    for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                                        outputname = (
                                                            filename
                                                            + '[AS_ASHRAE55'
                                                            + '[CA_' + repr(CAT_value)
                                                            + '[CM_' + repr(ComfMod_value)
                                                            + '[HM_' + repr(HVACmode_value)
                                                            + '[VC_' + repr(VentCtrl_value)
                                                            + '[VO_' + repr(VSToffset_value)
                                                            + '[MT_' + repr(MinOToffset_value)
                                                            + '[MW_' + repr(MaxWindSpeed_value)
                                                            + '[AT_' + repr(ASTtol_value)
                                                            + suffix
                                                            + '.idf'
                                                            )
                                                        outputlist.append(outputname)
    if verboseMode:
        print('The list of output IDFs is going to be:')
        print(*outputlist, sep="\n")
        print(f'And the total number of output IDFs is going to be {len(outputlist)}')

    if confirmGen is None:
        confirmGen = input('Do you still want to run ACCIS? [y/n]: ')
        if confirmGen == 'y':
            confirmGen = True
        else:
            confirmGen = False

    if confirmGen == True:
    #     for file in filelist_pymod, progressBar(outputlist, prefix = 'Progress:', suffix = 'Complete', length = 50):
        for file in filelist_pymod:
            filename = file

            fname1 = filename+'.idf'
            if verboseMode:
                print(fname1)
            idf1 = IDF(fname1)

            # print(filename)

            SetInputData = ([program for program in idf1.idfobjects['EnergyManagementSystem:Program'] if program.Name == 'SetInputData'])

            for AdapStand_value in self.AdapStand_List:
                SetInputData[0].Program_Line_1 = 'set AdapStand = '+repr(AdapStand_value)
                if AdapStand_value == 0:
                    SetInputData[0].Program_Line_2 = 'set CAT = 1'
                    SetInputData[0].Program_Line_3 = 'set ComfMod = 0'
                    for HVACmode_value in self.HVACmode_List:
                        SetInputData[0].Program_Line_4 = 'set HVACmode = '+repr(HVACmode_value)
                        if HVACmode_value == 0:
                            for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                SetInputData[0].Program_Line_5 = 'set ACSTtol = '+repr(-ASTtol_value)
                                SetInputData[0].Program_Line_6 = 'set AHSTtol = '+repr(ASTtol_value)
                                outputname = (
                                    filename
                                    + '[AS_CTE'
                                    + '[CA_X'
                                    + '[CM_X'
                                    + '[HM_' + repr(HVACmode_value)
                                    + '[VC_X'
                                    + '[VO_X'
                                    + '[MT_X'
                                    + '[MW_X'
                                    + '[AT_' + repr(ASTtol_value)
                                    + suffix
                                    + '.idf'
                                    )
                                if verboseMode:
                                    print(outputname)
                                idf1.savecopy(outputname)

                        else:
                            for VentCtrl_value in self.VentCtrl_List:
                                SetInputData[0].Program_Line_5 = 'set VentCtrl = '+repr(VentCtrl_value)
                                for VSToffset_value in self.VSToffset_List:
                                    SetInputData[0].Program_Line_6 = 'set VSToffset = '+repr(VSToffset_value)
                                    for MinOToffset_value in self.MinOToffset_List:
                                        SetInputData[0].Program_Line_7 = 'set MinOToffset = '+repr(MinOToffset_value)
                                        for MaxWindSpeed_value in self.MaxWindSpeed_List:
                                            SetInputData[0].Program_Line_8 = 'set MaxWindSpeed = '+repr(MaxWindSpeed_value)
                                            for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                                SetInputData[0].Program_Line_9 = 'set ACSTtol = '+repr(-ASTtol_value)
                                                SetInputData[0].Program_Line_10 = 'set AHSTtol = '+repr(ASTtol_value)
                                                outputname = (
                                                    filename
                                                    + '[AS_CTE'
                                                    + '[CA_X'
                                                    + '[CM_X'
                                                    + '[HM_' + repr(HVACmode_value)
                                                    + '[VC_' + repr(VentCtrl_value)
                                                    + '[VO_' + repr(VSToffset_value)
                                                    + '[MT_' + repr(MinOToffset_value)
                                                    + '[MW_' + repr(MaxWindSpeed_value)
                                                    + '[AT_' + repr(ASTtol_value)
                                                    + suffix
                                                    + '.idf'
                                                    )
                                                if verboseMode:
                                                    print(outputname)
                                                idf1.savecopy(outputname)

                elif AdapStand_value == 1:
                    for CAT_value in self.CAT_List:
                        if CAT_value not in range(0, 4):
                            continue
                        else:
                            SetInputData[0].Program_Line_2 = 'set CAT = '+repr(CAT_value)
                            for ComfMod_value in self.ComfMod_List:
                                SetInputData[0].Program_Line_3 = 'set ComfMod = '+repr(ComfMod_value)
                                for HVACmode_value in self.HVACmode_List:
                                    SetInputData[0].Program_Line_4 = 'set HVACmode = '+repr(HVACmode_value)
                                    if HVACmode_value == 0:
                                        for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                            SetInputData[0].Program_Line_9 = 'set ACSTtol = '+repr(-ASTtol_value)
                                            SetInputData[0].Program_Line_10 = 'set AHSTtol = '+repr(ASTtol_value)
                                            outputname = (
                                                filename
                                                + '[AS_EN16798'
                                                + '[CA_' + repr(CAT_value)
                                                + '[CM_' + repr(ComfMod_value)
                                                + '[HM_' + repr(HVACmode_value)
                                                + '[VC_X'
                                                + '[VO_X'
                                                + '[MT_X'
                                                + '[MW_X'
                                                + '[AT_' + repr(ASTtol_value)
                                                + suffix
                                                + '.idf'
                                                )
                                            if verboseMode:
                                                print(outputname)
                                            idf1.savecopy(outputname)

                                    else:
                                        for VentCtrl_value in self.VentCtrl_List:
                                            SetInputData[0].Program_Line_5 = 'set VentCtrl = '+repr(VentCtrl_value)
                                            for VSToffset_value in self.VSToffset_List:
                                                SetInputData[0].Program_Line_6 = 'set VSToffset = '+repr(VSToffset_value)
                                                for MinOToffset_value in self.MinOToffset_List:
                                                    SetInputData[0].Program_Line_7 = 'set MinOToffset = '+repr(MinOToffset_value)
                                                    for MaxWindSpeed_value in self.MaxWindSpeed_List:
                                                        SetInputData[0].Program_Line_8 = 'set MaxWindSpeed = '+repr(MaxWindSpeed_value)
                                                        for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                                            SetInputData[0].Program_Line_9 = 'set ACSTtol = '+repr(-ASTtol_value)
                                                            SetInputData[0].Program_Line_10 = 'set AHSTtol = '+repr(ASTtol_value)
                                                            outputname = (
                                                                filename
                                                                + '[AS_EN16798'
                                                                + '[CA_' + repr(CAT_value)
                                                                + '[CM_' + repr(ComfMod_value)
                                                                + '[HM_' + repr(HVACmode_value)
                                                                + '[VC_' + repr(VentCtrl_value)
                                                                + '[VO_' + repr(VSToffset_value)
                                                                + '[MT_' + repr(MinOToffset_value)
                                                                + '[MW_' + repr(MaxWindSpeed_value)
                                                                + '[AT_' + repr(ASTtol_value)
                                                                + suffix
                                                                + '.idf'
                                                                )
                                                            if verboseMode:
                                                                print(outputname)
                                                            idf1.savecopy(outputname)

                elif AdapStand_value == 2:
                    for CAT_value in self.CAT_List:
                        if CAT_value not in range(80, 91, 10):
                            continue
                        else:
                            SetInputData[0].Program_Line_2 = 'set CAT = '+repr(CAT_value)
                            for ComfMod_value in self.ComfMod_List:
                                SetInputData[0].Program_Line_3 = 'set ComfMod = '+repr(ComfMod_value)
                                for HVACmode_value in self.HVACmode_List:
                                    SetInputData[0].Program_Line_4 = 'set HVACmode = '+repr(HVACmode_value)
                                    if HVACmode_value == 0:
                                        for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                            SetInputData[0].Program_Line_9 = 'set ACSTtol = '+repr(-ASTtol_value)
                                            SetInputData[0].Program_Line_10 = 'set AHSTtol = '+repr(ASTtol_value)
                                            outputname = (
                                                filename
                                                + '[AS_EN16798'
                                                + '[CA_' + repr(CAT_value)
                                                + '[CM_' + repr(ComfMod_value)
                                                + '[HM_' + repr(HVACmode_value)
                                                + '[VC_X'
                                                + '[VO_X'
                                                + '[MT_X'
                                                + '[MW_X'
                                                + '[AT_' + repr(ASTtol_value)
                                                + suffix
                                                + '.idf'
                                                )
                                            if verboseMode:
                                                print(outputname)
                                            idf1.savecopy(outputname)
                                    else:
                                        for VentCtrl_value in self.VentCtrl_List:
                                            SetInputData[0].Program_Line_5 = 'set VentCtrl = '+repr(VentCtrl_value)
                                            for VSToffset_value in self.VSToffset_List:
                                                SetInputData[0].Program_Line_6 = 'set VSToffset = '+repr(VSToffset_value)
                                                for MinOToffset_value in self.MinOToffset_List:
                                                    SetInputData[0].Program_Line_7 = 'set MinOToffset = '+repr(MinOToffset_value)
                                                    for MaxWindSpeed_value in self.MaxWindSpeed_List:
                                                        SetInputData[0].Program_Line_8 = 'set MaxWindSpeed = '+repr(MaxWindSpeed_value)
                                                        for ASTtol_value in numpy.arange(self.ASTtol_value_from, self.ASTtol_value_to, self.ASTtol_value_steps):
                                                            SetInputData[0].Program_Line_9 = 'set ACSTtol = '+repr(-ASTtol_value)
                                                            SetInputData[0].Program_Line_10 = 'set AHSTtol = '+repr(ASTtol_value)
                                                            outputname = (
                                                                filename
                                                                + '[AS_ASHRAE55'
                                                                + '[CA_' + repr(CAT_value)
                                                                + '[CM_' + repr(ComfMod_value)
                                                                + '[HM_' + repr(HVACmode_value)
                                                                + '[VC_' + repr(VentCtrl_value)
                                                                + '[VO_' + repr(VSToffset_value)
                                                                + '[MT_' + repr(MinOToffset_value)
                                                                + '[MW_' + repr(MaxWindSpeed_value)
                                                                + '[AT_' + repr(ASTtol_value)
                                                                + suffix
                                                                + '.idf'
                                                                )
                                                            if verboseMode:
                                                                print(outputname)
                                                            idf1.savecopy(outputname)
        time.sleep(0.1)
    elif confirmGen == False:
        if verboseMode:
            print('IDF generation has been shut down')

    filelist_pymod = ([file for file in listdir() if file.endswith('_pymod.idf')])
    for file in filelist_pymod:
        os.remove(file)

    # del SetInputData
