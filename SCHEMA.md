session (a Python dict-like object that represents the top-level container for user state): {}

{
    'lists': [
      {}, # <-- This is a TodoListDict (a dictionary) 
      {} # <-- This is another TodoListDict (a dictionary)
    ],   # <-- The value for 'lists' key is a Python LIST
    '_flashes': [], # <-- The value for '_flashes' key is a Python LIST
    # ... other Flask session keys
}

TodoListDict (a Python dict that represents a single Todo List): {}

{
    'id': 'str',        # UUID string
    'title': 'str',     # List title string
    'todos': [],        # <-- This is a Python LIST (of TodoItemDicts)
}

TodoItemDict (a Python dict that represents a single Todo Item within a list)

{
    'id': 'str',            # UUID string
    'title': 'str',         # Todo item title string
    'completed': 'bool'     # Boolean 
}

# Example of what session['lists'] might contain:

session['lists'] = [
    # --- Start of the first TodoListDict ---
    {
        'id': 'abc-123-uuid-list-1',
        'title': 'Groceries for the Weekend',
        'todos': [
            # --- Start of first TodoItemDict within 'Groceries for the Weekend' ---
            {
                'id': 'xyz-456-uuid-todo-a',
                'title': 'Buy Milk',
                'completed': False
            },
            # --- End of first TodoItemDict ---

            # --- Start of second TodoItemDict within 'Groceries for the Weekend'--- 
            {
                'id': 'def-789-uuid-todo-b',
                'title': 'Pick up Eggs',
                'completed': True
            }
            # --- End of second TodoItemDict --- 
        ]
    },
    # --- End of first TodoList Dict ---

    # --- Start of second TodoListDict --- 
    {
        'id': 'ghi-012-uuid-list-2',
        'title': 'Morning Chores',
        'todos': [] # An empty list of todo items for this list
    }
    # --- End of the second TodoListDict ---
]

# Example of session['_flashes'] after two flashes: 
session['_flashes'] = [
    ('success', 'The list has been added.'),
    ('error', 'Title must be unique.')
]