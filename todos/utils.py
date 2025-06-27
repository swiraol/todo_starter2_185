def error_for_list_title(title, lists):

    if any(title.casefold() == lst['title'].casefold() for lst in lists):
        return "The title must be unique."
    elif not 1 <= len(title) <= 100:
        return "The title must be 100 characters or less"
    else:
        return None

def error_for_todo_title(title):
    if not 0 < len(title) <= 100:
        return "Todo title must be between 1 and 100 characters"
    
    return None

def find_todo_by_id(todo_id, lst):
    for item in lst:
        print(todo_id, item['id'])
        if todo_id == item['id']:
            return item
    return None

def todos_remaining(lst):
    return sum(1 for todo in lst['todos'] if not todo['completed'])

def is_list_completed(lst):
    return len(lst['todos']) > 0 and todos_remaining(lst) == 0

def is_todo_completed(todo):
    return todo['completed']

def sort_items(items, func):
    sorted_items = sorted(items, key=lambda item: item['title'].casefold())

    incomplete_list = [item for item in sorted_items if not func(item)]
    completed_list = [item for item in sorted_items if func(item)]

    return incomplete_list + completed_list