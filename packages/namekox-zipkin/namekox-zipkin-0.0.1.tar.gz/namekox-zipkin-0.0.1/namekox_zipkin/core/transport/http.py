#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


import urllib2


from py_zipkin.transport import SimpleHTTPTransport


class HTTPTransport(SimpleHTTPTransport):
    def __init__(self, protocol='http', req_host='127.0.0.1', req_port=9411):
        self.protocol = protocol
        self.req_host = req_host
        self.req_port = req_port
        super(HTTPTransport, self).__init__(req_host, req_port)

    def send(self, payload):
        path, content_type = self._get_path_content_type(payload)
        url = '{}://{}:{}{}'.format(self.protocol, self.req_host, self.req_port, path)
        req = urllib2.Request(url, payload, {'Content-Type': content_type})
        return urllib2.urlopen(req)
