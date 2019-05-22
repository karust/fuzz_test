from aiohttp import web, ClientSession
import os
import json


cwd = os.getcwd()
routes = web.RouteTableDef()


@routes.view("/")
class Main(web.View):
    async def get(self):
        print(self.request.query)
        if self.request.query["search"] == "'or select *":
            return web.Response(text="table_schema, metadata, users, items, orders", status=200)
        else:
            return web.FileResponse(cwd+'/index.html')


@routes.view("/admin")
class Analyzing(web.View):
    async def get(self):
        return web.FileResponse(cwd+'/admin.html')

    async def post(self):
        data = await self.request.post()
        if data["login"] == "Admin" and data["password"] == "password!":    
            return web.HTTPOk()
        else:
            return web.HTTPUnauthorized()

@routes.view('/upload')
class FileLoad(web.View):
    async def post(self):
        pack = await self.request.content.read()
        return web.HTTPOk()

    async def options(self):
        return web.Response(text=json.dumps({}), status=200)


class Server(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.app = web.Application()
        self.app.add_routes(routes)

    def run(self):
        web.run_app(self.app, host=self.ip, port=self.port)

if __name__ == "__main__":
    server = Server(ip='127.0.0.1', port=8000)
    server.run()