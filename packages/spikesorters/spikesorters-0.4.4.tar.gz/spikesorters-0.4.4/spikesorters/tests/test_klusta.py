import unittest
import pytest
import spikeextractors as se
from spikesorters import KlustaSorter
from spikesorters.tests.common_tests import SorterCommonTestSuite

# This run several tests
@pytest.mark.skipif(not KlustaSorter.is_installed(), reason='klusta not installed')
class KlustaCommonTestSuite(SorterCommonTestSuite, unittest.TestCase):
    SorterClass = KlustaSorter



if __name__ == '__main__':
    KlustaCommonTestSuite().test_on_toy()
    KlustaCommonTestSuite().test_several_groups()
    KlustaCommonTestSuite().test_with_BinDatRecordingExtractor()
