from flask import Flask, json, jsonify, request
from flask_cors import CORS
from models.models import Question, Quiz, Result, db, User
from routes.auth_routes import auth_bp
from flask_jwt_extended import JWTManager,get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash
import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# Config
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Replace with a strong secret key!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=24)

# Initialize extensions
jwt = JWTManager(app)
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)

# ✅ Create tables and update admin password
with app.app_context():
    db.create_all()

    existing_admin = User.query.filter_by(email="admin@quizmaster.com").first()

    if not existing_admin:
        admin_user = User(
        full_name="Admin",
        email="admin@quizmaster.com",
        password=generate_password_hash("admin123"),
        qualification="Admin",
        dob=datetime.date(1990, 1, 1),
        role="admin"
        )
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Admin user created!")

# Routes
@app.route('/')
def home():
    return jsonify({"message": "🚀 Quiz Master API is running!"})

@app.route('/api/user')
@jwt_required()
def get_user():
    try:
        identity = json.loads(get_jwt_identity())
        print("Extracted JWT Identity:", identity)  # Add this line

        if 'role' not in identity or identity['role'] != 'user':
            return jsonify({"message": "Access denied"}), 403

        user = User.query.filter_by(email=identity["email"]).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        return jsonify({"user": {
            "full_name": user.full_name,
            "email": user.email,
            "qualification": user.qualification,
            "dob": user.dob
        }}), 200

    except Exception as e:
        print("Error in /api/user:", str(e))
        return jsonify({"message": "Something went wrong"}), 500
    
@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        identity = json.loads(get_jwt_identity()) 
        print("Extracted Identity:", identity) 

        admin = User.query.filter_by(id=identity["id"], role="admin").first()
        if not admin:
            return jsonify({"message": "Admins only!"}), 403

        users = User.query.all()
        user_list = [{
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "dob": u.dob,
            "qualification": u.qualification,
            "role": u.role
        } for u in users]

        return jsonify({"users": user_list}), 200

    except Exception as e:
        print("Error in /api/admin/users:", str(e))
        return jsonify({"message": "Something went wrong"}), 500

@app.route('/api/admin/questions', methods=['POST'])
@jwt_required()
def create_question():
    try:
        identity = json.loads(get_jwt_identity())
        admin = User.query.filter_by(id=identity["id"], role="admin").first()
        if not admin:
            return jsonify({"message": "Admins only!"}), 403

        data = request.get_json()

        # Extract values from request
        quiz_id = data.get("quiz_id")  # You must pass this from the frontend
        question_text = data.get("question_text")
        question_type = data.get("question_type")  # 'mcq', 'msq', 'numeric', 'text'
        options = data.get("options", [])
        correct_answer = data.get("correct_answer")

        # Basic validation
        if quiz_id is None or not question_text or not question_type or correct_answer is None:
            return jsonify({"message": "Missing required fields"}), 400

        if question_type in ["mcq", "msq"]:
            if not isinstance(options, list) or len(options) < 2:
                return jsonify({"message": "At least 2 options required for MCQ/MSQ"}), 400

        # Store options and answer as JSON strings
        options_json = json.dumps(options) if options else None
        correct_json = json.dumps(correct_answer)

        new_question = Question(
            quiz_id=quiz_id,
            question_text=question_text,
            question_type=question_type,
            options=options_json,
            correct_answer=correct_json
        )

        db.session.add(new_question)
        db.session.commit()

        return jsonify({"message": "Question added successfully!"}), 201

    except Exception as e:
        print("Error in create_question:", str(e))
        return jsonify({"message": "Server error"}), 500

@app.route('/api/admin/questions', methods=['GET'])
@jwt_required()
def get_all_questions():
    try:
        identity = json.loads(get_jwt_identity())
        admin = User.query.filter_by(id=identity["id"], role="admin").first()
        if not admin:
            return jsonify({"message": "Admins only!"}), 403

        questions = Question.query.all()
        question_list = []
        for q in questions:
            question_list.append({
                "id": q.id,
                "quiz_id": q.quiz_id,
                "question_text": q.question_text,
                "question_type": q.question_type,
                "options": json.loads(q.options) if q.options else [],
                "correct_answer": json.loads(q.correct_answer) if isinstance(q.correct_answer, str) else q.correct_answer
            })

        return jsonify({"questions": question_list}), 200

    except Exception as e:
        print("Error in get_all_questions:", str(e))
        return jsonify({"message": "Server error"}), 500
    
@app.route('/api/admin/questions/<int:question_id>', methods=['DELETE'])
@jwt_required()
def delete_question(question_id):
    try:
        identity = json.loads(get_jwt_identity())
        admin = User.query.filter_by(id=identity["id"], role="admin").first()
        if not admin:
            return jsonify({"message": "Admins only!"}), 403

        question = Question.query.get(question_id)
        if not question:
            return jsonify({"message": "Question not found"}), 404

        db.session.delete(question)
        db.session.commit()

        return jsonify({"message": "Question deleted successfully"}), 200
    except Exception as e:
        print("Error deleting question:", e)
        return jsonify({"message": "Server error"}), 500

