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

    def test_add(self):
        elevator_offenders = {
          "id" : "u3bu-v2bf",
          "name" : "Top Ten Elevator Offenders",
          "attribution" : "Department of Buildings (DOB)",
          "averageRating" : 0,
          "category" : "Housing & Development",
          "createdAt" : 1318294305,
          "description" : "Top Ten Elevator Offenders",
          "displayType" : "table",
          "downloadCount" : 32,
          "numberOfComments" : 0,
          "oid" : 4141679,
          "publicationAppendEnabled" : False,
          "publicationDate" : 1371847810,
          "publicationGroup" : 244589,
          "publicationStage" : "published",
          "rowsUpdatedAt" : 1371847808,
          "rowsUpdatedBy" : "5fuc-pqz2",
          "signed" : False,
          "tableId" : 933163,
          "totalTimesRated" : 0,
          "viewCount" : 710,
          "viewLastModified" : 1371847810,
          "viewType" : "tabular",
          "columns" : [ {
            "id" : 75780594,
            "name" : "Owner",
            "dataTypeName" : "text",
            "fieldName" : "owner",
            "position" : 2,
            "renderTypeName" : "text",
            "tableColumnId" : 1570119,
            "width" : 160,
            "cachedContents" : {
              "non_null" : 10,
              "smallest" : "100 Audubon Holdings, LP",
              "null" : 0,
              "largest" : "Tivoli Towers Housing Co.",
              "top" : [ {
                "count" : 20,
                "item" : "Heights Inter-Neighborhood HDF"
              }, {
                "count" : 19,
                "item" : "1627-1635 Amsterdam Avenue LLC"
              }, {
                "count" : 18,
                "item" : "129-135 Ridge Street, HDFC"
              }, {
                "count" : 17,
                "item" : "Thermald Realty Associates LLP"
              }, {
                "count" : 16,
                "item" : "941 Intervale Realty"
              }, {
                "count" : 15,
                "item" : "885 Third Owner LLC"
              }, {
                "count" : 14,
                "item" : "100 Audubon Holdings, LP"
              }, {
                "count" : 13,
                "item" : "Tivoli Towers Housing Co."
              }, {
                "count" : 12,
                "item" : "Fulton Park Site 4 Houses, Inc."
              }, {
                "count" : 11,
                "item" : "Harlem River Park Houses aka River Park Associates"
              } ]
            },
            "format" : {
            }
          }, {
            "id" : 75780595,
            "name" : "Street Address",
            "dataTypeName" : "text",
            "fieldName" : "street_address",
            "position" : 3,
            "renderTypeName" : "text",
            "tableColumnId" : 1570120,
            "width" : 268,
            "cachedContents" : {
              "non_null" : 10,
              "smallest" : "10 Richman Plaza",
              "null" : 0,
              "largest" : "941 Intervale Avenue",
              "top" : [ {
                "count" : 20,
                "item" : "1694 Davidson Ave"
              }, {
                "count" : 19,
                "item" : "476 West 141 Street"
              }, {
                "count" : 18,
                "item" : "129 Ridge Street"
              }, {
                "count" : 17,
                "item" : "91 East Third Street"
              }, {
                "count" : 16,
                "item" : "941 Intervale Avenue"
              }, {
                "count" : 15,
                "item" : "885 Third Avenue"
              }, {
                "count" : 14,
                "item" : "551 West 170th Street"
              }, {
                "count" : 13,
                "item" : "49 Crown Street"
              }, {
                "count" : 12,
                "item" : "1711 Fulton Street"
              }, {
                "count" : 11,
                "item" : "10 Richman Plaza"
              } ]
            },
            "format" : {
            }
          }, {
            "id" : 75780596,
            "name" : "Location 1",
            "dataTypeName" : "location",
            "fieldName" : "location_1",
            "position" : 4,
            "renderTypeName" : "location",
            "tableColumnId" : 1570121,
            "width" : 220,
            "cachedContents" : {
              "non_null" : 10,
              "smallest" : {
                "longitude" : "-73.91844899972153",
                "latitude" : "40.82557699997852",
                "human_address" : "{\"address\":\"10 Richman Plaza\",\"city\":\"Bronx\",\"state\":\"NY\",\"zip\":\"\"}"
              },
              "null" : 0,
              "largest" : {
                "longitude" : "-73.89692832141648",
                "latitude" : "40.821035486559545",
                "human_address" : "{\"address\":\"941 Intervale Avenue\",\"city\":\"Bronx\",\"state\":\"NY\",\"zip\":\"\"}"
              },
              "top" : [ {
                "count" : 20,
                "item" : {
                  "longitude" : "-73.91400146662433",
                  "latitude" : "40.84694407041451",
                  "human_address" : "{\"address\":\"1694 Davidson Ave\",\"city\":\"Bronx\",\"state\":\"NY\",\"zip\":\"\"}"
                }
              }, {
                "count" : 19,
                "item" : {
                  "longitude" : "-73.94885071508074",
                  "latitude" : "40.82240435307847",
                  "human_address" : "{\"address\":\"476 141 Street\",\"city\":\"New York\",\"state\":\"NY\",\"zip\":\"\"}"
                }
              }, {
                "count" : 18,
                "item" : {
                  "longitude" : "-73.98289508051067",
                  "latitude" : "40.71950537368474",
                  "human_address" : "{\"address\":\"129 Ridge Street\",\"city\":\"New York\",\"state\":\"NY\",\"zip\":\"\"}"
                }
              }, {
                "count" : 17,
                "item" : {
                  "longitude" : "-73.9869510002884",
                  "latitude" : "40.756053999992105",
                  "human_address" : "{\"address\":\"91 Third Street\",\"city\":\"New York\",\"state\":\"NY\",\"zip\":\"\"}"
                }
              }, {
                "count" : 16,
                "item" : {
                  "longitude" : "-73.89692832141648",
                  "latitude" : "40.821035486559545",
                  "human_address" : "{\"address\":\"941 Intervale Avenue\",\"city\":\"Bronx\",\"state\":\"NY\",\"zip\":\"\"}"
                }
              }, {
                "count" : 15,
                "item" : {
                  "longitude" : "-73.96916243312324",
                  "latitude" : "40.75800534975912",
                  "human_address" : "{\"address\":\"885 Third Avenue\",\"city\":\"New York\",\"state\":\"NY\",\"zip\":\"\"}"
                }
              }, {
                "count" : 14,
                "item" : {
                  "longitude" : "-73.93800768357518",
                  "latitude" : "40.8419275035329",
                  "human_address" : "{\"address\":\"551 170th Street\",\"city\":\"New York\",\"state\":\"NY\",\"zip\":\"\"}"
                }
              }, {
                "count" : 13,
                "item" : {
                  "longitude" : "-73.95991278165833",
                  "latitude" : "40.667314293900304",
                  "human_address" : "{\"address\":\"49 Crown Street\",\"city\":\"Brooklyn\",\"state\":\"NY\",\"zip\":\"\"}"
                }
              }, {
                "count" : 12,
                "item" : {
                  "longitude" : "-73.93017152973913",
                  "latitude" : "40.67936060442289",
                  "human_address" : "{\"address\":\"1711 Fulton Street\",\"city\":\"Brooklyn\",\"state\":\"NY\",\"zip\":\"\"}"
                }
              }, {
                "count" : 11,
                "item" : {
                  "longitude" : "-73.91844899972153",
                  "latitude" : "40.82557699997852",
                  "human_address" : "{\"address\":\"10 Richman Plaza\",\"city\":\"Bronx\",\"state\":\"NY\",\"zip\":\"\"}"
                }
              } ]
            },
            "format" : {
            },
            "subColumnTypes" : [ "human_address", "latitude", "longitude", "machine_address", "needs_recoding" ]
          } ],
          "grants" : [ {
            "inherited" : False,
            "type" : "viewer",
            "flags" : [ "public" ]
          } ],
          "metadata" : {
            "custom_fields" : {
              "Update" : {
                "Update Frequency" : "As needed"
              }
            },
            "rdfSubject" : "0"
          },
          "owner" : {
            "id" : "txun-eb7e",
            "displayName" : "Albert Webber",
            "emailUnsubscribed" : False,
            "privacyControl" : "login",
            "profileLastModified" : 1370657621,
            "roleName" : "administrator",
            "screenName" : "Albert Webber",
            "rights" : [ "create_datasets", "edit_others_datasets", "edit_sdp", "edit_site_theme", "moderate_comments", "manage_users", "chown_datasets", "edit_nominations", "approve_nominations", "feature_items", "federations", "manage_stories", "manage_approval", "change_configurations", "view_domain", "view_others_datasets", "edit_pages", "create_pages", "short_session" ]
          },
          "query" : {
          },
          "rights" : [ "read" ],
          "tableAuthor" : {
            "id" : "don't use this field",
            "displayName" : "Albert Webber",
            "emailUnsubscribed" : False,
            "privacyControl" : "login",
            "profileLastModified" : 1370657621,
            "roleName" : "administrator",
            "screenName" : "Albert Webber",
            "rights" : [ "create_datasets", "edit_others_datasets", "edit_sdp", "edit_site_theme", "moderate_comments", "manage_users", "chown_datasets", "edit_nominations", "approve_nominations", "feature_items", "federations", "manage_stories", "manage_approval", "change_configurations", "view_domain", "view_others_datasets", "edit_pages", "create_pages", "short_session" ]
          },
          "tags" : [ "dob", "department of buildings", "buildings", "disciplinary actions", "electrician", "plumber", "master plumber", "architect", "engineer", "surrender of privileges", "elevator", "offender", "2010", "2011", "clean web" ],
          "flags" : [ "default" ]
        }
        self.graph.add(elevator_offenders)

        n.assert_equal(self.graph.views["u3bu-v2bf"]['users'], Counter({'txun-eb7e': 1}))
        n.assert_equal(self.graph.tables[933163]['users'], Counter({'txun-eb7e': 1}))
        n.assert_equal(self.graph.view_types["table"]['users'], Counter({'txun-eb7e': 1}))

        n.assert_equal(self.graph.views['u3bu-v2bf']['tables'], Counter({933163: 1}))
        n.assert_equal(self.graph.users['txun-eb7e']['tables'], Counter({933163: 1}))
        n.assert_equal(self.graph.view_types["table"]['tables'], Counter({933163: 1}))

        n.assert_equal(self.graph.tables[933163]['views'], Counter({'u3bu-v2bf': 1}))
        n.assert_equal(self.graph.users['txun-eb7e']['views'], Counter({'u3bu-v2bf': 1}))
        n.assert_equal(self.graph.view_types["table"]['views'], Counter({'u3bu-v2bf': 1}))

        n.assert_equal(self.graph.views['u3bu-v2bf']['view_types'], Counter({'table': 1}))
        n.assert_equal(self.graph.tables[933163]['view_types'], Counter({'table': 1}))
        n.assert_equal(self.graph.users['txun-eb7e']['view_types'], Counter({'table': 1}))

        # Doing it again shouldn't change anything.
        self.graph.add(elevator_offenders)

        n.assert_equal(self.graph.views["u3bu-v2bf"]['users'], Counter({'txun-eb7e': 1}))
        n.assert_equal(self.graph.tables[933163]['users'], Counter({'txun-eb7e': 1}))
        n.assert_equal(self.graph.view_types["table"]['users'], Counter({'txun-eb7e': 1}))

        n.assert_equal(self.graph.views['u3bu-v2bf']['tables'], Counter({933163: 1}))
        n.assert_equal(self.graph.users['txun-eb7e']['tables'], Counter({933163: 1}))
        n.assert_equal(self.graph.view_types["table"]['tables'], Counter({933163: 1}))

        n.assert_equal(self.graph.tables[933163]['views'], Counter({'u3bu-v2bf': 1}))
        n.assert_equal(self.graph.users['txun-eb7e']['views'], Counter({'u3bu-v2bf': 1}))
        n.assert_equal(self.graph.view_types["table"]['views'], Counter({'u3bu-v2bf': 1}))

        n.assert_equal(self.graph.views['u3bu-v2bf']['view_types'], Counter({'table': 1}))
        n.assert_equal(self.graph.tables[933163]['view_types'], Counter({'table': 1}))
        n.assert_equal(self.graph.users['txun-eb7e']['view_types'], Counter({'table': 1}))

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
