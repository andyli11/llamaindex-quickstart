from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
import tempfile
from main import (
    load_from_type, build_query_engine, generate_summary, generate_preview,
    search_web_with_google, answer_with_gemini, is_answer_not_found
)

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Store query engines in memory (in production, use Redis or similar)
query_engines = {}
document_summaries = {}
session_documents = {}  # Store documents for each session to support adding context

UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_content():
    try:
        session_id = str(uuid.uuid4())
        
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, f"{session_id}_{filename}")
                file.save(filepath)
                
                # Determine file type
                file_ext = filename.rsplit('.', 1)[1].lower()
                input_type = 'pdf' if file_ext == 'pdf' else 'image'
                
                # Process the file
                docs = load_from_type(input_type, filepath)
                query_engine = build_query_engine(docs)
                summary = generate_summary(docs, input_type)
                
                # Store in memory
                query_engines[session_id] = query_engine
                document_summaries[session_id] = summary
                session_documents[session_id] = docs
                
                # Clean up uploaded file
                os.remove(filepath)
                
                return jsonify({
                    'success': True,
                    'session_id': session_id,
                    'summary': summary,
                    'content_type': input_type
                })
                
        elif request.json:
            data = request.json
            if 'url' in data:
                docs = load_from_type('url', data['url'])
                query_engine = build_query_engine(docs)
                summary = generate_summary(docs, 'url')
                
                query_engines[session_id] = query_engine
                document_summaries[session_id] = summary
                session_documents[session_id] = docs
                
                return jsonify({
                    'success': True,
                    'session_id': session_id,
                    'summary': summary,
                    'content_type': 'url'
                })
                
            elif 'text' in data:
                docs = load_from_type('text', data['text'])
                query_engine = build_query_engine(docs)
                summary = generate_summary(docs, 'text')
                
                query_engines[session_id] = query_engine
                document_summaries[session_id] = summary
                session_documents[session_id] = docs
                
                return jsonify({
                    'success': True,
                    'session_id': session_id,
                    'summary': summary,
                    'content_type': 'text'
                })
        
        return jsonify({'success': False, 'error': 'No valid content provided'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/query', methods=['POST'])
def query_document():
    try:
        data = request.json
        session_id = data.get('session_id')
        question = data.get('question')
        
        if not session_id or not question:
            return jsonify({'success': False, 'error': 'Missing session_id or question'})
        
        if session_id not in query_engines:
            return jsonify({'success': False, 'error': 'Invalid session_id'})
        
        query_engine = query_engines[session_id]
        response = query_engine.query(question)
        response_text = str(response)
        
        result = {
            'success': True,
            'answer': response_text,
            'source': 'document'
        }
        
        # Check if answer was not found
        if is_answer_not_found(response_text):
            result['not_found'] = True
            result['can_search_web'] = True
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/search-web', methods=['POST'])
def search_web():
    try:
        data = request.json
        question = data.get('question')
        
        if not question:
            return jsonify({'success': False, 'error': 'Missing question'})
        
        # Try Google Search first
        google_result = search_web_with_google(question)
        
        if google_result == "quota_exceeded":
            # Fallback to Gemini
            gemini_result = answer_with_gemini(question)
            return jsonify({
                'success': True,
                'answer': gemini_result,
                'source': 'gemini_fallback',
                'message': 'Google Search quota exceeded. Used Gemini\'s general knowledge.'
            })
        elif google_result.startswith("search_error:"):
            # Fallback to Gemini
            gemini_result = answer_with_gemini(question)
            return jsonify({
                'success': True,
                'answer': gemini_result,
                'source': 'gemini_fallback',
                'message': 'Google search error. Used Gemini\'s general knowledge.'
            })
        else:
            return jsonify({
                'success': True,
                'answer': google_result,
                'source': 'google_search'
            })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/add-context', methods=['POST'])
def add_context():
    try:
        session_id = None
        
        if 'file' in request.files:
            session_id = request.form.get('session_id')
            if not session_id or session_id not in session_documents:
                return jsonify({'success': False, 'error': 'Invalid session_id'})
                
            file = request.files['file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, f"{session_id}_{filename}")
                file.save(filepath)
                
                # Determine file type
                file_ext = filename.rsplit('.', 1)[1].lower()
                input_type = 'pdf' if file_ext == 'pdf' else 'image'
                
                # Load new documents
                new_docs = load_from_type(input_type, filepath)
                
                # Generate preview of new content
                new_content_preview = generate_preview(new_docs, f"{input_type} file: {filename}")
                
                # Add to existing documents
                session_documents[session_id].extend(new_docs)
                
                # Rebuild query engine with all documents
                query_engine = build_query_engine(session_documents[session_id])
                summary = generate_summary(session_documents[session_id], 'mixed')
                
                # Update stored data
                query_engines[session_id] = query_engine
                document_summaries[session_id] = summary
                
                # Clean up uploaded file
                os.remove(filepath)
                
                return jsonify({
                    'success': True,
                    'summary': summary,
                    'added_content': {
                        'type': input_type,
                        'name': filename,
                        'preview': new_content_preview
                    }
                })
                
        elif request.json:
            data = request.json
            session_id = data.get('session_id')
            
            if not session_id or session_id not in session_documents:
                return jsonify({'success': False, 'error': 'Invalid session_id'})
            
            if 'url' in data:
                new_docs = load_from_type('url', data['url'])
                new_content_preview = generate_preview(new_docs, f"URL: {data['url']}")
                
                session_documents[session_id].extend(new_docs)
                
                query_engine = build_query_engine(session_documents[session_id])
                summary = generate_summary(session_documents[session_id], 'mixed')
                
                query_engines[session_id] = query_engine
                document_summaries[session_id] = summary
                
                return jsonify({
                    'success': True,
                    'summary': summary,
                    'added_content': {
                        'type': 'url',
                        'name': data['url'],
                        'preview': new_content_preview
                    }
                })
                
            elif 'text' in data:
                new_docs = load_from_type('text', data['text'])
                new_content_preview = generate_preview(new_docs, "Text content")
                
                session_documents[session_id].extend(new_docs)
                
                query_engine = build_query_engine(session_documents[session_id])
                summary = generate_summary(session_documents[session_id], 'mixed')
                
                query_engines[session_id] = query_engine
                document_summaries[session_id] = summary
                
                return jsonify({
                    'success': True,
                    'summary': summary,
                    'added_content': {
                        'type': 'text',
                        'name': 'Custom text',
                        'preview': new_content_preview
                    }
                })
        
        return jsonify({'success': False, 'error': 'No valid content provided'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sessions/<session_id>/summary')
def get_summary(session_id):
    if session_id in document_summaries:
        return jsonify({
            'success': True,
            'summary': document_summaries[session_id]
        })
    return jsonify({'success': False, 'error': 'Session not found'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)