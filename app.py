from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # SQLite database file path
db = SQLAlchemy(app)

#defining the Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    due_date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', due_date='{self.due_date}', status='{self.status}')"


with app.app_context():
    db.create_all()


#defining the creating task method
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data or 'due_date' not in data or 'status' not in data:
        abort(400, 'Missing required fields')
    new_task = Task(title=data['title'], description=data.get('description', ''), due_date=data['due_date'],
                    status=data['status'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'})

#Method to get task with ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date,
            'status': task.status
        }
        return jsonify(task_data)
    return jsonify({'message': 'Task not found'}), 404

#method to update the task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        data = request.get_json()
        if not data or 'title' not in data or 'due_date' not in data or 'status' not in data:
            abort(400, 'Missing required fields')
        task.title = data['title']
        task.description = data.get('description', '')
        task.due_date = data['due_date']
        task.status = data['status']
        db.session.commit()
        return jsonify({'message': 'Task updated successfully'})
    return jsonify({'message': 'Task not found'}), 404

#method to delete the task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})
    return jsonify({'message': 'Task not found'}), 404




@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': error.description}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404



if __name__ == '__main__':
    app.run(debug=True)