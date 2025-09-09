# Simple dev runner (auto-reload enabled when FLASK_DEBUG=1 or app.config['DEBUG']=True)
from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
