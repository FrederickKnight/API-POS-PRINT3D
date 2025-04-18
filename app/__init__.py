from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .error_handler import register_error_handlers

from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

bcrypt = Bcrypt()
cors = CORS()

basedir = os.path.abspath(os.path.dirname(__file__))
if os.name == 'nt':  # Windows
    upload_folder = os.path.abspath(os.path.join(basedir, '.','static', 'uploads'))

app = Flask(__name__)

def create_app():
    
    if os.environ.get("DB_URL") is None:
        load_dotenv()

    register_error_handlers(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = upload_folder

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    
    from app.models import (
        BaseModel,
    )
    
    with app.app_context():
        db.create_all()

    define_routes(app)
    
    return app

def define_routes(app):
    # -------------------------------- Routes --------------------------------
    
    from app.routes import (
        AuthUserRoute,
        ClientRoute,
        MaterialTypeRoute,
        MaterialRoute,
        ThemeRoute,
        SubthemeRoute,
        MaterialInventoryRoute,
        InventoryRoute,
        PrintModelRoute,
        BrandModelRoute,
        SetModelRoute,
        GeneralPricesRoute,
        TicketRoute,
        SalesRoute,
        ErrorSaleRoute
    )
    
    #user & auth
    app.register_blueprint(AuthUserRoute().get_blueprint(),url_prefix="/api/auth/user/")

    # routes
    app.register_blueprint(ClientRoute().get_blueprint(),url_prefix="/api/client/")
    
    app.register_blueprint(MaterialTypeRoute().get_blueprint(),url_prefix="/api/material-type/")
    app.register_blueprint(MaterialRoute().get_blueprint(),url_prefix="/api/material/")

    app.register_blueprint(ThemeRoute().get_blueprint(),url_prefix="/api/theme/")
    app.register_blueprint(SubthemeRoute().get_blueprint(),url_prefix="/api/subtheme/")

    app.register_blueprint(MaterialInventoryRoute().get_blueprint(),url_prefix="/api/material-inventory/")
    app.register_blueprint(InventoryRoute().get_blueprint(),url_prefix="/api/inventory/")

    app.register_blueprint(PrintModelRoute().get_blueprint(),url_prefix="/api/print-model/")
    app.register_blueprint(BrandModelRoute().get_blueprint(),url_prefix="/api/brand-model/")
    app.register_blueprint(SetModelRoute().get_blueprint(),url_prefix="/api/set-model/")

    app.register_blueprint(GeneralPricesRoute().get_blueprint(),url_prefix="/api/general-price/")
    app.register_blueprint(TicketRoute().get_blueprint(),url_prefix="/api/ticket/")
    app.register_blueprint(SalesRoute().get_blueprint(),url_prefix="/api/sale/")
    app.register_blueprint(ErrorSaleRoute().get_blueprint(),url_prefix="/api/error-sale/")