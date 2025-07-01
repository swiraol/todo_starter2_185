from uuid import uuid4

class SessionPersistence:
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

    def update_list_by_id(self, new_title, id):
        lst = self.find_list(id)
        if lst:
            lst['title'] = title
            self.session.modified = True

    def delete_list(self, id):
        self.session['lists'] = [lst for lst in self.session['lists'] if not lst['id'] == id]
        self.session.modified = True

    def create_new_todo(self, list_id, todo_title):
        lst = self.find_list(list_id)

        if lst:
            lst['todos'].append({
                'title': todo_title,
                'id': str(uuid4()),
                'completed': False,
            })
        
        self.session.modified = True
    
    def delete_todo_from_list(self, list_id, todo_id):
        lst = self.find_list(list_id)

        if lst:
            lst['todos'] = [todo for todo in lst['todos'] if todo['id'] != todo_id]

        self.session.modified = True
    
    def update_todo_status(list_id, todo_id, is_completed):
        lst = self.find_list(list_id)

        if lst:
            for todo in lst['todos']:
                if todo['id'] == todo_id:
                    todo['completed'] = is_completed
        
        self.session.modified = True
    
    def mark_all_todos_completed(list_id):
        lst = find_list(list_id)

        if lst: 
            for todo in lst['todos']:
                todo['completed'] = True

        self.session.modified = True