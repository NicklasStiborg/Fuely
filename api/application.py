from flask import Flask
from flask_restful import Resource, Api
import database
from flask_cors import CORS
from apscheduler.scheduler import Scheduler 

conn = database.connect()

application = app = Flask(__name__)
api = Api(application)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

class apiClass(Resource):
    def get(self):
        return {database.newestPrice(conn)[0][2]:{'time':database.newestPrice(conn)[0][1],'price_95':database.newestPrice(conn)[0][3], 'price_D': database.newestPrice(conn)[0][4]},
                database.newestPrice(conn)[1][2]:{'time':database.newestPrice(conn)[1][1],'price_95':database.newestPrice(conn)[1][3], 'price_D': database.newestPrice(conn)[1][4]},
                database.newestPrice(conn)[2][2]:{'time':database.newestPrice(conn)[2][1],'price_95':database.newestPrice(conn)[2][3], 'price_D': database.newestPrice(conn)[2][4]},
                database.newestPrice(conn)[3][2]:{'time':database.newestPrice(conn)[3][1],'price_95':database.newestPrice(conn)[3][3], 'price_D': database.newestPrice(conn)[3][4]},
                database.newestPrice(conn)[4][2]:{'time':database.newestPrice(conn)[4][1],'price_95':database.newestPrice(conn)[4][3], 'price_D': database.newestPrice(conn)[4][4]},
                database.newestPrice(conn)[5][2]:{'time':database.newestPrice(conn)[5][1],'price_95':database.newestPrice(conn)[5][3], 'price_D': database.newestPrice(conn)[5][4]},
        }

    
api.add_resource(apiClass, '/')

if __name__ == '__main__':
    application.run()


