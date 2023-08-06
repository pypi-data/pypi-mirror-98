# Install
```shell script
pip install -U namekox-zipkin
```

# Example
> gateway.py
```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_webserver.core.entrypoints.app import app
from namekox_zookeeper_jsonrpc.core.proxy import Proxy
from namekox_zookeeper_jsonrpc.core.mixin import Registry
from namekox_jsonrpc.constants import DEFAULT_JSONRPC_PORT
from namekox_zipkin.core.dependencies import ZipkinHelper


# 网关服务
SERVICE_NAME = 'gateway'
SERVICE_PORT = DEFAULT_JSONRPC_PORT


class Gateway(Registry(name=SERVICE_NAME, roptions={'port': SERVICE_PORT})):
    name = SERVICE_NAME

    zipkin = ZipkinHelper(port=SERVICE_PORT)

    @app.api('/api/user/token/', methods=['GET'])
    def get_user_token(self, request):
        return Proxy(self).admin.gen_user_token()
```
> admin.py
```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_jsonrpc.core.entrypoints import jsonrpc
from namekox_zookeeper_jsonrpc.core.proxy import Proxy
from namekox_zookeeper_jsonrpc.core.mixin import Registry
from namekox_jsonrpc.constants import DEFAULT_JSONRPC_PORT
from namekox_zipkin.core.dependencies import ZipkinHelper


# 平台服务
SERVICE_NAME = 'admin'
SERVICE_PORT = DEFAULT_JSONRPC_PORT


class Admin(Registry(name=SERVICE_NAME, roptions={'port': SERVICE_PORT})):
    name = SERVICE_NAME

    zipkin = ZipkinHelper(port=SERVICE_PORT)

    @jsonrpc.rpc()
    def gen_user_token(self):
        return Proxy(self).user.auth()
```
> user.py
```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_jsonrpc.core.entrypoints import jsonrpc
from namekox_zookeeper_jsonrpc.core.proxy import Proxy
from namekox_zookeeper_jsonrpc.core.mixin import Registry
from namekox_jsonrpc.constants import DEFAULT_JSONRPC_PORT
from namekox_zipkin.core.dependencies import ZipkinHelper


# 用户服务
SERVICE_NAME = 'user'
SERVICE_PORT = DEFAULT_JSONRPC_PORT


class User(Registry(name=SERVICE_NAME, roptions={'port': SERVICE_PORT})):
    name = SERVICE_NAME

    zipkin = ZipkinHelper(port=SERVICE_PORT)

    @jsonrpc.rpc()
    def auth(self):
        return Proxy(self).ad.authenticate()
```
> ad.py
```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_jsonrpc.core.entrypoints import jsonrpc
from namekox_zookeeper_jsonrpc.core.mixin import Registry
from namekox_jsonrpc.constants import DEFAULT_JSONRPC_PORT
from namekox_zipkin.core.dependencies import ZipkinHelper


# 用户服务
SERVICE_NAME = 'ad'
SERVICE_PORT = DEFAULT_JSONRPC_PORT


class Ad(Registry(name=SERVICE_NAME, roptions={'port': SERVICE_PORT})):
    name = SERVICE_NAME

    zipkin = ZipkinHelper(port=SERVICE_PORT)

    @jsonrpc.rpc()
    def authenticate(self):
        return 'succ'
```

