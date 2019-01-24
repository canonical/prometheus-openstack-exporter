import unittest

import prometheus_openstack_exporter as poe


class TestPrometheusOpenstackExporter(unittest.TestCase):
    def test_data_gatherer_needed(self):
        self.assertTrue(
            poe.data_gatherer_needed(
                {'enabled_collectors':
                 ['cinder', 'neutron', 'nova', 'swift']}))
        self.assertTrue(
            poe.data_gatherer_needed(
                {'enabled_collectors':
                 ['cinder', 'neutron', 'nova', 'swift', 'swift-account-usage']}))
        self.assertFalse(
            poe.data_gatherer_needed(
                {'enabled_collectors':
                 ['swift-account-usage']}))
        self.assertFalse(
            poe.data_gatherer_needed(
                {'enabled_collectors':
                 ['swift', 'swift-account-usage']}))
