from web_app import create_app

app = create_app()

# test
# test 2
# test 3
# without this line, it will run when imported, debug=true automatically reruns when edits are made, __name__ is special variable
if __name__ == '__main__':
    app.run(debug=True)
