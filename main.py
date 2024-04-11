import aiohttp
from aiohttp import web

import time
import hashlib
import os

from neurannparser import GenericChromosomeParseResult

async def g_index(request):
    return web.FileResponse("index.html")


def get_time_hash():
    return hashlib.sha256(bytes(time.time_ns())).hexdigest()

def try_parse_chromosome(filepath) -> GenericChromosomeParseResult:
    return GenericChromosomeParseResult.from_file(filepath)

async def p_upload(request):
    postargs = await request.post()
    if (not "chromosome_file" in postargs) or (not isinstance(postargs["chromosome_file"], aiohttp.web_request.FileField)):
        raise web.HTTPBadRequest(text="Bad/missing chromosome file")
    
    filename = postargs["chromosome_file"].file.name
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "wb") as f:
        f.write(postargs["chromosome_file"].file.read())

    
    result = try_parse_chromosome(filename)
    os.remove(filename)

    return web.Response(text=str(result.parse_result))

app = web.Application()
app.add_routes([
    web.get("/", g_index),
    web.post("/test_upload", p_upload)
])

web.run_app(app)