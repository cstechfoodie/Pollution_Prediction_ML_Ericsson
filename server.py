from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import re

weights_file_directory = "weights.txt"
dict_for_cbwd = {'NW': 1, "NE": 2, "SE": 3, "cv": 4}


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
    print(request.method)
    if str(request.method) == 'POST':
        print(request.body.decode('ascii'))
        inputs = request.body.decode('ascii')
    # Sample output
    # 127.0.0.1 - - [02/Jun/2019 00:37:37] "GET /predict HTTP/1.1" 200 17
    # GET
    # 127.0.0.1 - - [02/Jun/2019 00:43:11] "GET /predict HTTP/1.1" 200 17
    # POST
    # 2848.0,2010.0,1.0,15.0,19.0,91.0,-15.0,-6.0,1037.0,cv,1.78,0.0,0.0

    inputs = re.split(",", inputs)
    for i in range(5, len(inputs)):
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
    
    response = Response(str(predicted_pm))
    response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '1728000',
        })
    # return Response(str(predicted_pm))
    return response

if __name__ == '__main__':
    #创建了一个Configuration类的实例config
    with Configurator() as config:
        
        #注册了一个以/hello/开头的URL路由,路由的名字就叫'hello'
        config.add_route('hello', '/hello')
        config.add_route('predict', '/predict')
        
        #注册了一个view callable函数  URL Path（比如/hello/world）->route(比如'hello')->view callable(比如hello_world函数); 当名为'hello'的路由被匹配时应该调用这个函数
        config.add_view(hello_world, route_name='hello')
        config.add_view(predict_pm, route_name='predict')
        
        #pyramid.config.Configurator.make_wsgi_app()方法来创建WSGI应用程序
        app = config.make_wsgi_app()
    
    #启动了一个WSGI服务
    server = make_server('localhost', 9090, app)
    #serve_forever()方法创建了一个循环来接受外界的request请求
    server.serve_forever()

# -----------------------------------------------------------------------
# https://www.jianshu.com/p/c5096adf5a22

# WSGI - Web Server Gateway Interface. This is a Python standard for connecting web applications to web servers, similar to the concept of Java Servlets. Pyramid requires that your application be served as a WSGI application.

# Imports 包
    # 第2行引入了pyramid.config模块的Configurator类，第59行创建了它的一个实例，然后通过这个实例来配置我们的应用。
    # 跟其他Python web框架一样，Pyramid 用 WSGI 协议来将一个应用程序和web服务器联系到一起。而第一行用到的wsgiref模块就是WSGI服务的一种封装，现在wsgiref已经被引入Python 标准库了。
    # 第三行引入了pyramid.response.Response,用来返回response信息。
