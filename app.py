from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
users = [
    {
        "email": "srishti@dal.ca",
        "firstName": "Srishti",
        "id": "5abf6783"
    },
    {
        "email": "john@dal.ca",
        "firstName": "John",
        "id": "5abf674563"
    }
]

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        return jsonify({
            "message": "Users retrieved",
            "success": True,
            "users": users
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# GET a single user by ID
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    try:
        user = next((user for user in users if user["id"] == id), None)
        if user:
            return jsonify({
                "success": True,
                "user": user
            })
        else:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# POST a new user
@app.route('/add', methods=['POST'])
def add_user():
    try:
        new_user = request.json
        if "email" not in new_user or "firstName" not in new_user:
            return jsonify({
                "success": False,
                "message": "Invalid request data"
            }), 400
        
        new_user["id"] = generate_unique_id()
        users.append(new_user)
        return jsonify({
            "message": "User added",
            "success": True
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# PUT update user
@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    try:
        updated_user = request.json
        user = next((user for user in users if user["id"] == id), None)
        if user:
            if "email" not in updated_user and "firstName" not in updated_user:
                return jsonify({
                    "success": False,
                    "message": "Invalid request data"
                }), 400
            
            user.update(updated_user)
            return jsonify({
                "message": "User updated",
                "success": True
            })
        else:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# Helper function to generate a unique ID
def generate_unique_id():
    import uuid
    return str(uuid.uuid4())

if __name__ == '__main__':
    app.run(debug=True)
