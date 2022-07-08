<!DOCTYPE html>
<html lang="cs">
<head>
	<title>EasyTasker</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="content-type" content="text/html; charset=UTF-8">
	<meta name="description" content="Small tasker for Deso.">
	<meta name="keywords" content="Linux, Python, Tasks">
	<meta name="author" content="Jiří Němec">
<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
}

/* Style the header */
.header {
  background-color: #f1f1f1;
  padding: 10px;
  text-align: center;
}

/* Style the top navigation bar */
.topnav {
  overflow: hidden;
  background-color: #333;
}

/* Style the topnav links */
.topnav a {
  float: left;
  display: block;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

/* Change color on hover */
.topnav a:hover {
  background-color: #ddd;
  color: black;
}

/* Create three equal tasks that floats next to each other */
/* Create three equal columns that float next to each other */
.task {
  float: left;
  width: 33.33%;
}

/* Clear floats after the columns */
.column:after {
  content: "";
  display: table;
  clear: both;
}

/* Responsive layout - makes the three columns stack on top of each other instead of next to each other on smaller screens (600px wide or less) */
@media screen and (max-width: 600px) {
  .task {
    width: 100%;
  }
}

</style>
</head>
<body>

<div class="header">
  <h2>EasyTasker</h2>
  <p>Organize your tasks easy!</p>
</div>

<div class="topnav">
	<a href="/">Aktuální úkoly</a>
	<a href="/?tasks=finished">Dokončené úkoly</a>
	<a href="/?tasks=expired">Prošlé úkoly</a>
	<a href="/new_task">Nový úkol</a>
	<a href="/logout">Odhlásit se</a>
</div>

<div class="column">
	${self.body()}
</div>

</body>
</html>
