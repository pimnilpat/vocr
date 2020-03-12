from datetime import datetime, timedelta
from flask import Request, Response, url_for, json, request
from werkzeug.utils import secure_filename
import os
from flask import render_template


class main_api():
    def __init__(self, app): 
        
        #Define API Route

        '''
        Error handler methed
        404 , not found
        '''
        @app.errorhandler(404)
        def not_found(error=None):
            message = {
                "message" : "Not found : " + request.url
            }

            resp = Response(json.dumps(message, default=str))
            resp.mimetype = "application/json"
            resp.default_status = 404

            return resp


        @app.route("/api/0.0.1", methods=["GET"])
        def index():  
        
            res_message = """Welcome to VOCR API \nYou are running on {0} \nSession time is {1} \nUpload folder is {2}"""

            res_message = res_message.format(app.config["ENV"], app.config["PERMANENT_SESSION_LIFETIME"], app.config["UPLOAD_FOLDER"])
                

            resp = Response(res_message)
            resp.mimetype = "text/plain"
            resp.status_code = 200

            return resp

        @app.route("/views/images", methods=["GET"])
        def display_images():
            lists = os.listdir(app.config["UPLOAD_FOLDER"])            
            return render_template("display-image.html", url=lists)

        @app.route("/api/0.0.1/bucard/read", methods=["POST"])        
        def extract_image():
            #check if request has the  file part
            if "file" not in request.files:
                message = {
                    "message": "No file part in the request",
                    "description": request.files
                }
                resp = Response(json.dumps(message, default=str))
                resp.mimetype = "application/json"
                resp.status_code = 400
                return resp

            
            file = request.files["file"]

            #if filename is empty
            if file.filename == "":
                message = {
                    "message": "No file selected for uploading"
                }
                resp = Response(json.dumps(message, default=str))
                resp.mimetype = "application/json"
                resp.status_code = 400
                return resp

            #save file if validation passes
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))  #save file

                message = {
                    "message": "File successfully uploaded",
                    "url": render_template("base.html")
                }

                resp = Response(json.dumps(message, default=str))
                resp.mimetype = "application/json"
                resp.status_code = 201
                return resp               

            else: 
                message = {
                    "message": "Allow file types are ".join(app.config["ALLOWED_EXTENSIONS"])
                }
                
                resp = Response(json.dumps(message, default=str))
                resp.mimetype = "application/json"
                resp.status_code = 400
                return resp

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
            

        
