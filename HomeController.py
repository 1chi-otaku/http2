class HomeController :
    def index(self) :
        return '''
<form method="post">
<div class="input-group mb-3">
  <span class="input-group-text" id="basic-addon1">@</span>
  <input name="user-name" type="text" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="basic-addon1">
</div>
 
<div class="input-group mb-3">
  <span class="input-group-text" id="basic-addon2">@</span>
  <input name="user-email" type="email" class="form-control" placeholder="E-mail" aria-label="E-mail" aria-describedby="basic-addon2">
</div>
 
<div class="input-group mb-3">
  <span class="input-group-text" id="basic-addon3">@</span>
  <input name="user-password" type="password" class="form-control" placeholder="****" aria-label="password" aria-describedby="basic-addon3">
</div>

<button type="submit" class="btn btn-outline-secondary">Register</button>
</form>
'''