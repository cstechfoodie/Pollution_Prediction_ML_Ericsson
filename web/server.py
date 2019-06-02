from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import re

weights_file_directory = "weights.txt"
dict_for_cbwd = {'NW':1, "NE":2, "SE":3, "cv":4}

def hello_world(request):
    return Response('Hello World!')

def convert_to_float_otherwise_none_or_string(input):
    try:
        if input is not None:
            return float(input)
        else: 
            return 0.0
    except ValueError:
        if input is None:
            return 0.0
        if len(input) == 0:
            return None
        else:
            return str(input)

def predict_pm(request):
    inputs = "2656.0,2014.0,1.0,3.0,13.0,29.0,-17.0,9.0,1022.0,NW,22.35,0.0,0.0"
    inputs = re.split(",", inputs)
    for i in range(5,len(inputs)):
        inputs[i] = convert_to_float_otherwise_none_or_string(inputs[i])

    f = open(weights_file_directory, "r", encoding="iso8859_2")
    line = f.readline()
    weights = re.split(',', line)
    for i in range(len(weights)):
        weights[i] = convert_to_float_otherwise_none_or_string(weights[i])
    f.close()

    record_anchor = 6
    predicted_pm = float(weights[record_anchor]) * float(inputs[record_anchor]) + \
            float(weights[record_anchor + 1]) * float(inputs[record_anchor + 1]) + \
            float(weights[record_anchor + 2]) * float(inputs[record_anchor + 2]-1000) + \
            float(weights[record_anchor + 3]) * float(dict_for_cbwd.get(inputs[record_anchor + 3])) + \
            float(weights[record_anchor + 4]) * float(inputs[record_anchor + 4]) + \
            float(weights[record_anchor + 5]) * float(inputs[record_anchor + 5]) + \
            float(weights[record_anchor + 6]) * float(inputs[record_anchor + 6])
    return Response(str(predicted_pm))

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/hello')
        config.add_route('predict', '/predict')
        config.add_view(hello_world, route_name='hello')
        config.add_view(predict_pm, route_name='predict')
        app = config.make_wsgi_app()
    server = make_server('localhost', 9090, app)
    server.serve_forever()