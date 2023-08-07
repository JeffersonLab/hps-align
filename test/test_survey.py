
import unittest

from hps_align.survey.survey_results_2019 import *


class TestSurvey2019(unittest.TestCase):

    def test_txt_input(self):
        survey_files = {'ballframe_top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_top_1.txt',
                    'pinframe_top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_top_1.txt',
                    'ballframe_bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_bottom_1.txt',
                    'pinframe_bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/uchannel_empty_bottom_1.txt',
                    'matt_fixture': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_fixture_empty_1.txt',
                    'sho_fixture': '/Users/schababi/workspace/hps/hps-align/survey_data/L123_fixture_sho.txt',
                    'L0_axial_top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_axial_top_module1_1.txt',
                    'L0_stereo_top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_stereo_top_module1_1.txt',
                    'L0_axial_bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_axial_bottom_module2_1.txt',
                    'L0_stereo_bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L0_stereo_bottom_module2_1.txt',
                    'L1_axial_top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L1_axial_top_module3_1.txt',
                    'L1_stereo_top': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L1_stereo_top_module3_1.txt',
                    'L1_axial_bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L1_axial_bottom_module5_1.txt',
                    'L1_stereo_bottom': '/Users/schababi/workspace/hps/hps-align/survey_data/meas1/L1_stereo_bottom_module5_1.txt'}
    
        survey = Survey2019(survey_files)
        survey.print_results('survey_results_2019.csv')
