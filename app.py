from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/process_statement', methods=['POST'])
def process_statement():
    """
    API endpoint to receive a problem statement and return a mock processed response.
    Expects JSON input: {"problem_statement": "..."}
    Returns JSON response: {"original_statement": "...", "summary": "...", "keywords": [...], "processing_status": "..."}
    """
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Invalid JSON format", "details": str(e)}), 400

    if not data or 'problem_statement' not in data:
        return jsonify({"error": "Missing 'problem_statement' in request JSON"}), 400

    problem_statement = data['problem_statement']

    if not isinstance(problem_statement, str):
        return jsonify({"error": "'problem_statement' must be a string"}), 400
        
    # Mock AI Processing
    # Ensure problem_statement is not empty for keyword generation
    first_word = ""
    if problem_statement and problem_statement.strip(): # Check if statement is not empty or just whitespace
        first_word = problem_statement.split(' ')[0]
    else: # Handle empty or whitespace-only problem_statement
        problem_statement = "[No statement provided]" # Provide a default for summary if it's empty
        first_word = "empty_statement"


    summary = f"Summary of '{problem_statement[:30]}...': This statement needs careful analysis and further refinement."
    
    keywords = ["analysis", "requirements", "stakeholder_input", f"{first_word.lower()}"]

    response_data = {
        "original_statement": problem_statement if problem_statement != "[No statement provided]" else data.get('problem_statement', ''), # return original empty string if it was empty
        "summary": summary,
        "keywords": keywords,
        "processing_status": "success_mock"
    }

    return jsonify(response_data), 200

@app.route('/')
def home():
    """A simple route for the home page to verify the app is running."""
    return "Flask API for AI Processing is running!"

if __name__ == '__main__':
    # Runs the Flask development server
    # Debug mode should be False in a production environment
    app.run(debug=True, port=5000)
