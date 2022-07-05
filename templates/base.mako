<!DOCTYPE html>
<html lang="cs">
<head>
	<title>EasyTasker</title>
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="content-type" content="text/html; charset=UTF-8">
	<meta name="description" content="Small tasker for Deso.">
	<meta name="keywords" content="Linux, Python, Tasks">
	<meta name="author" content="Jiří Němec">
	<link rel="stylesheet" href="/templates/reset.css">
	<link rel="stylesheet" href="/templates/styles.css">
	<link rel="shortcut icon" href="data:image/x-icon;," type="image/x-icon"> 
</head>
<body class="container">
<header>
<div class="title">
<a href="/">Aktuální úkoly</a>
<a href="/?tasks=finished">Dokončené úkoly</a>
<a href="/?tasks=expired">Prošlé úkoly</a>
<a href="/new_task">Nový úkol</a>
</div>
</header>

<main>
<div id="middle">
${self.body()}
</div><!-- #middle-->
</main>
<footer>Jiří Němec, 2022</footer>
</body>
</html>
