from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import re
import model_training.pp as p


def hello_world(request):
    return Response('Hello World!')


def predict_pm(request):
    inputs = "2656.0,2014.0,1.0,3.0,13.0,29.0,-17.0,9.0,1022.0,NW,22.35,0.0,0.0"
    if str(request.method) == 'POST':
        print(request.body.decode('ascii'))
        inputs = request.body.decode('ascii')
    predicted_pm = p.predict(inputs)
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
