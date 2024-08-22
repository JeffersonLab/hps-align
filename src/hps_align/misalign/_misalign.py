from random import gauss, uniform
from os import *
import xml.etree.ElementTree as ET

class Misalignment:

    def __init__(self, detector_file, new_name=None):
        # detector_file = str(detector_file)
        # separate name of detector and filepath
        detector_name = detector_file.split('/')[-1]
        self.detector_name = detector_name.split('.')[0]
        self.detector_path = '/'.join(detector_file.split('/')[:-1])
        if new_name:
            misaligned_detector = self.detector_path + "/" + new_name
        else:
            # new detector file
            misaligned_detector = self.detector_path + "/" + self.detector_name + '_misaligned.xml'
        # copy detector_file to new file and set that as detector
        system(f'cp {detector_file} {misaligned_detector}')
        self.detector = misaligned_detector

        self.rwlist = [12301, 12302, 12303, 12304, 12305,
                       12306, 12307, 12308, 12309, 12310,
                       12311, 12312, 12313, 12314, 12315,
                       12316, 12317, 12318, 12319, 12320,
                       22301, 22302, 22303, 22304, 22305,
                       22306, 22307, 22308, 22309, 22310,
                       22311, 22312, 22313, 22314, 22315,
                       22316, 22317, 22318, 22319, 22320]
        
        self.tulist = [11101, 11102, 11103, 11104, 11105,
                       11106, 11107, 11108, 11109, 11110,
                       11111, 11112, 11113, 11114, 11115,
                       11116, 11117, 11118, 11119, 11120,
                       21101, 21102, 21103, 21104, 21105,
                       21106, 21107, 21108, 21109, 21110,
                       21111, 21112, 21113, 21114, 21115,
                       21116, 21117, 21118, 21119, 21120]
    
    def move_rw(self, distribution, sigma):
        """Draw random numbers from a distribution and add to Rw aligment constants.

        Parameters
        ----------
        distribution : str
            Distribution to draw from (gauss, uniform)
        sigma : float
            Characteristic displacement in Rw
        """
        # open detector xml file to edit values
        tree = ET.parse(self.detector)
        root = tree.getroot()
        # find the detector element
        detector = root.find('detectors').find('detector')
        # find all millepede constants
        for milleconst in detector.find('millepede_constants').findall('millepede_constant'):
            name = int(milleconst.get('name'))
            # check if millerpede constant is Rw
            if name in self.rwlist:
                value = milleconst.get('value')
                if distribution == 'gauss':
                    new_value = value + " + " + "%6f"%gauss(0, sigma)
                elif distribution == 'uniform':
                    new_value = value + " + " + "%6f"%uniform(0, sigma)
                else:
                    new_value = value
                milleconst.set('value', new_value)
        
        tree.write(self.detector)

    def move_tu(self, distribution, sigma):
        """Draw random numbers from a distribution and add to Tu aligment constants.
        
        Parameters
        ----------
        distribution : str
            Distribution to draw from (gauss, uniform)
        sigma : float
            Characteristic displacement in Tu
        """
        # open detector xml file to edit values
        tree = ET.parse(self.detector)
        root = tree.getroot()
        # find the detector element
        detector = root.find('detectors').find('detector')
        # find all millepede constants
        for milleconst in detector.find('millepede_constants').findall('millepede_constant'):
            name = int(milleconst.get('name'))
            # check if millerpede constant is Tu
            if name in self.tulist:
                value = milleconst.get('value')
                if distribution == 'gauss':
                    new_value = value + " + " + "%6f"%gauss(0, sigma)
                elif distribution == 'uniform':
                    new_value = value + " + " + "%6f"%uniform(0, sigma)
                else:
                    new_value = value
                milleconst.set('value', new_value)
        
        tree.write(self.detector)
    
    def misalign(self, distribution, params={'rw': 0.5, 'tu': 10}):
        if params['rw']:
            rw = params['rw']
            self.move_rw(distribution, rw)
        if params['tu']:
            tu = params['tu']
            self.move_tu(distribution, tu)
        print('Misalignment complete')