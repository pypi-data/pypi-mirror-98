import os, getpass
if getpass.getuser() == 'samuel':
    ironclust_path = '/home/samuel/Documents/Spikeinterface/ironclust'
    os.environ["IRONCLUST_PATH"] = ironclust_path

import unittest
import pytest
import spikeextractors as se
from spikesorters import IronClustSorter
from spikesorters.tests.common_tests import SorterCommonTestSuite

# This run several tests
@pytest.mark.skipif(not IronClustSorter.is_installed(), reason='ironclust not installed')
class IronclustCommonTestSuite(SorterCommonTestSuite, unittest.TestCase):
    SorterClass = IronClustSorter


if __name__ == '__main__':
    IronclustCommonTestSuite().test_on_toy()
    IronclustCommonTestSuite().test_several_groups()
    IronclustCommonTestSuite().test_with_BinDatRecordingExtractor()
