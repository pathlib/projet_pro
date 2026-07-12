def guis() -> str:
    return """
    <!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Mon API CRUD</title>

  <style>
    body{
      font-family: Arial, sans-serif;
      background:#0f172a;
      color:white;
      margin:0;
      padding:0;
    }

    header{
      background:#1e293b;
      padding:30px;
      text-align:center;
    }

    h1{
      color:#38bdf8;
      font-size:40px;
    }

    .container{
      padding:40px;
      max-width:900px;
      margin:auto;
    }

    .card{
      background:#1e293b;
      padding:25px;
      border-radius:15px;
      margin-bottom:20px;
      box-shadow:0 0 10px rgba(0,0,0,0.3);
    }

    h2{
      color:#38bdf8;
    }

    code{
      background:black;
      padding:4px 8px;
      border-radius:5px;
      color:#4ade80;
    }

    footer{
      text-align:center;
      padding:20px;
      color:#94a3b8;
    }
  </style>
</head>

<body>

  <header>
    <h1>Mon API CRUD  </h1>
  </header>

  <div class="container">

    <div class="card">
      <h2>Fonctionnalités</h2>
      <ul>
        <li>Création de données</li>
        <li>Lecture des données</li>
        <li>Mise à jour</li>
        <li>Suppression</li>
        <li>Authentification JWT en cour </li>
        <li>Base de données sécurisée en cour </li>
      </ul>
    </div>

    <div class="card">
      <h2>Exemple de route API</h2>

      <p>GET utilisateurs :</p>
      <code>GET /donnees </code>
      <h3>affiche toute les donnee</h3>

      <br><br>

      <p>Créer un utilisateur :</p>
      <code>POST /donnee/donnee_add</code>

      <br><br>

      <p>Supprimer un utilisateur :</p>
      <code>DELETE /donnee/id/</code>
    </div>

    <div class="card">
      <h2>Technologies</h2>

      <ul>
        <li>sqlite</li>
        <li>logger</li>
      </ul>
    </div>

  </div>

  <footer>
    © 2026 - Mon API CRUD
  </footer>

</body>
</html>
    """


def gui2() -> str:
    return """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Mon API CRUD V2</title>

  <style>
    body{
      font-family: Arial, sans-serif;
      background:#0f172a;
      color:white;
      margin:0;
      padding:0;
    }

    header{
      background: linear-gradient(90deg,#1e293b,#0f172a);
      padding:30px;
      text-align:center;
      border-bottom:3px solid #38bdf8;
      position:relative;
    }

    h1{
      color:#38bdf8;
      font-size:40px;
      margin:0;
    }

    /* 🔥 BADGE V2 ULTRA VISIBLE */
    .v2-badge{
      position:absolute;
      top:15px;
      right:15px;
      background:#38bdf8;
      color:#0f172a;
      padding:8px 14px;
      border-radius:20px;
      font-weight:bold;
      font-size:14px;
      box-shadow:0 0 15px #38bdf8;
    }

    .container{
      padding:40px;
      max-width:900px;
      margin:auto;
    }

    .card{
      background:#1e293b;
      padding:25px;
      border-radius:15px;
      margin-bottom:20px;
      box-shadow:0 0 10px rgba(0,0,0,0.3);
      border:1px solid rgba(56,189,248,0.15);
    }

    h2{
      color:#38bdf8;
    }

    code{
      background:black;
      padding:4px 8px;
      border-radius:5px;
      color:#4ade80;
    }

    footer{
      text-align:center;
      padding:20px;
      color:#94a3b8;
    }

    /* petit effet V2 global */
    .card:hover{
      transform:scale(1.01);
      transition:0.2s;
      border-color:#38bdf8;
    }
  </style>
</head>

<body>

  <header>
    <div class="v2-badge">V2 🚀</div>
    <h1>Mon API CRUD</h1>
  </header>

  <div class="container">

    <div class="card">
      <h2>Fonctionnalités</h2>
      <ul>
        <li>Création de données</li>
        <li>Lecture des données</li>
        <li>Mise à jour</li>
        <li>Suppression</li>
        <li>Authentification JWT en cours</li>
        <li>Base de données sécurisée en cours</li>
      </ul>
    </div>

    <div class="card">
      <h2>Exemple de route API</h2>

      <p>GET utilisateurs :</p>
      <code>GET /donnees</code>

      <h3>affiche toutes les données</h3>

      <br>

      <p>Créer un utilisateur :</p>
      <code>POST /donnee/donnee_add</code>

      <br><br>

      <p>Supprimer un utilisateur :</p>
      <code>DELETE /donnee/id/</code>
    </div>

    <div class="card">
      <h2>Technologies</h2>
      <ul>
        <li>SQLite</li>
        <li>Logger</li>
      </ul>
    </div>

  </div>

  <footer>
    © 2026 - Mon API CRUD - Version 2
  </footer>

</body>
</html> """
