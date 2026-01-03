# main.py

from app.client import app

# import handlers (this registers them)
import handlers.start  # noqa

if __name__ == "__main__":
    print("🚀 Kasukabe Hosting Bot started")
    app.run()