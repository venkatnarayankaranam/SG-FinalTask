from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

tasks = [
    {"title": "Buy groceries", "done": False},
    {"title": "Complete assignment", "done": True}
]

@main.route('/')
def index():
    return render_template("index.html", tasks=tasks)

@main.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    tasks.append({"title": title, "done": False})
    return redirect(url_for('main.index'))

@main.route('/complete/<int:task_id>')
def complete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = True
    return redirect(url_for('main.index'))
