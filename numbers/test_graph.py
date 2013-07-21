import nose.tools as n
import unittest

from collections import Counter
from graph import Graph, NodeFactories

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

    def test_init(self):
        n.assert_dict_equal(self.graph.users, {})
        n.assert_dict_equal(self.graph.views, {})
        n.assert_dict_equal(self.graph.tables, {})
        n.assert_dict_equal(self.graph.view_types, {})

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
        n.assert_list_equal(self.graph.users.keys(), [owner['id']])

    def test_add_view(self):
        self.graph._add_view({'id': 'abcd-efgh'})
        n.assert_list_equal(self.graph.views.keys(), ['abcd-efgh'])
    #   n.assert_list_equal(self.graph.tables['abcd-efgh']['users'].keys(), ['xxxx-xxxx'])
    #   n.assert_list_equal(self.graph.tables['xxxx-xxxx']['tables'].keys(), ['abcd-efgh'])

    def test_add_table(self):
        self.graph._add_table('abcd-efgh')
        n.assert_list_equal(self.graph.tables.keys(), ['abcd-efgh'])

    def test_add_view_type(self):
        self.graph._add_view_type('abcd-efgh')
        n.assert_list_equal(self.graph.view_types.keys(), ['abcd-efgh'])

    def test_add_edge(self):
        with n.assert_raises(IndexError):
            self.graph._add_edge('user', 'xxxx-xxxx', 'view', 'yyyy-yyyy')

        self.graph._add_user({'id': 'xxxx-xxxx'})
        self.graph._add_view({'id': 'yyyy-yyyy'})

        self.graph._add_edge('user', 'xxxx-xxxx', 'view', 'yyyy-yyyy')
        n.assert_equal(self.graph.users['xxxx-xxxx']['views'], Counter({'yyyy-yyyy': 1}))
        n.assert_equal(self.graph.views['yyyy-yyyy']['users'], Counter({'xxxx-xxxx': 1}))
        self.graph._add_edge('user', 'xxxx-xxxx', 'view', 'yyyy-yyyy')
        n.assert_equal(self.graph.users['xxxx-xxxx']['views'], Counter({'yyyy-yyyy': 2}))
        n.assert_equal(self.graph.views['yyyy-yyyy']['users'], Counter({'xxxx-xxxx': 2}))

        with n.assert_raises(TypeError):
            self.graph._add_edge('user', 'xxxx-xxxx', 'user', 'yyyy-yyyy')

        with n.assert_raises(TypeError):
            self.graph._add_edge('not-an-entity-type', 'xxxx-xxxx', 'user', 'yyyy-yyyy')

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
