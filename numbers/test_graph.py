import nose.tools as n
import unittest

from collections import Counter
from graph import Graph, NodeFactories

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

    def test_add_user(self):
        owner = {
            "id" : "xbqz-g2u5",
            "displayName" : "Matt Smith",
            "emailUnsubscribed" : False,
            "privacyControl" : "login",
            "profileLastModified" : 1300299847,
            "roleName" : "administrator",
            "screenName" : "Matt Smith",
            "rights" : [ "create_datasets", "edit_others_datasets", "edit_sdp", "edit_site_theme", "moderate_comments", "manage_users", "chown_datasets", "edit_nominations", "approve_nominations", "feature_items", "federations", "manage_stories", "manage_approval", "change_configurations", "view_domain", "view_others_datasets", "edit_pages", "create_pages" ]
          }
        self.graph._add_user(owner)
#       n.assert_dict_equal(self.graph.users, Counter({owner['id']: 1}))

class TestNodeFactories(unittest.TestCase):
    def test_user(self):
        observed = NodeFactories._user({'id': 'abcd-efhg'})
        expected = {
            'abcd-efhg': {
                'profile': {},
                'tables': Counter(),
                'views': Counter(),
                'view_types': Counter(),
            }
        }
        n.assert_dict_equal(observed, expected)

    def test_view(self):
        observed = NodeFactories._view({'id': 'abcd-efhg', 'foo': 'bar'})
        expected = {
            'abcd-efgh': {
                'profile': {'foo': 'bar'},
                'users': Counter(),
                'views': Counter(),
                'view_types': Counter(),
            }
        }

    def test_table(self):
        observed = NodeFactories._table('abcd-efhg')
        expected = {
            'abcd-efgh': {
                'tables': Counter(),
                'users': Counter(),
                'view_types': Counter(),
            }
        }

    def test_view_type(self):
        observed = NodeFactories._view_type('abcd-efhg')
        expected = {
            'abcd-efgh': {
                'tables': Counter(),
                'users': Counter(),
                'views': Counter(),
            }
        }
