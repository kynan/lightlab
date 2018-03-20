from . import VISAInstrumentDriver
from lightlab.equipment.abstract_drivers import TekScopeAbstract

class Tektronix_TDS6154C_Oscope(VISAInstrumentDriver, TekScopeAbstract):
    ''' Real time scope.
        See abstract driver for description.

        `Manual <http://www.tek.com/sites/tek.com/files/media/media/resources/55W_14873_9.pdf>`__
    '''
    totalChans = 4
    # Similar to the DSA, except
    __recLenParam = 'HORIZONTAL:RECORDLENGTH'  # this is different from DSA
    __clearBeforeAcquire = True
    __measurementSourceParam = 'SOURCE1:WFM'
    __runModeParam = 'ACQUIRE:STOPAFTER:MODE'
    __runModeSingleShot = 'CONDITION'
    __yScaleParam = 'YMULT'                    # this is different from DSA

    def __setupSingleShot(self, isSampling, forcing=False):
        ''' Additional DSA things needed to put it in the right mode.
            If it is not sampling, the trigger source should always be external
        '''
        super().__setupSingleShot(isSampling, forcing)
        self.setConfigParam('ACQUIRE:STOPAFTER:CONDITION',
                            'ACQWFMS' if isSampling else'AVGCOMP',
                            forceHardware=forcing)
        if isSampling:
            self.setConfigParam('ACQUIRE:STOPAFTER:COUNT', '1', forceHardware=forcing)
        if not isSampling:
            self.setConfigParam('TRIGGER:SOURCE', 'EXTDIRECT', forceHardware=forcing)
