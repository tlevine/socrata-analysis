from collections import Counter
from copy import copy

class Graph:
    def __init__(self):
        self.users = {}
        self.views = {}
        self.tables = {}
        self.view_types = {}

    def add(self, view):
        "Given a view's metadata, add the necessary things to the graph."
        user = view['owner']
        table = view['tableId']
        view_type = view.get('displayType', 'table')

        self._add_user(user)
        self._add_view(view)
        self._add_table(table)
        self._add_view_type(view_type)

        self._add_edge('view', view['id'], 'user', user['id'])
        self._add_edge('view', view['id'], 'table', table)
        self._add_edge('view', view['id'], 'view_type', view_type)

        self._add_edge('user', user['id'], 'view', view['id'])
        self._add_edge('user', user['id'], 'table', table)
        self._add_edge('user', user['id'], 'view_type', view_type)

        self._add_edge('table', table, 'user', user['id'])
        self._add_edge('table', table, 'view', view['id'])
        self._add_edge('table', table, 'view_type', view_type)

        self._add_edge('view_type', view_type, 'user', user['id'])
        self._add_edge('view_type', view_type, 'view', view['id'])
        self._add_edge('view_type', view_type, 'table', table)

    def _add_table(self, tableId):
        'Add a table (a family of views)'
        if tableId not in self.tables:
            self.tables.update(NodeFactories._table(tableId))

    def _add_user(self, owner):
        'Add a user (taken from the `owner` field)'
        if owner['id'] not in self.users:
            self.users.update(NodeFactories._user(owner))

    def _add_view(self, view):
        if view['id'] not in self.views:
            self.views.update(NodeFactories._view(view))

    def _add_view_type(self, view_type):
        'Add a view type'
        if view_type not in self.view_types:
            self.view_types.update(NodeFactories._view_type(view_type))

    def _add_edge(self, nodetypea, nodea, nodetypeb, nodeb):
        NODETYPES = {'user', 'view', 'table', 'view_type'}
        if nodetypea not in NODETYPES:
            raise TypeError('"%s" is not a valid node type' % nodetypea)
        elif nodetypeb not in NODETYPES:
            raise TypeError('"%s" is not a valid node type' % nodetypeb)
        elif nodetypea == nodetypeb:
            raise TypeError('The two node types must be different.')
        elif nodea not in getattr(self, nodetypea + 's'):
            raise IndexError('You need to add the A node before creating the edge.')
        elif nodeb not in getattr(self, nodetypeb + 's'):
            raise IndexError('You need to add the B node before creating the edge.')
        getattr(self, nodetypea + 's')[nodea][nodetypeb + 's'].update([nodeb])
        getattr(self, nodetypeb + 's')[nodeb][nodetypea + 's'].update([nodea])

class NodeFactories:
    @staticmethod
    def _user(user):
        result = {
            user['id']: {
                'profile': copy(user),
                'tables': Counter(),
                'views': Counter(),
                'view_types': Counter(),
            }
        }
        del result[user['id']]['profile']['id']
        return result

    @staticmethod
    def _view(view):
        result = {
            view['id']: {
                'profile': copy(view),
                'users': Counter(),
                'tables': Counter(),
                'view_types': Counter(),
            }
        }
        del result[view['id']]['profile']['id']
        return result

    @staticmethod
    def _table(table_id):
        return {
            table_id: {
                'views': Counter(),
                'users': Counter(),
                'view_types': Counter(),
            }
        }

    @staticmethod
    def _view_type(view_type):
        return {
            view_type: {
                'tables': Counter(),
                'users': Counter(),
                'views': Counter(),
            }
        }
