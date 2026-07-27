from app import create_app

if __name__ == "__main__":
    print("Starting Flask app... this might take a while")
    myapp = create_app()
    myapp.run()
