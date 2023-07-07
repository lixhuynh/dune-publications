from tornado import web as web, ioloop as ioloop
import nest_asyncio

PAGE_PATH = "C:/Users/potas/OneDrive/Documents/GitHub/dune-publications/index.html"
PAGE = open(PAGE_PATH, "r")
PORT = 8888

nest_asyncio.apply()

class basicRequestHandler(web.RequestHandler):
    def get(self):
        self.write(PAGE.read())
    
if __name__ == "__main__":
    app = web.Application([
        (r"/", basicRequestHandler)
    ])
    app.listen(PORT) # Page available at localhost:PORT
    ioloop.IOLoop.current().start()