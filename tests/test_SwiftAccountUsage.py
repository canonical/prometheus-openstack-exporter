import unittest

from mock import Mock, MagicMock, call, patch

from requests.structures import CaseInsensitiveDict

import prometheus_openstack_exporter as poe


class TestSwiftAccountUsage(unittest.TestCase):

    @patch('prometheus_openstack_exporter.SwiftAccountUsage._get_account_ring')
    @patch('prometheus_openstack_exporter.requests')
    @patch('prometheus_openstack_exporter.config')
    def test__get_account_usage(self, _config, _requests, _SwiftAccountUsage__get_account_ring):
        _config = MagicMock()  # noqa: F841
        _requests = MagicMock()  # noqa: F841
        _SwiftAccountUsage__get_account_ring = MagicMock()  # noqa: F841

        s = poe.SwiftAccountUsage()
        s.account_ring = MagicMock()
        s.account_ring.get_nodes.return_value = (26701, [
            {'device': 'sdb', 'id': 0, 'ip': '10.24.0.18', 'meta': u'', 'port': 6002,
             'region': 1, 'replication_ip': '10.24.0.18', 'replication_port': 6002, 'weight': 100.0, 'zone': 1},
            {'device': 'sdd', 'id': 50, 'ip': '10.24.0.71', 'meta': u'', 'port': 6002,
             'region': 1, 'replication_ip': '10.24.0.71', 'replication_port': 6002, 'weight': 180.0, 'zone': 3},
            {'device': 'sdi', 'id': 59, 'ip': '10.24.0.72', 'meta': u'', 'port': 6002,
             'region': 1, 'replication_ip': '10.24.0.72', 'replication_port': 6002, 'weight': 360.0, 'zone': 2}])

        response_mock = Mock()
        response_mock.configure_mock(
            status_code=204,
            headers=CaseInsensitiveDict({'x-account-bytes-used': '368259416'}),
            )
        poe.requests.head.return_value = response_mock

        # Assert that _get_account_ring does what we expect.
        self.assertEqual(s._get_account_usage('AUTH_12bb569bf909441b90791482ae6f9ca9'), 368259416)

        # Assert that _get_account_ring did it in the manner we expected.
        s.account_ring.get_nodes.assert_called_once_with(account='AUTH_12bb569bf909441b90791482ae6f9ca9')
        poe.requests.head.assert_called_once()
        self.assertTrue(poe.requests.head.call_args in [
            call('http://10.24.0.18:6002/sdb/26701/AUTH_12bb569bf909441b90791482ae6f9ca9'),
            call('http://10.24.0.71:6002/sdd/26701/AUTH_12bb569bf909441b90791482ae6f9ca9'),
            call('http://10.24.0.72:6002/sdi/26701/AUTH_12bb569bf909441b90791482ae6f9ca9'),
            ])
