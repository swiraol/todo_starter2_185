import secrets
from uuid import uuid4
from functools import wraps 
import os

from flask import (Flask, 
                   g,
                   redirect,
                   render_template, 
                   request,
                   session,
                   url_for,
                   flash,
)
from werkzeug.exceptions import NotFound
from todos.utils import (
    error_for_list_title, 
    error_for_todo_title, 
    find_todo_by_id, 
    is_list_completed,
    todos_remaining,
    sort_items,
    is_todo_completed
)

from todos.session_persistence import SessionPersistence

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

def require_list(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        list_id = kwargs.get('list_id')    
        todo_lst = g.storage.find_list(list_id, session['lists'])
        if not todo_lst:
            raise NotFound(description="List not found")
        return f(todo_lst=todo_lst, *args, **kwargs)
    
    return decorated_function

def require_todo(f):
    @wraps(f)
    @require_list
    def decorated_function(todo_lst, *args, **kwargs):
        todo_id = kwargs.get('todo_id')
        todo_item = find_todo_by_id(todo_id, todo_lst['todos'])
        if not todo_item:
            raise NotFound(description="Todo not found")
        return f(todo_lst=todo_lst, todo_item=todo_item, *args, **kwargs)
    
    return decorated_function

@app.context_processor
def list_utilities_processor():
    return dict(
        is_list_completed=is_list_completed,
    )

@app.before_request
def load_session():
    session['lists'] = session.get('lists', [])
    g.storage = SessionPersistence(session)

@app.route("/")
def index():

    return redirect(url_for('get_lists'))

@app.route('/lists/new')
def add_todo_list():

    return render_template('new_list.html')

@app.route('/lists', methods=["GET"])
def get_lists():
    lists = sort_items(g.storage.all_lists(), is_list_completed)
    return render_template('lists.html', lists=lists, todos_remaining=todos_remaining)

@app.route('/lists', methods=["POST"])
def create_list():
    title = request.form.get('list_title', "").strip()
    error = error_for_list_title(title, g.storage.all_lists())

    if error:
        flash(error, "error")
        return render_template('new_list.html', title=title)
    
    g.storage.create_new_list(title)    
    flash('The list has been added.', 'success')
    return redirect(url_for('get_lists'))

@app.route('/lists/<list_id>', methods=["GET"])
@require_list
def show_list(todo_lst, list_id):
    todo_lst['todos'] = sort_items(todo_lst['todos'], is_todo_completed)
    return render_template("list.html", todo_lst=todo_lst)

@app.route('/lists/<list_id>', methods=["POST"])
@require_list
def update_list(todo_lst, list_id):
    all_lsts = session['lists']
    title = request.form.get('title', '')
    
    validation_fails = error_for_list_title(title, all_lsts)

    if validation_fails:
        flash(validation_fails, "error")
        return render_template("edit_list.html", list_id=list_id, title=title, todo_lst=todo_lst)
    
    todo_lst['title'] = title 
    flash('List is updated', 'success')
    session.modified = True

    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/todos', methods=["POST"])
@require_list
def create_todo(todo_lst, list_id):
    todo_title = request.form.get('todo', None).strip()

    error = error_for_todo_title(todo_title)
    if error:
        flash(error, "error")
        return render_template('list.html', todo_lst=todo_lst)
    print("all lists: ", session['lists'])
    print("todo_lst: ", todo_lst)
    todo_lst['todos'].append({
        'title': todo_title, 
        'id': str(uuid4()), 
        'completed': False,
    })
    
    flash("The todo was added.", "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/complete_all', methods=['POST'])
@require_list
def complete_all_todos(todo_lst, list_id):
    
    for todo in todo_lst['todos']:
        todo['completed'] = True
    
    session.modified = True
    flash("All todos are completed", "success")

    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/todos/<todo_id>/toggle', methods=['POST'])
@require_todo
def update_todo_status(todo_lst, todo_item, list_id, todo_id):
    
    is_completed = request.form.get('completed').lower() == 'true'
    todo_item['completed'] = is_completed

    flash('You completed an item', 'success')
    session.modified = True
    
    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/todos/<todo_id>/delete', methods=["POST"])
@require_todo
def delete_todo(todo_lst, todo_item, list_id, todo_id):
    
    todo_lst['todos'] = [item for item in todo_lst['todos'] if item != todo_item]
    # print("todo_item after del: ", todo_item)
    flash("You removed a todo item", "success")
    session.modified = True
    return redirect(url_for("show_list", list_id=list_id))

@app.route('/lists/<list_id>/edit', methods=["GET"])
@require_list
def edit_list(todo_lst, list_id):
    return render_template('edit_list.html', todo_lst=todo_lst)

@app.route('/lists/<list_id>/delete', methods=["POST"])
@require_list
def delete_list(todo_lst, list_id):
    
    session['lists'] = [todo_lst_dict for todo_lst_dict in session['lists'] if not list_id == todo_lst_dict['id']]

    session.modified = True
    flash('List removed', 'success')

    return redirect(url_for('get_lists'))

if __name__ == "__main__":
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True, port=5003)