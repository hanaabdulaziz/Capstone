#!/bin/bash

# Export Auth0 configurations
export AUTH0_DOMAIN='fsnd310.us.auth0.com'
export AUTH0_CLIENT_ID='ljvb8bRE7tOFHbKVADflsXaaQ62oVhH8'
export AUTH0_CLIENT_SECRET='_5pTntQeXAVg5PImS5KhxlX9c6N1lFdFjN784qmUDDl-3EhiIIn8jVQaPbRcuwqC'
export API_KEY='casting'

# Install dependencies
pip install Flask Flask-SQLAlchemy Flask-Cors Flask-HTTPAuth requests

# Initialize the database
python -c "from app import create_app; app = create_app(); with app.app_context(): app.create_all()"

echo "Setup complete"