@app.route('/api/admin/questions/<int:question_id>', methods=['PUT'])
@jwt_required()
def update_question(question_id):
    data = request.get_json()
    print("Received update payload:", data)

    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    question.quiz_id = data.get("quiz_id", question.quiz_id)
    question.question_text = data.get("question_text", question.question_text)
    question.question_type = data.get("question_type", question.question_type)

    # Serialize lists as JSON strings before saving
    options = data.get("options")
    correct_answer = data.get("correct_answer")

    if options is not None:
        question.options = json.dumps(options)

    if correct_answer is not None:
        question.correct_answer = json.dumps(correct_answer)

    try:
        db.session.commit()
        return jsonify({"message": "Question updated successfully"}), 200
    except Exception as e:
        print("Error while updating:", e)
        db.session.rollback()
        return jsonify({"error": "Failed to update question"}), 500

@app.route('/api/admin/quizzes', methods=['POST'])
@jwt_required()
def create_quiz():
    try:
        identity = json.loads(get_jwt_identity())
        admin = User.query.filter_by(id=identity["id"], role="admin").first()
        if not admin:
            return jsonify({"message": "Admins only!"}), 403

        data = request.get_json()
        title = data.get("title")
        description = data.get("description", "")
        total_marks = data.get("total_marks")

        if not title or total_marks is None:
            return jsonify({"message": "Title and total marks are required"}), 400

        new_quiz = Quiz(
            title=title,
            description=description,
            total_marks=total_marks
        )

        db.session.add(new_quiz)
        db.session.commit()

        return jsonify({"message": "Quiz created successfully!"}), 201

    except Exception as e:
        print("Error in create_quiz:", str(e))
        return jsonify({"message": "Server error"}), 500
    
@app.route('/api/quizzes', methods=['GET'])
@jwt_required()
def get_quizzes():
    try:
        identity = json.loads(get_jwt_identity())

        # Both user and admin can access this
        user = User.query.filter_by(id=identity["id"]).first()
        if not user:
            return jsonify({"message": "Unauthorized"}), 403

        quizzes = Quiz.query.all()
        quiz_list = [{
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "total_marks": quiz.total_marks
        } for quiz in quizzes]

        return jsonify({"quizzes": quiz_list}), 200

    except Exception as e:
        print("Error in get_quizzes:", e)
        return jsonify({"message": "Server error"}), 500

@app.route('/api/submit-quiz', methods=['POST'])
@jwt_required()
def submit_quiz():
    try:
        identity = json.loads(get_jwt_identity())
        user = User.query.filter_by(id=identity["id"], role="user").first()
        if not user:
            return jsonify({"message": "Users only!"}), 403

        data = request.get_json()
        quiz_id = data.get("quiz_id")
        answers = data.get("answers")  # [{ question_id: ..., selected_answer: ... }]

        if not quiz_id or not answers:
            return jsonify({"message": "Quiz ID and answers are required"}), 400

        score = 0

        for ans in answers:
            question = Question.query.filter_by(id=ans['question_id']).first()
            if not question:
                continue

            correct = json.loads(question.correct_answer) if isinstance(question.correct_answer, str) else question.correct_answer
            selected = ans['selected_answer']

            if question.question_type == 'msq':
                # Compare sorted lists for MSQ
                if sorted(map(str, correct)) == sorted(map(str, selected)):
                    score += 1
            else:
                # MCQ, numeric, text (simple match)
                if str(correct).strip().lower() == str(selected).strip().lower():
                    score += 1

        result = Result(user_id=user.id, quiz_id=quiz_id, score=score)
        db.session.add(result)
        db.session.commit()

        return jsonify({"message": "Quiz submitted successfully!", "score": score}), 200

    except Exception as e:
        print("Error in submit_quiz:", e)
        return jsonify({"message": "Server error"}), 500

@app.route('/api/quizzes/<int:quiz_id>', methods=['GET'])
@jwt_required()
def get_quiz_by_id(quiz_id):
    try:
        identity = json.loads(get_jwt_identity())

        # Both user and admin can access
        user = User.query.filter_by(id=identity["id"]).first()
        if not user:
            return jsonify({"message": "Unauthorized"}), 403

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({"message": "Quiz not found"}), 404

        # Include associated questions
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        question_list = []
        for q in questions:
            question_list.append({
                "id": q.id,
                "question_text": q.question_text,
                "question_type": q.question_type,
                "options": json.loads(q.options) if q.options else [],
            })

        return jsonify({
            "quiz": {
                "id": quiz.id,
                "title": quiz.title,
                "description": quiz.description,
                "total_marks": quiz.total_marks,
                "questions": question_list
            }
        }), 200

    except Exception as e:
        print("Error in get_quiz_by_id:", e)
        return jsonify({"message": "Server error"}), 500


if __name__ == '__main__':
    app.run(debug=True)
