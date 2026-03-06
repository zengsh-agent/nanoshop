"""
NanoShop - AI-Powered Image Editor
Run this file to start both the backend and frontend servers.
"""
import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")

    # Backend dependencies
    print("\nInstalling backend dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])

    # Frontend dependencies
    print("\nInstalling frontend dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "frontend/requirements.txt"])

    print("\nDependencies installed successfully!")

def start_backend():
    """Start the FastAPI backend server."""
    print("\nStarting backend server on http://localhost:8000")
    os.chdir("backend")
    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

def start_frontend():
    """Start the Flask frontend server."""
    print("\nStarting frontend server on http://localhost:5000")
    os.chdir("frontend")
    subprocess.run([sys.executable, "app.py"])

def main():
    """Main entry point."""
    print("=" * 50)
    print("  NanoShop - AI Image Editor")
    print("=" * 50)

    # Check if ANTHROPIC_API_KEY is set
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\nWARNING: ANTHROPIC_API_KEY environment variable not set.")
        print("Please set it before running the app:")
        print("  export ANTHROPIC_API_KEY=your_api_key")
        print("\nYou can get an API key from: https://console.anthropic.com/")
        print("\nContinuing without AI features...")

    # Ask user what to do
    print("\nOptions:")
    print("1. Install dependencies only")
    print("2. Start backend only")
    print("3. Start frontend only")
    print("4. Start both (development)")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == "1":
        install_dependencies()
    elif choice == "2":
        start_backend()
    elif choice == "3":
        start_frontend()
    elif choice == "4":
        # For development, we typically run backend in one terminal
        # and frontend in another
        print("\nFor development, please run these in separate terminals:")
        print("  Terminal 1: cd backend && python main.py")
        print("  Terminal 2: cd frontend && python app.py")
        print("\nThen open http://localhost:5000 in your browser")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
