from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Path to the JSON file
json_file_path = 'data.json'

# Function to load data from the JSON file
def load_data():
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)
    else:
        return {"students": []}

# Function to save data to the JSON file
def save_data(data):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

data = load_data()

@app.route('/')
def home():
    return "Welcome to the Flask API!"

# Create a new student
@app.route('/students', methods=['POST'])
def create_student():
    new_student = request.get_json()
    data['students'].append(new_student)
    save_data(data)
    return jsonify({"message": "Student created successfully"}), 201

# Read all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(data)

# Read a specific student by student_number
@app.route('/students/<student_number>', methods=['GET'])
def get_student(student_number):
    student = next((student for student in data['students'] if student['student_number'] == student_number), None)
    if student:
        return jsonify(student)
    else:
        return jsonify({"message": "Student not found"}), 404

# Update a student's information
@app.route('/students/<student_number>', methods=['PUT'])
def update_student(student_number):
    updated_info = request.get_json()
    student = next((student for student in data['students'] if student['student_number'] == student_number), None)
    if student:
        student.update(updated_info)
        save_data(data)
        return jsonify({"message": "Student updated successfully"})
    else:
        return jsonify({"message": "Student not found"}), 404

# Delete a student
@app.route('/students/<student_number>', methods=['DELETE'])
def delete_student(student_number):
    global data
    new_students_list = [student for student in data['students'] if student['student_number'] != student_number]
    if len(new_students_list) != len(data['students']):
        data['students'] = new_students_list
        save_data(data)
        return jsonify({"message": "Student deleted successfully"})
    else:
        return jsonify({"message": "Student not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

