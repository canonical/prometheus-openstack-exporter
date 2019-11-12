import unittest

import mock

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
        self.assertEqual(
            poe.data_gatherer_needed(
                {'enabled_collectors':
                 ['cinder', 'neutron', 'nova', 'swift']}),
            set(['cinder', 'nova', 'neutron']),
        )
        self.assertEqual(
            poe.data_gatherer_needed({}),
            set(['cinder', 'nova', 'neutron']),
        )

    @mock.patch('prometheus_openstack_exporter.config')
    def test_get_nova_info(self, config):
        config.return_value = {}
        prodstack = {'tenants': []}
        nova = mock.Mock()
        nova.aggregates = mock.MagicMock()
        nova.flavors = mock.MagicMock()
        nova.hypervisors = mock.MagicMock()
        nova.servers = mock.MagicMock()
        nova.servers.list = mock.MagicMock()
        nova.services = mock.MagicMock()

        data_gatherer = poe.DataGatherer()
        data_gatherer._get_nova_info(nova, None, prodstack)

        expected = [
            mock.call(search_opts={'marker': '', 'limit': '100', 'status': 'ACTIVE', 'all_tenants': '1'}),
            mock.call(search_opts={'marker': '', 'limit': '100', 'status': 'ERROR', 'all_tenants': '1'}),
            mock.call(search_opts={'marker': '', 'limit': '100', 'status': 'SHELVED_OFFLOADED', 'all_tenants': '1'}),
            mock.call(search_opts={'marker': '', 'limit': '100', 'status': 'SHUTOFF', 'all_tenants': '1'}),
            mock.call(search_opts={'marker': '', 'limit': '100', 'status': 'SUSPENDED', 'all_tenants': '1'}),
            mock.call(search_opts={'marker': '', 'limit': '100', 'status': 'VERIFY_RESIZE', 'all_tenants': '1'}),
        ]
        nova.servers.list.assert_has_calls(expected, any_order=True)

        not_expected = mock.call(search_opts={'marker': '', 'limit': '100', 'status': 'BUILD', 'all_tenants': '1'})
        self.assertTrue(not_expected not in nova.servers.list.call_args_list)
