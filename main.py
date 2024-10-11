from flask import Flask
from jinja2.utils import F
from routes.log_eqto import log_eqto_route
from routes.Cad_Eqto import Cad_Eqto_route
from routes.Ctr_Eqto import Ctr_Eqto_route
from routes.Carr_Img import Carr_Img_route
import os

 
app = Flask(__name__)

UPLOAD_FOLDER_CERT = '/static/certificados'

app.config['UPLOAD_FOLDER_CERT'] = UPLOAD_FOLDER_CERT

app.register_blueprint(log_eqto_route, url_prefix="/")
app.register_blueprint(Cad_Eqto_route, url_prefix="/Cad_Eqto")
app.register_blueprint(Ctr_Eqto_route, url_prefix="/Ctr_Eqto")
app.register_blueprint(Carr_Img_route, url_prefix="/Carr_Img")


if __name__ == "__main__":
    app.run(debug=True)
 
    