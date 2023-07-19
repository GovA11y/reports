# run.py

import os
from app import create_app, startup

app = create_app()

startup()

if __name__ == '__main__':
    # Use the APP_PORT environment variable
    port = os.environ.get('APP_PORT', 8080)
    app.run(host='0.0.0.0', port=port, debug=True)
