from flask import Flask, request, jsonify, send_from_directory
import openai # Added
import os # Added
from dotenv import load_dotenv # Added

# Load environment variables from .env file
load_dotenv() # Added

app = Flask(__name__)

# Initialize OpenAI client
# It's good practice to check if the key exists and handle it,
# but the check will be done within the route for a more specific error message.
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = openai.OpenAI(api_key=api_key)
else:
    client = None # Will be checked in the route

@app.route('/api/process_statement', methods=['POST'])
def process_statement():
    """
    API endpoint to receive a problem statement and return a processed response
    using OpenAI API.
    Expects JSON input: {"problem_statement": "..."}
    Returns JSON response: {"original_statement": "...", "summary": "...", "keywords": [...], "processing_status": "..."}
    """
    if not client: # Check if OpenAI client was initialized
        return jsonify({"error": "OpenAI API key not configured or missing. Please set the OPENAI_API_KEY environment variable."}), 500

    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Invalid JSON format", "details": str(e)}), 400

    if not data or 'problem_statement' not in data:
        return jsonify({"error": "Missing 'problem_statement' in request JSON"}), 400

    problem_statement = data['problem_statement']

    if not isinstance(problem_statement, str) or not problem_statement.strip():
        return jsonify({"error": "'problem_statement' must be a non-empty string"}), 400
        
    # --- Start OpenAI API Integration ---
    prompt_messages = [
        {"role": "system", "content": "You are an expert business analyst assistant. Your task is to provide a concise summary and extract key entities/keywords from the user's problem statement. Format your response clearly with 'Summary:' on one line, followed by the summary, and 'Keywords:' on another line, followed by a comma-separated list of keywords."},
        {"role": "user", "content": f"Problem Statement: {problem_statement}\n\nPlease provide a one-sentence summary and list up to 5 main keywords or entities. For example:\nSummary: [Your summary here].\nKeywords: keyword1, keyword2, keyword3, keyword4, keyword5."}
    ]

    summary_text = "Could not parse summary from AI response."
    keywords_list = []
    processing_status = "error_ai_processing" # Default status

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=prompt_messages
        )
        llm_output_text = response.choices[0].message.content.strip()

        # Attempt to parse the LLM output
        # Expected format:
        # Summary: [The summary sentence].
        # Keywords: keyword1, keyword2, keyword3.
        
        parsed_summary = False
        parsed_keywords = False

        lines = llm_output_text.split('\n')
        for line in lines:
            if line.lower().startswith("summary:"):
                summary_text = line.split("summary:", 1)[1].strip()
                parsed_summary = True
            elif line.lower().startswith("keywords:"):
                keywords_raw = line.split("keywords:", 1)[1].strip()
                # Remove trailing period if present before splitting
                if keywords_raw.endswith('.'):
                    keywords_raw = keywords_raw[:-1]
                keywords_list = [k.strip() for k in keywords_raw.split(',') if k.strip()]
                parsed_keywords = True
        
        if parsed_summary and parsed_keywords:
            processing_status = "success_real_ai"
        else:
            # Fallback if specific parsing fails - use the whole output as summary
            # and log this occurrence or set a specific status.
            summary_text = f"AI Response (could not parse specifically): {llm_output_text}"
            keywords_list = [] # No reliable keywords if parsing failed
            processing_status = "success_real_ai_parsing_failed"


    except openai.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        return jsonify({"error": "Error communicating with OpenAI API", "details": str(e)}), 500
    except Exception as e:
        # Handle other unhandled errors
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred during AI processing", "details": str(e)}), 500
    # --- End OpenAI API Integration ---

    response_data = {
        "original_statement": problem_statement,
        "summary": summary_text,
        "keywords": keywords_list,
        "processing_status": processing_status
    }

    return jsonify(response_data), 200

@app.route('/')
def serve_index():
    """Serves the index.html file from the current directory (project root)."""
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
