<center>
<div class="comment_title"><b>Přihlaste se prosím:</b></div>
<div class="comment_form">
<form method="post" action="" accept-charset="UTF-8" enctype="multipart/form-data">
	<label for="login">Uživatelské jméno:</label><br>
	<input type="text" name="login" placeholder="Login name"><br>
	<label for="password">Heslo:</label><br>
	<input type="password" name="password" placeholder="Password"><br>
	<input type="checkbox" onclick="showPassword()">Show Password<br>
	<input type="submit" value="Odeslat">
</form>
</div>
<div class="comment_title"><b>Pokud nejste registrováni, můžete tak učinit <a href="/register">ZDE</a></b></div>
<script>
function showPassword() {
var x = document.getElementsByName("password")[0];
if (x.type === "password") {
	x.type = "text";
} else {
	x.type = "password";
}
}
</script>
</center>
