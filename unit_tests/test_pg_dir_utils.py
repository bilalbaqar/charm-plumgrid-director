from mock import MagicMock
from collections import OrderedDict
import charmhelpers.contrib.openstack.templating as templating

templating.OSConfigRenderer = MagicMock()

import pg_dir_utils as nutils

from test_utils import (
    CharmTestCase,
)
import charmhelpers.core.hookenv as hookenv


TO_PATCH = [
    'os_release',
    'neutron_plugin_attribute',
]


class DummyContext():

    def __init__(self, return_value):
        self.return_value = return_value

    def __call__(self):
        return self.return_value


class TestPGDirUtils(CharmTestCase):

    def setUp(self):
        super(TestPGDirUtils, self).setUp(nutils, TO_PATCH)
        # self.config.side_effect = self.test_config.get

    def tearDown(self):
        # Reset cached cache
        hookenv.cache = {}

    def test_register_configs(self):
        class _mock_OSConfigRenderer():
            def __init__(self, templates_dir=None, openstack_release=None):
                self.configs = []
                self.ctxts = []

            def register(self, config, ctxt):
                self.configs.append(config)
                self.ctxts.append(ctxt)

        self.os_release.return_value = 'trusty'
        templating.OSConfigRenderer.side_effect = _mock_OSConfigRenderer
        _regconfs = nutils.register_configs()
        confs = [nutils.PG_KA_CONF,
                 nutils.PG_CONF,
                 nutils.PG_DEF_CONF,
                 nutils.PG_HN_CONF,
                 nutils.PG_HS_CONF,
                 nutils.PG_IFCS_CONF,
                 nutils.OPS_CONF]
        self.assertItemsEqual(_regconfs.configs, confs)

    def test_resource_map(self):
        _map = nutils.resource_map()
        svcs = ['plumgrid']
        confs = [nutils.PG_KA_CONF]
        [self.assertIn(q_conf, _map.keys()) for q_conf in confs]
        self.assertEqual(_map[nutils.PG_KA_CONF]['services'], svcs)

    def test_restart_map(self):
        _restart_map = nutils.restart_map()
        expect = OrderedDict([
            (nutils.PG_CONF, ['plumgrid']),
            (nutils.PG_KA_CONF, ['plumgrid']),
            (nutils.PG_DEF_CONF, ['plumgrid']),
            (nutils.PG_HN_CONF, ['plumgrid']),
            (nutils.PG_HS_CONF, ['plumgrid']),
            (nutils.OPS_CONF, ['plumgrid']),
            (nutils.PG_IFCS_CONF, []),
        ])
        self.assertEqual(expect, _restart_map)
        for item in _restart_map:
            self.assertTrue(item in _restart_map)
            self.assertTrue(expect[item] == _restart_map[item])
