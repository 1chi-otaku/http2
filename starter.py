from http.server import HTTPServer, BaseHTTPRequestHandler
import os, sys
import urllib.parse
import HomeController

static_files_path = r"C:/Users/1chi/http/wwwroot"

def ucfirst(input: str):
    if len(input) == 0:
        return input
    if len(input) == 1:
        return input[0].upper()
    return input[0].upper() + input[1:].lower()

class MainHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Разбираем путь и параметры запроса
        if '?' in self.path:
            path, qs = map(urllib.parse.unquote, self.path.split('?', 1)) 
        else:
            path, qs = urllib.parse.unquote(self.path), None

        if '../' in path:
            self.send_404()


        fname = static_files_path + path
        if os.path.isfile(fname):
            self.send_file(fname)
            return
        
        query_parameters = dict(
            pair.split('=', maxsplit=1) if '=' in pair else (pair, None)
            for pair in qs.split('&') if pair != ""
        ) if qs is not None else {}
        
        # Разделяем путь на части (Controller/Action/Slug)
        parts = path.strip('/').split('/', maxsplit=3)
        
        controller = parts[0] if len(parts) > 0 else 'home'
        action = parts[1] if len(parts) > 1 else 'index'
        slug = parts[2] if len(parts) > 2 else None

        # Формируем имя контроллера
        controller_name = ucfirst(controller) + "Controller"
        controller_module = getattr(sys.modules[__name__], controller_name, None)
        
        if controller_module is None:
            self.send_404()
            return

        # Проверяем есть ли в классе-контроллере метод с именем, как в переменной action
        controller_class = getattr(controller_module, controller_name, None)
        if controller_class is None:
            self.send_404()
            return
        controller_instance = controller_class()

        controller_action = getattr(controller_instance, action.lower(), None)
        if controller_action is None:
            self.send_404()
            return
        
        with open(static_files_path + '/index.html', 'r', encoding='utf-8') as f:
            layout = f.read()
        layout_body = controller_action()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        self.wfile.write(layout.replace('@RenderBody',layout_body).encode())     

    def send_404(self):
        self.send_response(404)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open(static_files_path + '/404.html', 'rb') as f:
            self.wfile.write(f.read())

    def send_file(self, fname):
        ext = fname.split('.')[-1] if '.' in fname else ''
        if ext in ('py', 'php'):
            self.send_404()
            return
        if ext == 'txt':
            mime_type = 'text/plain'
        elif ext == 'ico':
            mime_type = 'image/x-icon'
        elif ext == 'js':
            mime_type = 'text/javascript'
        elif ext in ('html', 'css'):
            mime_type = 'text/' + ext
        elif ext in ('jpg', 'jpeg'):
            mime_type = 'image/jpeg'
        elif ext in ('png', 'bmp', 'gif'):
            mime_type = 'image/' + ext
        else:
            mime_type = 'application/octet-stream'

        self.send_response(200)
        self.send_header('Content-Type', mime_type)
        self.end_headers()
        with open(fname, 'rb') as f:
            self.wfile.write(f.read())

def main():
    httpServer = HTTPServer(('127.0.0.1', 81), MainHandler)
    try:
        print("Server starting...")
        httpServer.serve_forever()
    except:
        print("Server stopped")

if __name__ == "__main__":
    main()
