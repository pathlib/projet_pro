def guis()-> str:
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
