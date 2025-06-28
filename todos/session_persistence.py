from uuid import uuid4

class Session_Persistence:
    def __init__(self, session):
        self.session = session
        if 'lists' not in self.session:
            self.session['lists'] = []
    
    def all_lists(self):
        return self.session['lists']
    
    def find_list(self, list_id):
        found = (lst for lst in self.session['lists'] if list_id == lst['id'])

        return next(found, None)
    
    def create_new_list(self, title):
        self.all_lists().append({
            'id': str(uuid4()),
            'title': title,
            'todos': []
        })

        self.session.modified = True
        