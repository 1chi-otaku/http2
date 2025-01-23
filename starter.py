from http.server import HTTPServer, BaseHTTPRequestHandler
import os

static_files_path = r"C:/Users/1chi/http/wwwroot"
#
class MainHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #print('self.path', self.path)
        
        if '?' in self.path:
            (path,qs) = self.path.split('?', 1)
        else:
            path,qs = self.path, None

        print ('path', path)
        print ('qs', qs)

        if '../' in path:
            self.send_404(self)

#         query_string = urllib.parse.unquote( envs['QUERY_STRING'], encoding="utf-8" )
# query_parameters = dict( pair.split('=', maxsplit = 1) if '=' in pair else (pair, None)
#                     for pair in query_string.split('&') if pair != "" )


        fname = static_files_path + (self.path if self.path!= '/' else '/index.html')
        print(fname)
        if os.path.isfile(fname):
            self.send_file(fname)
            return
        self.send_404(self)

       

    def send_404(self):
        self.send_response(404)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open(static_files_path + '/404.html', 'rb') as f:
            self.wfile.write(f.read())



    def send_file(self, fname):
        ext = fname.split('.')[-1] if '.' in fname else ''
        if ext in ('py', 'php'): self.send_404(); return
        if ext == 'txt' :  mime_type = 'text/plain'
        elif ext == 'ico': mime_type = 'image/x-icon'
        elif ext == 'js':  mime_type = 'text/javascript'
        elif ext in ('html', 'css'): mime_type = 'text/' + ext
        elif ext in ('jpg', 'jpeg'): mime_type = 'image/jpeg' + ext
        elif ext in ('png', 'bmp', 'gif'): mime_type = 'image/' + ext
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






'''

 Власний сервер. HTTP.
 Інший підхід до стоверння серверних програм - власний сервер
 відповідною мовою програмування
 + Немає потреби у сторонньому сервері
 - Такі сервери зазвичай повільніші
 + Робота єдиною мовою програмування
 - Потреба у гарантії вільного порту
 + Самостійний деплой, у т.ч. хостінга
 - Аналіз параметрів запиту - задача програми
 CGI- не "рідний" сторонній (окремий) сервер
HTTP - власний сервер (як частина коду)
 Host - "рідний" сторонній сервер



 Запуск сервера:
 зазвичай клас сервера надаэться мовою (библиотекой)
 сервер стартует по адресу (IP:port) и "зависает" - переходит у постоенное слушание
 с каждыйм запросом сервер запускает функцию-обработчик или объект 

 Формировання ответа:
 согласно структуре пакета HTTPP необходимо формировати три состовляющие:
 - статус код и фразу
 - заголовки
 - тело ответа

 Разные библиотеки могут давать разные способы для упрощения их формирования, 
 в частности у HTTPServer  необходимо формировать все три. Минимальный ответ выглядит так:
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write( b"<h1>Works</h1>")

        
404: запрос для сервера - всего лишь строчка, который он обрабаботав передает в функцию-обработчик
Понятие "не найдено" для сервера не существует, это задача обработчика. 

Дополнительно к задаче 404 есть задача отсылания статически файлов, а также ограниченеи
доступа к "службовим" файлам.
а) слздать отдельную директорию для статический фалйов
б) добавить фильтр для расширенных файлов.

Классическая задача - обеспечить работу стилией и JS

Передача параметров и маршрутизация
Проверить:
    Отделяеются ли части URL hash (#), query (?) [не отделяются]
    Разделяется ли query string [не разделяются]
    Проводится ли декодирование URL параметров [не проводится]





'''


