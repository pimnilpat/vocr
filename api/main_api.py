from datetime import datetime, timedelta
from flask import Request, Response, url_for, json, request

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


        @app.route("/api", methods=["GET"])
        def index():  
        
            res_message = """Welcome to VOCR API \nYou are running on {0} \nSession time is {1}"""

            res_message = res_message.format(app.config["ENV"], app.config["PERMANENT_SESSION_LIFETIME"])
                

            resp = Response(res_message)
            resp.mimetype = "text/plain"
            resp.status_code = 200

            return resp


       