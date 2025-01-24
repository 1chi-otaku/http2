from starter import MainHandler
from ActionResult import ActionResult

class HomeController :
    def __init__(self, handler:MainHandler):
        self.handler = handler
        self.handler
    

    def index(self) -> ActionResult :
        if self.handler.command == 'POST':
            content_type = self.handler.headers.get("Content-Type", 
                self.handler.headers.get("content-type", None))
            if content_type == 'application/x-www-form-urlencoded':
                body = self.handler.parse_urlencoded(self.handler.rfile.read(int(self.handler.headers.get('Content-Length'))).decode())
                user_name = body.get('user-name', '')
                if user_name == '':
                    return ActionResult(type='Redirect', code=302, payload=f"/Home/Signup?msg=Error")
                else:
                    return ActionResult(type='Redirect', code=302, payload=f"/Home/Signup?user-name=" + user_name)

            else:
                return ActionResult(type='Error', code=415, payload=f"Content-Type '{content_type}' not supported")
        else:
            view_path = ('C:/Users/1chi/http/views/' + self.handler.controller.lower() + '/' +
                                           self.handler.action.lower() + '.html')
            with open(view_path, 'r', encoding='utf-8') as view:
                return ActionResult(view.read())
            
    def signup(self) -> ActionResult :
        params = self.handler.query_parameters
        user_name = params.get('user-name', None)

        if user_name is not None:
            return ActionResult("Congrats with registr, " + user_name)
        else:
            return ActionResult("Error with register: " + params.get('msg', ''))