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





@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': error.description}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404



if __name__ == '__main__':
    app.run(debug=True)