#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


import socket


from logging import getLogger
from py_zipkin.zipkin import zipkin_span, ZipkinAttrs, Encoding
from namekox_zipkin.constants import ZIPKIN_CONFIG_KEY
from namekox_core.core.service.dependency import Dependency
from namekox_zipkin.core.transport.http import HTTPTransport
from namekox_core.core.friendly import AsLazyProperty, ignore_exception


logger = getLogger(__name__)


class ZipkinHelper(Dependency):
    def __init__(self, transport_handler=None, transport_options=None, **options):
        self.zptrace = None
        self.options = options
        self.transport_options = transport_options or {}
        self.transport_handler = transport_handler or HTTPTransport
        super(ZipkinHelper, self).__init__(transport_handler, transport_options, **options)

    @staticmethod
    def get_host_byname():
        name = socket.gethostname()
        return ignore_exception(socket.gethostbyname)(name)

    @staticmethod
    def gen_zipkin_attr(context):
        return ZipkinAttrs(trace_id=context.data['origin_id'],
                           flags='0', is_sampled=True,
                           span_id=context.data['call_id'],
                           parent_span_id=context.data['parent_call_id'])

    @AsLazyProperty
    def config(self):
        config = self.container.config.get(ZIPKIN_CONFIG_KEY, {})
        # host
        host = self.get_host_byname()
        config['host'] = host or '127.0.0.1'
        # transport_options
        transport_options = config.pop('transport_options', {})
        transport_options.update(self.transport_options)
        self.transport_options = transport_options
        return config

    def worker_setup(self, context):
        config = self.config.copy()
        config.update(self.options)
        transport_handler = self.transport_handler(**self.transport_options)
        self.zptrace = zipkin_span(service_name=context.service.name,
                                   zipkin_attrs=self.gen_zipkin_attr(context),
                                   span_name=context.entrypoint.obj_name,
                                   transport_handler=transport_handler,
                                   encoding=Encoding.V2_JSON, **config)
        self.zptrace.start()

    def worker_result(self, context, result=None, exc_info=None):
        self.zptrace.stop(*(exc_info or (None, None, None)))

    def get_instance(self, context):
        return self.zptrace