# Running
> config.yaml
```yaml
SERVICE:
  trace_id_func: namekox_zipkin.core.generator:generate_random_64bit_string
ZIPKIN:
  sample_rate: 100.0
  transport_options:
    protocol: http
    req_host: 127.0.0.1
    req_port: 9411
ZOOKEEPER:
  ping:
    hosts: 127.0.0.1:2181
WEBSERVER:
  host: 0.0.0.0
  port: 80
```
> namekox run gateway
```shell script
2021-03-17 21:29:59,138 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2021-03-17 21:30:03,156 DEBUG starting services [u'gateway']
2021-03-17 21:30:03,157 DEBUG starting service gateway entrypoints [gateway:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:get_user_token, gateway:namekox_webserver.core.entrypoints.app.server.WebServer:server]
2021-03-17 21:30:03,159 DEBUG spawn manage thread handle gateway:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2021-03-17 21:30:03,161 DEBUG service gateway entrypoints [gateway:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:get_user_token, gateway:namekox_webserver.core.entrypoints.app.server.WebServer:server] started
2021-03-17 21:30:03,161 DEBUG starting service gateway dependencies [gateway:namekox_context.core.dependencies.ContextHelper:ctx, gateway:namekox_zookeeper.core.dependencies.ZooKeeperHelper:zk, gateway:namekox_config.core.dependencies.ConfigHelper:cfg, gateway:namekox_zipkin.core.dependencies.ZipkinHelper:zipkin]
2021-03-17 21:30:03,163 INFO Connecting to 127.0.0.1:2181
2021-03-17 21:30:03,164 DEBUG Sending request(xid=None): Connect(protocol_version=0, last_zxid_seen=0, time_out=30000, session_id=0, passwd='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', read_only=None)
2021-03-17 21:30:03,182 INFO Zookeeper connection established, state: CONNECTED
2021-03-17 21:30:07,210 DEBUG Sending request(xid=1): GetChildren(path=u'/namekox', watcher=<bound method ChildrenWatch._watcher of <kazoo.recipe.watchers.ChildrenWatch object at 0x109085490>>)
2021-03-17 21:30:07,211 DEBUG Sending request(xid=2): Create(path=u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', data='{"port": 63687, "address": "192.168.43.170"}', acl=[ACL(perms=31, acl_list=['ALL'], id=Id(scheme='world', id='anyone'))], flags=1)
2021-03-17 21:30:07,211 DEBUG Sending request(xid=3): GetChildren(path=u'/namekox', watcher=None)
2021-03-17 21:30:07,216 DEBUG service gateway dependencies [gateway:namekox_context.core.dependencies.ContextHelper:ctx, gateway:namekox_zookeeper.core.dependencies.ZooKeeperHelper:zk, gateway:namekox_config.core.dependencies.ConfigHelper:cfg, gateway:namekox_zipkin.core.dependencies.ZipkinHelper:zipkin] started
2021-03-17 21:30:07,216 DEBUG Sending request(xid=4): Create(path=u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', data='{"port": 63687, "address": "192.168.43.170"}', acl=[ACL(perms=31, acl_list=['ALL'], id=Id(scheme='world', id='anyone'))], flags=1)
2021-03-17 21:30:07,217 DEBUG services [u'gateway'] started
2021-03-17 21:30:07,222 DEBUG Received response(xid=1): [u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:30:07,223 DEBUG Sending request(xid=5): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:30:07,225 DEBUG Received EVENT: Watch(type=4, state=3, path=u'/namekox')
2021-03-17 21:30:07,232 DEBUG Received response(xid=2): u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41'
2021-03-17 21:30:07,233 DEBUG Received response(xid=3): [u'gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:30:07,234 DEBUG Received error(xid=4) NodeExistsError()
2021-03-17 21:30:07,236 DEBUG Received response(xid=5): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:30:07,239 DEBUG Sending request(xid=6): GetData(path=u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', watcher=None)
2021-03-17 21:30:07,239 DEBUG Sending request(xid=7): GetChildren(path=u'/namekox', watcher=<bound method ChildrenWatch._watcher of <kazoo.recipe.watchers.ChildrenWatch object at 0x109085490>>)
2021-03-17 21:30:07,243 DEBUG Received response(xid=6): ('{"port": 63687, "address": "192.168.43.170"}', ZnodeStat(czxid=6126, mzxid=6126, ctime=1615987807221, mtime=1615987807221, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418959, dataLength=44, numChildren=0, pzxid=6126))
2021-03-17 21:30:07,244 DEBUG Sending request(xid=8): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:30:07,246 DEBUG Received response(xid=7): [u'gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:30:07,249 DEBUG Received response(xid=8): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:30:07,266 DEBUG Sending request(xid=9): GetData(path=u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', watcher=None)
2021-03-17 21:30:07,268 DEBUG Received response(xid=9): ('{"port": 63687, "address": "192.168.43.170"}', ZnodeStat(czxid=6126, mzxid=6126, ctime=1615987807221, mtime=1615987807221, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418959, dataLength=44, numChildren=0, pzxid=6126))
2021-03-17 21:30:07,268 DEBUG Sending request(xid=10): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:30:07,270 DEBUG Received response(xid=10): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:30:44,948 DEBUG Received EVENT: Watch(type=4, state=3, path=u'/namekox')
2021-03-17 21:30:44,954 DEBUG Sending request(xid=11): GetChildren(path=u'/namekox', watcher=<bound method ChildrenWatch._watcher of <kazoo.recipe.watchers.ChildrenWatch object at 0x109085490>>)
2021-03-17 21:30:44,959 DEBUG Received response(xid=11): [u'gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', u'admin.5197989e-5e14-4974-bf40-2e1d955f615d', u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:30:44,964 DEBUG Sending request(xid=12): GetData(path=u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', watcher=None)
2021-03-17 21:30:44,969 DEBUG Received response(xid=12): ('{"port": 63687, "address": "192.168.43.170"}', ZnodeStat(czxid=6126, mzxid=6126, ctime=1615987807221, mtime=1615987807221, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418959, dataLength=44, numChildren=0, pzxid=6126))
2021-03-17 21:30:44,970 DEBUG Sending request(xid=13): GetData(path=u'/namekox/admin.5197989e-5e14-4974-bf40-2e1d955f615d', watcher=None)
2021-03-17 21:30:44,978 DEBUG Received response(xid=13): ('{"port": 64439, "address": "192.168.43.170"}', ZnodeStat(czxid=6129, mzxid=6129, ctime=1615987844942, mtime=1615987844942, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418960, dataLength=44, numChildren=0, pzxid=6129))
2021-03-17 21:30:44,980 DEBUG Sending request(xid=14): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:30:44,985 DEBUG Received response(xid=14): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:31:18,630 DEBUG Received EVENT: Watch(type=4, state=3, path=u'/namekox')
2021-03-17 21:31:18,632 DEBUG Sending request(xid=15): GetChildren(path=u'/namekox', watcher=<bound method ChildrenWatch._watcher of <kazoo.recipe.watchers.ChildrenWatch object at 0x109085490>>)
2021-03-17 21:31:18,641 DEBUG Received response(xid=15): [u'gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', u'admin.5197989e-5e14-4974-bf40-2e1d955f615d', u'user.5e94f263-58fe-4059-bea1-daf5fb1956b9', u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:31:18,643 DEBUG Sending request(xid=16): GetData(path=u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', watcher=None)
2021-03-17 21:31:18,649 DEBUG Received response(xid=16): ('{"port": 63687, "address": "192.168.43.170"}', ZnodeStat(czxid=6126, mzxid=6126, ctime=1615987807221, mtime=1615987807221, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418959, dataLength=44, numChildren=0, pzxid=6126))
2021-03-17 21:31:18,650 DEBUG Sending request(xid=17): GetData(path=u'/namekox/admin.5197989e-5e14-4974-bf40-2e1d955f615d', watcher=None)
2021-03-17 21:31:18,654 DEBUG Received response(xid=17): ('{"port": 64439, "address": "192.168.43.170"}', ZnodeStat(czxid=6129, mzxid=6129, ctime=1615987844942, mtime=1615987844942, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418960, dataLength=44, numChildren=0, pzxid=6129))
2021-03-17 21:31:18,657 DEBUG Sending request(xid=18): GetData(path=u'/namekox/user.5e94f263-58fe-4059-bea1-daf5fb1956b9', watcher=None)
2021-03-17 21:31:18,664 DEBUG Received response(xid=18): ('{"port": 65125, "address": "192.168.43.170"}', ZnodeStat(czxid=6132, mzxid=6132, ctime=1615987878624, mtime=1615987878624, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418961, dataLength=44, numChildren=0, pzxid=6132))
2021-03-17 21:31:18,677 DEBUG Sending request(xid=19): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:31:18,681 DEBUG Received response(xid=19): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:31:27,971 DEBUG spawn manage thread handle gateway:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x109062e50>, ('127.0.0.1', 65475)), kwargs={}, tid=handle_request)
2021-03-17 21:31:27,981 DEBUG spawn worker thread handle gateway:get_user_token(args=(<Request 'http://127.0.0.1/api/user/token/' [GET]>,), kwargs={}, context={})
2021-03-17 21:31:27,985 DEBUG post http://192.168.43.170:64439/gen_user_token with args=(), kwargs={u'__call_mode__': 0}
127.0.0.1 - - [17/Mar/2021 21:31:28] "GET /api/user/token/ HTTP/1.1" 200 218 0.101059
```
> namekox run admin
```shell script
2021-03-17 21:30:36,865 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2021-03-17 21:30:40,884 DEBUG starting services [u'admin']
2021-03-17 21:30:40,885 DEBUG starting service admin entrypoints [admin:namekox_jsonrpc.core.entrypoints.rpc.handler.JSONRpcHandler:gen_user_token, admin:namekox_jsonrpc.core.entrypoints.rpc.server.JSONRpcServer:server]
2021-03-17 21:30:40,888 DEBUG spawn manage thread handle admin:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2021-03-17 21:30:40,889 DEBUG service admin entrypoints [admin:namekox_jsonrpc.core.entrypoints.rpc.handler.JSONRpcHandler:gen_user_token, admin:namekox_jsonrpc.core.entrypoints.rpc.server.JSONRpcServer:server] started
2021-03-17 21:30:40,889 DEBUG starting service admin dependencies [admin:namekox_context.core.dependencies.ContextHelper:ctx, admin:namekox_zookeeper.core.dependencies.ZooKeeperHelper:zk, admin:namekox_config.core.dependencies.ConfigHelper:cfg, admin:namekox_zipkin.core.dependencies.ZipkinHelper:zipkin]
2021-03-17 21:30:40,892 INFO Connecting to 127.0.0.1:2181
2021-03-17 21:30:40,892 DEBUG Sending request(xid=None): Connect(protocol_version=0, last_zxid_seen=0, time_out=30000, session_id=0, passwd='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', read_only=None)
2021-03-17 21:30:40,916 INFO Zookeeper connection established, state: CONNECTED
2021-03-17 21:30:44,938 DEBUG Sending request(xid=1): Create(path=u'/namekox/admin.5197989e-5e14-4974-bf40-2e1d955f615d', data='{"port": 64439, "address": "192.168.43.170"}', acl=[ACL(perms=31, acl_list=['ALL'], id=Id(scheme='world', id='anyone'))], flags=1)
2021-03-17 21:30:44,941 DEBUG service admin dependencies [admin:namekox_context.core.dependencies.ContextHelper:ctx, admin:namekox_zookeeper.core.dependencies.ZooKeeperHelper:zk, admin:namekox_config.core.dependencies.ConfigHelper:cfg, admin:namekox_zipkin.core.dependencies.ZipkinHelper:zipkin] started
2021-03-17 21:30:44,941 DEBUG Sending request(xid=2): GetChildren(path=u'/namekox', watcher=None)
2021-03-17 21:30:44,942 DEBUG services [u'admin'] started
2021-03-17 21:30:44,943 DEBUG Sending request(xid=3): GetChildren(path=u'/namekox', watcher=<bound method ChildrenWatch._watcher of <kazoo.recipe.watchers.ChildrenWatch object at 0x108ebfa50>>)
2021-03-17 21:30:44,944 DEBUG Sending request(xid=4): Create(path=u'/namekox/admin.5197989e-5e14-4974-bf40-2e1d955f615d', data='{"port": 64439, "address": "192.168.43.170"}', acl=[ACL(perms=31, acl_list=['ALL'], id=Id(scheme='world', id='anyone'))], flags=1)
2021-03-17 21:30:44,948 DEBUG Received response(xid=1): u'/namekox/admin.5197989e-5e14-4974-bf40-2e1d955f615d'
2021-03-17 21:30:44,951 DEBUG Received response(xid=2): [u'gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', u'admin.5197989e-5e14-4974-bf40-2e1d955f615d', u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:30:44,952 DEBUG Received response(xid=3): [u'gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', u'admin.5197989e-5e14-4974-bf40-2e1d955f615d', u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:30:44,954 DEBUG Received error(xid=4) NodeExistsError()
2021-03-17 21:30:44,954 DEBUG Sending request(xid=5): GetData(path=u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', watcher=None)
2021-03-17 21:30:44,956 DEBUG Sending request(xid=6): GetData(path=u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', watcher=None)
2021-03-17 21:30:44,959 DEBUG Received response(xid=5): ('{"port": 63687, "address": "192.168.43.170"}', ZnodeStat(czxid=6126, mzxid=6126, ctime=1615987807221, mtime=1615987807221, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418959, dataLength=44, numChildren=0, pzxid=6126))
2021-03-17 21:30:44,964 DEBUG Received response(xid=6): ('{"port": 63687, "address": "192.168.43.170"}', ZnodeStat(czxid=6126, mzxid=6126, ctime=1615987807221, mtime=1615987807221, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418959, dataLength=44, numChildren=0, pzxid=6126))
2021-03-17 21:30:44,965 DEBUG Sending request(xid=7): GetData(path=u'/namekox/admin.5197989e-5e14-4974-bf40-2e1d955f615d', watcher=None)
2021-03-17 21:30:44,967 DEBUG Sending request(xid=8): GetData(path=u'/namekox/admin.5197989e-5e14-4974-bf40-2e1d955f615d', watcher=None)
2021-03-17 21:30:44,971 DEBUG Received response(xid=7): ('{"port": 64439, "address": "192.168.43.170"}', ZnodeStat(czxid=6129, mzxid=6129, ctime=1615987844942, mtime=1615987844942, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418960, dataLength=44, numChildren=0, pzxid=6129))
2021-03-17 21:30:44,976 DEBUG Received response(xid=8): ('{"port": 64439, "address": "192.168.43.170"}', ZnodeStat(czxid=6129, mzxid=6129, ctime=1615987844942, mtime=1615987844942, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418960, dataLength=44, numChildren=0, pzxid=6129))
2021-03-17 21:30:44,979 DEBUG Sending request(xid=9): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:30:44,980 DEBUG Sending request(xid=10): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:30:44,983 DEBUG Received response(xid=9): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:30:44,995 DEBUG Received response(xid=10): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:31:18,632 DEBUG Received EVENT: Watch(type=4, state=3, path=u'/namekox')
2021-03-17 21:31:18,634 DEBUG Sending request(xid=11): GetChildren(path=u'/namekox', watcher=<bound method ChildrenWatch._watcher of <kazoo.recipe.watchers.ChildrenWatch object at 0x108ebfa50>>)
2021-03-17 21:31:18,641 DEBUG Received response(xid=11): [u'gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', u'admin.5197989e-5e14-4974-bf40-2e1d955f615d', u'user.5e94f263-58fe-4059-bea1-daf5fb1956b9', u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:31:18,642 DEBUG Sending request(xid=12): GetData(path=u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', watcher=None)
2021-03-17 21:31:18,648 DEBUG Received response(xid=12): ('{"port": 63687, "address": "192.168.43.170"}', ZnodeStat(czxid=6126, mzxid=6126, ctime=1615987807221, mtime=1615987807221, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418959, dataLength=44, numChildren=0, pzxid=6126))
2021-03-17 21:31:18,648 DEBUG Sending request(xid=13): GetData(path=u'/namekox/admin.5197989e-5e14-4974-bf40-2e1d955f615d', watcher=None)
2021-03-17 21:31:18,652 DEBUG Received response(xid=13): ('{"port": 64439, "address": "192.168.43.170"}', ZnodeStat(czxid=6129, mzxid=6129, ctime=1615987844942, mtime=1615987844942, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418960, dataLength=44, numChildren=0, pzxid=6129))
2021-03-17 21:31:18,652 DEBUG Sending request(xid=14): GetData(path=u'/namekox/user.5e94f263-58fe-4059-bea1-daf5fb1956b9', watcher=None)
2021-03-17 21:31:18,662 DEBUG Received response(xid=14): ('{"port": 65125, "address": "192.168.43.170"}', ZnodeStat(czxid=6132, mzxid=6132, ctime=1615987878624, mtime=1615987878624, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418961, dataLength=44, numChildren=0, pzxid=6132))
2021-03-17 21:31:18,677 DEBUG Sending request(xid=15): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:31:18,681 DEBUG Received response(xid=15): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:31:27,995 DEBUG spawn manage thread handle admin:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x108ed6d90>, ('192.168.43.170', 65476)), kwargs={}, tid=handle_request)
2021-03-17 21:31:28,007 DEBUG spawn worker thread handle admin:gen_user_token(args=[], kwargs={}, context={u'parent_call_id': None, u'origin_id': u'b4f8c690fea2b8f3', u'call_id': u'b4f8c690fea2b8f3'})
2021-03-17 21:31:28,011 DEBUG post http://192.168.43.170:65125/auth with args=(), kwargs={u'__call_mode__': 0}
192.168.43.170 - - [17/Mar/2021 21:31:28] "POST /gen_user_token HTTP/1.1" 200 157 0.072683
```
> namekox run user
```shell script
2021-03-17 21:31:10,561 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2021-03-17 21:31:14,586 DEBUG starting services [u'user']
2021-03-17 21:31:14,587 DEBUG starting service user entrypoints [user:namekox_jsonrpc.core.entrypoints.rpc.handler.JSONRpcHandler:auth, user:namekox_jsonrpc.core.entrypoints.rpc.server.JSONRpcServer:server]
2021-03-17 21:31:14,590 DEBUG spawn manage thread handle user:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2021-03-17 21:31:14,591 DEBUG service user entrypoints [user:namekox_jsonrpc.core.entrypoints.rpc.handler.JSONRpcHandler:auth, user:namekox_jsonrpc.core.entrypoints.rpc.server.JSONRpcServer:server] started
2021-03-17 21:31:14,591 DEBUG starting service user dependencies [user:namekox_config.core.dependencies.ConfigHelper:cfg, user:namekox_zookeeper.core.dependencies.ZooKeeperHelper:zk, user:namekox_context.core.dependencies.ContextHelper:ctx, user:namekox_zipkin.core.dependencies.ZipkinHelper:zipkin]
2021-03-17 21:31:14,593 INFO Connecting to 127.0.0.1:2181
2021-03-17 21:31:14,593 DEBUG Sending request(xid=None): Connect(protocol_version=0, last_zxid_seen=0, time_out=30000, session_id=0, passwd='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', read_only=None)
2021-03-17 21:31:14,604 INFO Zookeeper connection established, state: CONNECTED
2021-03-17 21:31:18,619 DEBUG Sending request(xid=1): Create(path=u'/namekox/user.5e94f263-58fe-4059-bea1-daf5fb1956b9', data='{"port": 65125, "address": "192.168.43.170"}', acl=[ACL(perms=31, acl_list=['ALL'], id=Id(scheme='world', id='anyone'))], flags=1)
2021-03-17 21:31:18,622 DEBUG service user dependencies [user:namekox_config.core.dependencies.ConfigHelper:cfg, user:namekox_zookeeper.core.dependencies.ZooKeeperHelper:zk, user:namekox_context.core.dependencies.ContextHelper:ctx, user:namekox_zipkin.core.dependencies.ZipkinHelper:zipkin] started
2021-03-17 21:31:18,623 DEBUG Sending request(xid=2): GetChildren(path=u'/namekox', watcher=None)
2021-03-17 21:31:18,623 DEBUG services [u'user'] started
2021-03-17 21:31:18,624 DEBUG Sending request(xid=3): GetChildren(path=u'/namekox', watcher=<bound method ChildrenWatch._watcher of <kazoo.recipe.watchers.ChildrenWatch object at 0x10ff07a50>>)
2021-03-17 21:31:18,625 DEBUG Sending request(xid=4): Create(path=u'/namekox/user.5e94f263-58fe-4059-bea1-daf5fb1956b9', data='{"port": 65125, "address": "192.168.43.170"}', acl=[ACL(perms=31, acl_list=['ALL'], id=Id(scheme='world', id='anyone'))], flags=1)
2021-03-17 21:31:18,634 DEBUG Received response(xid=1): u'/namekox/user.5e94f263-58fe-4059-bea1-daf5fb1956b9'
2021-03-17 21:31:18,636 DEBUG Received response(xid=2): [u'gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', u'admin.5197989e-5e14-4974-bf40-2e1d955f615d', u'user.5e94f263-58fe-4059-bea1-daf5fb1956b9', u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:31:18,637 DEBUG Received response(xid=3): [u'gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', u'admin.5197989e-5e14-4974-bf40-2e1d955f615d', u'user.5e94f263-58fe-4059-bea1-daf5fb1956b9', u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:31:18,640 DEBUG Received error(xid=4) NodeExistsError()
2021-03-17 21:31:18,641 DEBUG Sending request(xid=5): GetData(path=u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', watcher=None)
2021-03-17 21:31:18,642 DEBUG Sending request(xid=6): GetData(path=u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', watcher=None)
2021-03-17 21:31:18,647 DEBUG Received response(xid=5): ('{"port": 63687, "address": "192.168.43.170"}', ZnodeStat(czxid=6126, mzxid=6126, ctime=1615987807221, mtime=1615987807221, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418959, dataLength=44, numChildren=0, pzxid=6126))
2021-03-17 21:31:18,648 DEBUG Received response(xid=6): ('{"port": 63687, "address": "192.168.43.170"}', ZnodeStat(czxid=6126, mzxid=6126, ctime=1615987807221, mtime=1615987807221, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418959, dataLength=44, numChildren=0, pzxid=6126))
2021-03-17 21:31:18,649 DEBUG Sending request(xid=7): GetData(path=u'/namekox/admin.5197989e-5e14-4974-bf40-2e1d955f615d', watcher=None)
2021-03-17 21:31:18,650 DEBUG Sending request(xid=8): GetData(path=u'/namekox/admin.5197989e-5e14-4974-bf40-2e1d955f615d', watcher=None)
2021-03-17 21:31:18,652 DEBUG Received response(xid=7): ('{"port": 64439, "address": "192.168.43.170"}', ZnodeStat(czxid=6129, mzxid=6129, ctime=1615987844942, mtime=1615987844942, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418960, dataLength=44, numChildren=0, pzxid=6129))
2021-03-17 21:31:18,653 DEBUG Sending request(xid=9): GetData(path=u'/namekox/user.5e94f263-58fe-4059-bea1-daf5fb1956b9', watcher=None)
2021-03-17 21:31:18,660 DEBUG Received response(xid=8): ('{"port": 64439, "address": "192.168.43.170"}', ZnodeStat(czxid=6129, mzxid=6129, ctime=1615987844942, mtime=1615987844942, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418960, dataLength=44, numChildren=0, pzxid=6129))
2021-03-17 21:31:18,678 DEBUG Received response(xid=9): ('{"port": 65125, "address": "192.168.43.170"}', ZnodeStat(czxid=6132, mzxid=6132, ctime=1615987878624, mtime=1615987878624, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418961, dataLength=44, numChildren=0, pzxid=6132))
2021-03-17 21:31:18,678 DEBUG Sending request(xid=10): GetData(path=u'/namekox/user.5e94f263-58fe-4059-bea1-daf5fb1956b9', watcher=None)
2021-03-17 21:31:18,679 DEBUG Sending request(xid=11): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:31:18,682 DEBUG Received response(xid=10): ('{"port": 65125, "address": "192.168.43.170"}', ZnodeStat(czxid=6132, mzxid=6132, ctime=1615987878624, mtime=1615987878624, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418961, dataLength=44, numChildren=0, pzxid=6132))
2021-03-17 21:31:18,683 DEBUG Received response(xid=11): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:31:18,683 DEBUG Sending request(xid=12): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:31:18,685 DEBUG Received response(xid=12): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:31:28,019 DEBUG spawn manage thread handle user:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x10ff074d0>, ('192.168.43.170', 65478)), kwargs={}, tid=handle_request)
2021-03-17 21:31:28,023 DEBUG spawn worker thread handle user:auth(args=[], kwargs={}, context={u'parent_call_id': u'b4f8c690fea2b8f3', u'origin_id': u'b4f8c690fea2b8f3', u'call_id': u'9895292c04d8f29c'})
2021-03-17 21:31:28,024 DEBUG post http://192.168.43.170:62853/authenticate with args=(), kwargs={u'__call_mode__': 0}
192.168.43.170 - - [17/Mar/2021 21:31:28] "POST /auth HTTP/1.1" 200 157 0.044100
```
> namekox run ad
```shell script
2021-03-17 21:29:18,284 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2021-03-17 21:29:22,309 DEBUG starting services [u'ad']
2021-03-17 21:29:22,310 DEBUG starting service ad entrypoints [ad:namekox_jsonrpc.core.entrypoints.rpc.handler.JSONRpcHandler:authenticate, ad:namekox_jsonrpc.core.entrypoints.rpc.server.JSONRpcServer:server]
2021-03-17 21:29:22,312 DEBUG spawn manage thread handle ad:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2021-03-17 21:29:22,312 DEBUG service ad entrypoints [ad:namekox_jsonrpc.core.entrypoints.rpc.handler.JSONRpcHandler:authenticate, ad:namekox_jsonrpc.core.entrypoints.rpc.server.JSONRpcServer:server] started
2021-03-17 21:29:22,312 DEBUG starting service ad dependencies [ad:namekox_context.core.dependencies.ContextHelper:ctx, ad:namekox_config.core.dependencies.ConfigHelper:cfg, ad:namekox_zookeeper.core.dependencies.ZooKeeperHelper:zk, ad:namekox_zipkin.core.dependencies.ZipkinHelper:zipkin]
2021-03-17 21:29:22,314 INFO Connecting to 127.0.0.1:2181
2021-03-17 21:29:22,315 DEBUG Sending request(xid=None): Connect(protocol_version=0, last_zxid_seen=0, time_out=30000, session_id=0, passwd='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', read_only=None)
2021-03-17 21:29:22,344 INFO Zookeeper connection established, state: CONNECTED
2021-03-17 21:29:26,365 DEBUG service ad dependencies [ad:namekox_context.core.dependencies.ContextHelper:ctx, ad:namekox_config.core.dependencies.ConfigHelper:cfg, ad:namekox_zookeeper.core.dependencies.ZooKeeperHelper:zk, ad:namekox_zipkin.core.dependencies.ZipkinHelper:zipkin] started
2021-03-17 21:29:26,366 DEBUG Sending request(xid=1): GetChildren(path=u'/namekox', watcher=<bound method ChildrenWatch._watcher of <kazoo.recipe.watchers.ChildrenWatch object at 0x10880a090>>)
2021-03-17 21:29:26,367 DEBUG services [u'ad'] started
2021-03-17 21:29:26,368 DEBUG Sending request(xid=2): Create(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', data='{"port": 62853, "address": "192.168.43.170"}', acl=[ACL(perms=31, acl_list=['ALL'], id=Id(scheme='world', id='anyone'))], flags=1)
2021-03-17 21:29:26,368 DEBUG Sending request(xid=3): GetChildren(path=u'/namekox', watcher=None)
2021-03-17 21:29:26,369 DEBUG Sending request(xid=4): Create(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', data='{"port": 62853, "address": "192.168.43.170"}', acl=[ACL(perms=31, acl_list=['ALL'], id=Id(scheme='world', id='anyone'))], flags=1)
2021-03-17 21:29:26,376 DEBUG Received response(xid=1): [u'ad.b47c8f53-815a-416a-b43b-7ea9df5cfcbf']
2021-03-17 21:29:26,376 DEBUG Sending request(xid=5): GetData(path=u'/namekox/ad.b47c8f53-815a-416a-b43b-7ea9df5cfcbf', watcher=None)
2021-03-17 21:29:26,379 DEBUG Received EVENT: Watch(type=4, state=3, path=u'/namekox')
2021-03-17 21:29:26,382 DEBUG Received response(xid=2): u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859'
2021-03-17 21:29:26,384 DEBUG Received response(xid=3): [u'ad.b47c8f53-815a-416a-b43b-7ea9df5cfcbf', u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:29:26,385 DEBUG Received error(xid=4) NodeExistsError()
2021-03-17 21:29:26,392 DEBUG Received response(xid=5): ('{"port": 6004, "address": "192.168.43.170"}', ZnodeStat(czxid=6119, mzxid=6119, ctime=1615987072824, mtime=1615987072824, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418957, dataLength=43, numChildren=0, pzxid=6119))
2021-03-17 21:29:26,393 DEBUG Sending request(xid=6): GetData(path=u'/namekox/ad.b47c8f53-815a-416a-b43b-7ea9df5cfcbf', watcher=None)
2021-03-17 21:29:26,394 DEBUG Sending request(xid=7): GetChildren(path=u'/namekox', watcher=<bound method ChildrenWatch._watcher of <kazoo.recipe.watchers.ChildrenWatch object at 0x10880a090>>)
2021-03-17 21:29:26,396 DEBUG Received response(xid=6): ('{"port": 6004, "address": "192.168.43.170"}', ZnodeStat(czxid=6119, mzxid=6119, ctime=1615987072824, mtime=1615987072824, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418957, dataLength=43, numChildren=0, pzxid=6119))
2021-03-17 21:29:26,398 DEBUG Received response(xid=7): [u'ad.b47c8f53-815a-416a-b43b-7ea9df5cfcbf', u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:29:26,399 DEBUG Sending request(xid=8): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:29:26,400 DEBUG Sending request(xid=9): GetData(path=u'/namekox/ad.b47c8f53-815a-416a-b43b-7ea9df5cfcbf', watcher=None)
2021-03-17 21:29:26,401 DEBUG Received response(xid=8): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:29:26,402 DEBUG Received response(xid=9): ('{"port": 6004, "address": "192.168.43.170"}', ZnodeStat(czxid=6119, mzxid=6119, ctime=1615987072824, mtime=1615987072824, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418957, dataLength=43, numChildren=0, pzxid=6119))
2021-03-17 21:29:26,403 DEBUG Sending request(xid=10): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:29:26,406 DEBUG Received response(xid=10): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:29:35,243 DEBUG Received EVENT: Watch(type=4, state=3, path=u'/namekox')
2021-03-17 21:29:35,247 DEBUG Sending request(xid=11): GetChildren(path=u'/namekox', watcher=<bound method ChildrenWatch._watcher of <kazoo.recipe.watchers.ChildrenWatch object at 0x10880a090>>)
2021-03-17 21:29:35,253 DEBUG Received response(xid=11): [u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:29:35,262 DEBUG Sending request(xid=12): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:29:35,271 DEBUG Received response(xid=12): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:30:07,224 DEBUG Received EVENT: Watch(type=4, state=3, path=u'/namekox')
2021-03-17 21:30:07,225 DEBUG Sending request(xid=13): GetChildren(path=u'/namekox', watcher=<bound method ChildrenWatch._watcher of <kazoo.recipe.watchers.ChildrenWatch object at 0x10880a090>>)
2021-03-17 21:30:07,236 DEBUG Received response(xid=13): [u'gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:30:07,239 DEBUG Sending request(xid=14): GetData(path=u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', watcher=None)
2021-03-17 21:30:07,242 DEBUG Received response(xid=14): ('{"port": 63687, "address": "192.168.43.170"}', ZnodeStat(czxid=6126, mzxid=6126, ctime=1615987807221, mtime=1615987807221, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418959, dataLength=44, numChildren=0, pzxid=6126))
2021-03-17 21:30:07,243 DEBUG Sending request(xid=15): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:30:07,248 DEBUG Received response(xid=15): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:30:44,947 DEBUG Received EVENT: Watch(type=4, state=3, path=u'/namekox')
2021-03-17 21:30:44,952 DEBUG Sending request(xid=16): GetChildren(path=u'/namekox', watcher=<bound method ChildrenWatch._watcher of <kazoo.recipe.watchers.ChildrenWatch object at 0x10880a090>>)
2021-03-17 21:30:44,956 DEBUG Received response(xid=16): [u'gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', u'admin.5197989e-5e14-4974-bf40-2e1d955f615d', u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:30:44,958 DEBUG Sending request(xid=17): GetData(path=u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', watcher=None)
2021-03-17 21:30:44,964 DEBUG Received response(xid=17): ('{"port": 63687, "address": "192.168.43.170"}', ZnodeStat(czxid=6126, mzxid=6126, ctime=1615987807221, mtime=1615987807221, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418959, dataLength=44, numChildren=0, pzxid=6126))
2021-03-17 21:30:44,966 DEBUG Sending request(xid=18): GetData(path=u'/namekox/admin.5197989e-5e14-4974-bf40-2e1d955f615d', watcher=None)
2021-03-17 21:30:44,975 DEBUG Received response(xid=18): ('{"port": 64439, "address": "192.168.43.170"}', ZnodeStat(czxid=6129, mzxid=6129, ctime=1615987844942, mtime=1615987844942, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418960, dataLength=44, numChildren=0, pzxid=6129))
2021-03-17 21:30:44,977 DEBUG Sending request(xid=19): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:30:44,981 DEBUG Received response(xid=19): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:31:18,631 DEBUG Received EVENT: Watch(type=4, state=3, path=u'/namekox')
2021-03-17 21:31:18,636 DEBUG Sending request(xid=20): GetChildren(path=u'/namekox', watcher=<bound method ChildrenWatch._watcher of <kazoo.recipe.watchers.ChildrenWatch object at 0x10880a090>>)
2021-03-17 21:31:18,646 DEBUG Received response(xid=20): [u'gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', u'admin.5197989e-5e14-4974-bf40-2e1d955f615d', u'user.5e94f263-58fe-4059-bea1-daf5fb1956b9', u'ad.60d7f508-7256-40cf-bfff-b8f202dde859']
2021-03-17 21:31:18,647 DEBUG Sending request(xid=21): GetData(path=u'/namekox/gateway.8f8016c7-9b27-4829-a45b-b22ccd40de41', watcher=None)
2021-03-17 21:31:18,650 DEBUG Received response(xid=21): ('{"port": 63687, "address": "192.168.43.170"}', ZnodeStat(czxid=6126, mzxid=6126, ctime=1615987807221, mtime=1615987807221, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418959, dataLength=44, numChildren=0, pzxid=6126))
2021-03-17 21:31:18,651 DEBUG Sending request(xid=22): GetData(path=u'/namekox/admin.5197989e-5e14-4974-bf40-2e1d955f615d', watcher=None)
2021-03-17 21:31:18,660 DEBUG Received response(xid=22): ('{"port": 64439, "address": "192.168.43.170"}', ZnodeStat(czxid=6129, mzxid=6129, ctime=1615987844942, mtime=1615987844942, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418960, dataLength=44, numChildren=0, pzxid=6129))
2021-03-17 21:31:18,661 DEBUG Sending request(xid=23): GetData(path=u'/namekox/user.5e94f263-58fe-4059-bea1-daf5fb1956b9', watcher=None)
2021-03-17 21:31:18,665 DEBUG Received response(xid=23): ('{"port": 65125, "address": "192.168.43.170"}', ZnodeStat(czxid=6132, mzxid=6132, ctime=1615987878624, mtime=1615987878624, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418961, dataLength=44, numChildren=0, pzxid=6132))
2021-03-17 21:31:18,677 DEBUG Sending request(xid=24): GetData(path=u'/namekox/ad.60d7f508-7256-40cf-bfff-b8f202dde859', watcher=None)
2021-03-17 21:31:18,681 DEBUG Received response(xid=24): ('{"port": 62853, "address": "192.168.43.170"}', ZnodeStat(czxid=6122, mzxid=6122, ctime=1615987766371, mtime=1615987766371, version=0, cversion=0, aversion=0, ephemeralOwner=72100379689418958, dataLength=44, numChildren=0, pzxid=6122))
2021-03-17 21:31:28,032 DEBUG spawn manage thread handle ad:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x1087e3c90>, ('192.168.43.170', 65479)), kwargs={}, tid=handle_request)
2021-03-17 21:31:28,040 DEBUG spawn worker thread handle ad:authenticate(args=[], kwargs={}, context={u'parent_call_id': u'9895292c04d8f29c', u'origin_id': u'b4f8c690fea2b8f3', u'call_id': u'd45ccca1b6d34a07'})
192.168.43.170 - - [17/Mar/2021 21:31:28] "POST /authenticate HTTP/1.1" 200 157 0.026409
2021-03-17 21:32:47,877 DEBUG spawn manage thread handle ad:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x1087e3910>, ('192.168.43.170', 50736)), kwargs={}, tid=handle_request)
2021-03-17 21:32:47,888 DEBUG spawn worker thread handle ad:authenticate(args=[], kwargs={}, context={u'parent_call_id': u'86bf1d09594fb1d0', u'origin_id': u'fd5a07dc862e60ba', u'call_id': u'7d1db6904aad81ea'})
```
> curl http://127.0.0.1/api/user/token/
```json5
{
    "errs": "",
    "code": "Request:Success",
    "data": "succ",
    "call_id": "3ca08c834dfb3401"
}
```
