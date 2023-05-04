from web_app import create_app

app = create_app()

# Note: Ensures app only runs when this module is called. Debug=True automatically reruns when saved.
if __name__ == "__main__":
    app.run(debug=True)
