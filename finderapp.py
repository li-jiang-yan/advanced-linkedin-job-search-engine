from waitress import serve

from finderapp import create_app

if __name__ == "__main__":
    print(" * Running on http://127.0.0.1:5000")
    print("Press CTRL+C to quit")
    myapp = create_app()
    serve(myapp, host="127.0.0.1", port=5000)
