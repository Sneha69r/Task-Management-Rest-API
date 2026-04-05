from flask import Blueprint, request, jsonify
from app import db
from models import Task
from flask_jwt_extended import jwt_required, get_jwt_identity

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.json

    task = Task(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'pending'),
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({"msg": "Task created"})


@task_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()

    tasks = Task.query.filter_by(user_id=user_id).all()

    result = []
    for t in tasks:
        result.append({
            "id": t.id,
            "title": t.title,
            "status": t.status
        })

    return jsonify(result)


@task_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    task = Task.query.get(id)

    data = request.json
    task.title = data.get('title', task.title)
    task.status = data.get('status', task.status)

    db.session.commit()
    return jsonify({"msg": "Updated"})


@task_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    task = Task.query.get(id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"msg": "Deleted"})