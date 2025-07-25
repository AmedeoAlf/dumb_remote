from aiohttp import web, WSMsgType
from components import components

app = web.Application()


async def serveFile(request):
    path = request.path if request.path != "/" else "/index.html"
    return web.FileResponse(f"client{path}")


async def websocketConnection(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print("websocket connection opened")

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                commands = msg.data.split()
                components[commands[0]](commands)
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')
    return ws

app.router.add_get("/{tail:.*}", serveFile)
app.router.add_get("/ws", websocketConnection)
web.run_app(app)
