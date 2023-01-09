# Import flask app that exits within __init__.py
from dashboardapp import create_app
app = create_app()
if __name__ == "__main__":
    app.run(debug=True)