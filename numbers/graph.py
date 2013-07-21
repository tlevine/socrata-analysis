from collections import Counter

class Graph:
    def __init__(self):
        self.users = {}
        self.views = {}
        self.tables = {}
        self.view_types = {}

    def add(self, view):
        "Given a view's metadata, add the necessary things to the graph."
        view.get('displayType')
        view['owner']['id']
        view['tableId']
        view['id']

    def _add_table(self, tableId, tableAuthor):
        'Add a table (a family of views)'

    def _add_user(self, owner):
        'Add a user (taken from the `owner` field)'

class NodeFactories:
    @staticmethod
    def _user(user):
        result = {
            user['id']: {
                'profile': user,
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
                'profile': view,
                'users': Counter(),
                'views': Counter(),
                'view_types': Counter(),
            }
        }
        del result[view['id']]['profile']['id']
        return result

    @staticmethod
    def _table(table_id):
        return {
            table_id: {
                'tables': Counter(),
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
