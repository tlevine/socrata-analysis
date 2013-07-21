class Graph:
    def __init__(self):
        self.users = {
            'tables': {},
            'views': {},
            'view_types': {},
        }
        self.tables = {
            'users': {},
            'views': {},
            'view_types': {},
        }
        self.views = {
            'tables': {},
            'users': {},
            'view_types': {},
        }
        self.view_types = {
            'tables': {},
            'users': {},
            'views': {},
        }

    def add(self, view):
        "Given a view's metadata, add the necessary things to the graph."
        view.get('displayType')
        view['owner']['id']
        view['tableId']

    def _add_table(self, tableId, tableAuthor):
        'Add a table (a family of views)'

    def _add_user(self, owner):
        'Add a user (taken from the `owner` field)'
