# main.py
from website import create_app
import os # Import os module

# Load environment variables from .env file if in development
# In production, these should be set directly in the hosting environment
# For local development, install python-dotenv: pip install python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass # dotenv not installed or not in dev environment

app = create_app()

# Set SECRET_KEY from environment variable
app.config['SECRET_KEY'] = os.environ.get('aliali110', 'aliali110')
# IMPORTANT: 'your_default_secret_key_for_dev' should only be used for local development.
# For production, ensure the SECRET_KEY environment variable is set.
# You can generate a strong key with: os.urandom(24).hex()

if __name__ == '__main__':
    # When debug=True, Flask automatically reloads on code changes
    # For production, debug should be False.
    app.run(debug=True)