from flask import Flask, request, jsonify
import google.generativeai as genai
from app import process_upload
# api_key="AIzaSyAVQbBfLAIbuv7rEJGqC5nOnPGmiuuKnBU"
genai.configure()
app = Flask(__name__)

model = genai.GenerativeModel("gemini-1.5-flash")

def get_summary(extracted_text):
    
    # Make the request to the Gemini API
    response = model.generate_content(f"Give the Summary for the PDF File extracted text: {extracted_text}")
    return response.text


@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        # Check if the request has a file
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No selected file"}), 400
            
            # Extract text from the PDF file
            extracted_text, summary = process_upload(file)
        
        # Check if the request has text data
        elif 'text' in request.json:
            extracted_text = request.json.get('text')
            if not extracted_text:
                return jsonify({"error": "No text provided"}), 400
        else:
            return jsonify({"error": "No file or text provided"}), 400
        
        # Get the summary
        summary = get_summary(extracted_text)
        
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
