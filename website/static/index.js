// website/static/index.js

/**
 * Dynamically displays a Bootstrap-style alert message on the page.
 * @param {string} message The message to display.
 * @param {string} type The type of alert (e.g., 'success', 'error', 'info').
 */
function displayMessage(message, type) {
    const container = document.querySelector('.container.mt-5.pt-4'); // Target the existing flash message container
    if (!container) {
        console.warn('Flash message container not found. Cannot display message.');
        // Fallback to a simple alert if the container isn't found
        alert(message);
        return;
    }

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show animate__animated animate__fadeInDown`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    container.prepend(alertDiv); // Add the new alert to the top of the container

    // Optional: Automatically dismiss the alert after a few seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv); // Initialize Bootstrap Alert
        bsAlert.close();
    }, 5000); // Dismiss after 5 seconds
}


function deleteNote(noteId) {
    // --- Start: Robust ID and Element Check ---
    console.log('deleteNote function called with noteId:', noteId);

    if (typeof noteId !== 'number' || isNaN(noteId)) {
        console.error('Invalid noteId received:', noteId, 'Expected a number.');
        displayMessage('Cannot delete: Invalid note ID. Please refresh and try again.', 'error');
        return; 
    }

    const noteElementId = `note-${noteId}`;
    const noteElement = document.getElementById(noteElementId);
    
    console.log('Attempting to find note element with ID:', noteElementId, 'Result:', noteElement);

    if (!noteElement) {
        console.warn('Note element not found in the DOM for ID:', noteElementId);
        displayMessage('Could not find the note to delete in the display. It might already be gone, or there is a display issue.', 'error');
        return; 
    }
    // --- End: Robust ID and Element Check ---

    // --- Start: Re-enable Animation ---
    // Add a class to trigger the CSS fade-out and collapse animation
    noteElement.classList.add('note-deleting'); 

    // Listen for the 'transitionend' event, which fires when the CSS animation is complete.
    // The '{ once: true }' option ensures this listener is removed after it runs once.
    noteElement.addEventListener('transitionend', function handler() {
        // Remove the event listener to prevent it from firing multiple times
        noteElement.removeEventListener('transitionend', handler); 

        // Send the DELETE request to the Flask backend AFTER the animation completes
        fetch('/delete-note', {
            method: 'POST',
            body: JSON.stringify({ noteId: noteId }), 
            headers: {
                'Content-Type': 'application/json' 
            }
        })
        .then(response => response.json()) // Parse the JSON response
        .then(data => {
            if (data.success) {
                noteElement.remove(); // Remove the element from the DOM after successful deletion
                displayMessage(data.message, 'success'); // Display success message
            } else {
                console.error('Error deleting note:', data.error || 'Unknown error');
                displayMessage(data.message || 'Failed to delete note. Unknown error.', 'error'); // Display error message
                noteElement.classList.remove('note-deleting'); // Revert animation if deletion fails
            }
        })
        .catch(error => {
            console.error('Network or unexpected error during note deletion:', error);
            displayMessage('An unexpected error occurred during deletion. Please try again.', 'error'); // Display network error message
            noteElement.classList.remove('note-deleting'); // Revert animation if fetch fails
        });
    }, { once: true }); 
    // --- End: Re-enable Animation ---
}
