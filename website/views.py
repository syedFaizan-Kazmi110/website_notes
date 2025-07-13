from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json # Make sure json is imported

from . import db
from .models import Note # Make sure Note model is imported

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_content = request.form.get('note') # Renamed 'note' to 'note_content' for clarity
        
        if len(note_content) < 1:
            flash('Note cannot be empty!', category='error')
        else:
            new_note = Note(data=note_content, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully!', category='success')
            # Implement Post/Redirect/Get pattern to prevent re-submission on refresh
            return redirect(url_for('views.home')) 
        
    # For GET requests or failed POSTs (e.g., empty note), render the template
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
@login_required # Ensures user is logged in to delete notes
def delete_note():
    try:
        # Safely parse the JSON data from the request body
        note_data = json.loads(request.data)
        # Use .get() to retrieve 'noteId'. This prevents KeyError if the key is missing.
        note_id = note_data.get('noteId') 
    except json.JSONDecodeError:
        # Handle cases where the incoming data is not valid JSON
        # No flash here, as this is an AJAX endpoint
        return jsonify({'error': 'Invalid JSON data', 'message': 'Invalid request data provided for note deletion.'}), 400

    # Ensure note_id was provided and is an integer
    if not isinstance(note_id, int): # Check if note_id is an integer
        # No flash here
        return jsonify({'error': 'Invalid Note ID', 'message': 'Invalid Note ID provided for deletion.'}), 400

    # Query the database for the note using the ID
    note = Note.query.get(note_id)
    
    if note: # Check if the note exists in the database
        # Verify that the current logged-in user owns this note
        if note.user_id == current_user.id:
            db.session.delete(note) # Delete the note from the session
            db.session.commit()    # Commit the changes to the database
            # Return success message in JSON
            return jsonify({'success': True, 'message': 'Note deleted successfully!'}) 
        else:
            # User is trying to delete someone else's note
            # No flash here
            return jsonify({'error': 'Unauthorized access', 'message': 'You do not have permission to delete this note.'}), 403 # 403 Forbidden
    else:
        # Note with the given ID was not found
        # No flash here
        return jsonify({'error': 'Note not found', 'message': 'Note not found for deletion.'}), 404 # 404 Not Found