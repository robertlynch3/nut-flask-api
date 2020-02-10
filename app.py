# Robert Lynch (C) 2019
#
#
#
#
#
nutserver_IP="127.0.0.1"
requireAPIkey=False
APIkey=""



# Import statements
from flask import Flask, request
from flask_restplus import Api, Resource, fields
from functools import wraps
from importlib import reload
import nut2


# JSON for API key
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}




app=Flask(__name__)

# if requireAPIkey is set to true, Swagger documentation will require add authorization
if requireAPIkey==True:
    api=Api(app, authorizations=authorizations, doc='/docs',version=1.0, title='NUT Server API', description='API tool to get information from a NUT server')
else:
    api=Api(app, doc='/docs',version=1.0, title='NUT Server API', description='API tool to get information from a NUT server')


# API Authentication function
def API_authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if requireAPIkey:
            token = None
            # checks to see if the token header is present in the header
            if 'X-API-KEY' in request.headers:
                token=request.headers["X-API-KEY"]
                if token!=APIkey:
                    return {"Error":"Not Authorized"}, 401
            # if the token is not present the user receives an error.
            if not token:
                return {"Error":"Token Missing"}, 401
        return f(*args, **kwargs)
    return decorated #Returns the arguments after confirming if the token is correct 

# API routes below:
#
#
#
# Get UPSes ...(side note, is it UPSes or UPSs....????) that are defined in the nut/ups.conf file
@api.route('/getups')
class GetUPS(Resource):
    @api.doc(security='apikey', responses={200:'Success', '401': 'Authentication Issue'})
    @api.param('host', 'IP address of host')
    @API_authentication #passes to the API_authentication function
    def get(self):
        reload(nut2)
        # If user passes a host, it will use the host that is passed, else it uses the defined host in nutserver_IP
        if request.args.get('host')!=None:
            client = nut2.PyNUTClient(request.args.get('host'))
        else:
            client = nut2.PyNUTClient(nutserver_IP)
        return client.list_ups(), 200


# Gets all values from UPS
@api.route('/values')
class GetUPSValues(Resource):
    @api.doc(security='apikey', responses={200:'Success', '401': 'Authentication Issue'})
    @api.param('host', 'IP address of host')
    @api.param('ups', 'UPS name')
    @API_authentication #passes to the API_authentication function
    def get(self):
        reload(nut2)
        # If user passes a host, it will use the host that is passed, else it uses the defined host in nutserver_IP
        if request.args.get('host')!=None:
            client = nut2.PyNUTClient(request.args.get('host'))
        else:
            client = nut2.PyNUTClient(nutserver_IP)
        if request.args.get('ups')!=None:
            return client.list_vars(request.args.get('ups')), 200
        else:
            return {'Error':'UPS not requested'}, 400


# Gets Specific variables from UPS
@api.route('/variables/<var>')
class GetUPSSpecificVariables(Resource):
    @api.doc(security='apikey', responses={200:'Success', '401': 'Authentication Issue'}, params={'var':'Variable name'})
    @api.param('host', 'IP address of host')
    @api.param('ups', 'UPS name')
   # @API_authentication #passes to the API_authentication function
    def get(self, var):
        reload(nut2)
        # If user passes a host, it will use the host that is passed, else it uses the defined host in nutserver_IP
        if request.args.get('host')!=None:
            client = nut2.PyNUTClient(request.args.get('host'))
        else:
            client = nut2.PyNUTClient(nutserver_IP)
        if request.args.get('ups')!=None:
            return client.get(request.args.get('ups'), var), 200
        else:
            return {'Error':'UPS not requested'}, 400

@api.route('/variablesdescription/<var>')
class GetUPSVariablesDescription(Resource):
    @api.doc(security='apikey', responses={200:'Success', '401': 'Authentication Issue'}, params={'var':'Variable name'})
    @api.param('host', 'IP address of host')
    @api.param('ups', 'UPS name')
    @API_authentication #passes to the API_authentication function
    def get(self, var):
        reload(nut2)
        # If user passes a host, it will use the host that is passed, else it uses the defined host in nutserver_IP
        if request.args.get('host')!=None:
            client = nut2.PyNUTClient(request.args.get('host'))
        else:
            client = nut2.PyNUTClient(nutserver_IP)
        if request.args.get('ups')!=None:
            return client.var_description(request.args.get('ups'), var), 200
        else:
            return {'Error':'UPS not requested'}, 400



if __name__=="__main__":
    app.run(debug=True)
