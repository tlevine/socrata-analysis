from collections import Counter

class Graph:
    def __init__(self):
        pass

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
    def _user(user_id):
        return {
            user_id: {
                'tables': Counter(),
                'views': Counter(),
                'view_types': Counter(),
            }
        }

    @staticmethod
    def _view(view_id):
        return {
            view_id: {
                'users': Counter(),
                'views': Counter(),
                'view_types': Counter(),
            }
        }

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
