from flask_app import create_app

app = create_app() #add config in brackets

if __name__ == "__main__":
    app.run(debug = False)
