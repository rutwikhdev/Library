from flask import Flask
from flask_cors import CORS
from app.books_view import books_view
from app.members_view import members_view
from app.rentals_view import rentals_view
from app.transact_view import transact_view
from app.reports_view import reports_view
import config


app = Flask(__name__)
app.config['SECRET_KEY'] = config.Config.SECRET_KEY
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

app.register_blueprint(books_view)
app.register_blueprint(members_view)
app.register_blueprint(rentals_view)
app.register_blueprint(transact_view)
app.register_blueprint(reports_view)

if __name__ == '__main__':
    app.run(debug=config.Config.DEBUG, host=config.Config.SERVER)
