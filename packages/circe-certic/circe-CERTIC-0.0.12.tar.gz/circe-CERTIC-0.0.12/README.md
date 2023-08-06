# Circe

API web pour la transformation de documents.

Dépôt: [pdn-certic/circe](https://git.unicaen.fr/pdn-certic/circe)

## Table des matières

- [Description du service](#description-du-service)
	- [Format d'échange](#format-déchange)
		- [Structure du fichier job.json](#structure-du-fichier-jobjson)
	- [Web API](#web-api)
		- [GET /transformations/](#get-transformations)
		- [POST /job/](#post-job)
		- [GET /job/[UUID]](#get-jobuuid)
	- [Notification](#notification)
- [Serveur de référence](#serveur-de-référence)
	- [Pré-requis](#pré-requis)
	- [Installation et démarrage du service](#installation-et-démarrage-du-service)
	- [Variables d'environnement et configuration par défaut:](#variables-denvironnement-et-configuration-par-défaut)
	- [Utilisation en ligne de commande](#utilisation-en-ligne-de-commande)
	- [Ajouter des transformations](#ajouter-des-transformations)
- [Clients de référence](#clients-de-référence)
- [Tests](#tests)


## Description du service

### Format d'échange

Le client fournit au serveur une tâche (un _job_) à effectuer sous forme d'une archive tar *gzippée* (*.tar.gz) contenant a minima **à sa racine**:

- les fichiers à transformer
- un fichier nommé job.json décrivant les transformations souhaitées sur ces fichiers

On peut également ajouter des fichiers utiles à la conversion, tel que des feuilles de styles ou des fichiers de fontes par exemple.

#### Structure du fichier job.json

Est placé dans l'archive un fichier ```job.json``` décrivant l'ensemble des opérations à faire sur les fichiers.

Un cas minimal:

    {
        "transformations": [
            {"name": "html2pdf"}
        ]
    }

... décrit une transformation unique à effectuer sur les documents fournis dans l'archive, sans options.

La seule clef obligatoire pour le job est la clef ```transformations```, contenant la liste des transformations à faire. La seule clef obligatoire pour la transformation est la clef ```name```, contenant le nom de la transformation.

Un cas plus complet:

    {
        "transformations": [
            {"name": "html2pdf",
             "options": {"compression": 1}},
            {"name": "donothing",}
        ],
        "notify_hook": "http://www.domain.tld/notify-me/"
    }

... décrit 2 transformations consécutives, dont une avec une option, ainsi qu'une URL de notification (```notify_hook```) qui sera appelée par le serveur à la fin du _job_.

Les résultats des transformations sont également fournis par le serveur sous forme d'archive tar _gzippée_.

### Web API

#### GET /transformations/

Retourne une liste JSON des transformations supportées. Exemple:

    ["html2pdf","donothing", "docx2markdown"]

#### POST /job/

Attend dans le corps de la requête une archive de _job_ correctement formée. 

Retourne un [UUID version 4](https://fr.wikipedia.org/wiki/Universal_Unique_Identifier#Version_4 "UUID v4") sous forme de chaîne de caractères. L'UUID retourné est l'identifiant du _job_, à conserver pour les prochaines requêtes.

Si l'option ```block=1``` est passée dans l'URL (```/job/?block=1```), alors le comportement est différent: ce n'est pas l'UUID qui sera retourné mais directement le résultat des transformations, de manière identique à ```GET /job/[UUID]```.

En fonction de la configuration du serveur, la soumission d'un nouveau _job_ peut nécessiter une authentification. Dans ce cas, l'entête HTTP Authorization doit être renseigné sous la forme suivante:

    Authorization: [UUID de l'application] [signature HMAC de l'archive]

_Voir le source du client Python pour un exemple de signature HMAC._

#### GET /job/[UUID]

Récupère l'archive contenant les fichiers transformés par le serveur. Exemple:

    curl http://www.domain.tl/job/55d87fe0-3924-423a-893d-23aa45614ad9 

Un statut HTTP 200 est retourné et l'archive avec les documents transformés est contenue dans le corps de la réponse.

Au cas où le _job_ ne serait pas terminé, un statut HTTP 202 est retourné.

Au cas où l'UUID fait référence à un _job_ n'existant pas sur ce serveur, un statut HTTP 404 est retourné.

En fonction de la configuration du serveur, la récupération d'un _job_ terminé peut nécessiter une authentification. Dans ce cas, l'entête HTTP Authorization doit être renseigné sous la forme suivante:

    Authorization: [UUID de l'application] [signature HMAC de l'UUID du job]

_Voir le source du client Python pour un exemple de signature HMAC._

### Notification

Dans le cas où une URL a été fournie dans la clef ```notify_hook``` du fichier job.json, le serveur effectue une requête POST sur cette URL avec l'UUID du _job_ en corps de requête.

## Serveur de référence

Un serveur de référence est implémenté en Python. Deux composants sont fournis:

- un serveur HTTP exposant l'interface HTTP du service
- un pool de workers effectivement chargés des transformations

### Pré-requis

- Python >= 3.6

### Installation et démarrage du service

Création et activation d'un venv:

    cd web
    python3 -m venv myvenv
    . ./myvenv/bin/activate

Installation de Circe:

    pip install circe-CERTIC

Démarrage du service HTTP:

    circe serve

Démarrage des workers:

    circe start-workers

Démarrage simultané du service HTTP et des workers:

    circe run

### Variables d'environnement et configuration par défaut:

- ```CIRCE_HOST``` (```0.0.0.0```)
- ```CIRCE_PORT``` (```8000```)
- ```CIRCE_DEBUG``` (```False```)
- ```CIRCE_WORKERS``` (```number of CPUs```)
- ```CIRCE_WORKING_DIR``` (```$HOME/.circe/```)
- ```CIRCE_ENABLE_WEB_UI``` (```False```)
- ```CIRCE_WEB_UI_CRYPT_KEY``` (```"you should really change this"```)
- ```CIRCE_WEB_UI_REMOVE_USER_FILES_DELAY``` (```7200```)
- ```CIRCE_USE_AUTH``` (```True```)
- ```CIRCE_TRANSFORMATIONS_MODULE``` (```None```)

### Utilisation en ligne de commande

Un certain nombre de commande sont disponibles dans circe.py. Pour les afficher:

    (venv) ➜  src ✗ circe --help
    usage: circe [-h]
                 {serve,start-workers,make-api-access,remove-api-access,list-api-access,list-transformations,run}
                 ...
    
    positional arguments:
      {serve,start-workers,make-api-access,remove-api-access,list-api-access,list-transformations,run}
        serve               Start Circe HTTP server
        start-workers       Start job workers
        make-api-access     Create new app uuid / secret couple for api access.
        remove-api-access   Remove access to the API
        list-api-access     List all access tokens to the API
        list-transformations
        run                 Start both HTTP server and job workers
    
    optional arguments:
      -h, --help            show this help message and exit

Il est possible d'obtenir de l'aide sur chaque commande:

    (venv) ➜  src ✗ circe serve --help
    usage: circe serve [-h] [--host HOST] [-p PORT] [-w WORKERS] [-d] [-a]

    Start Circe HTTP server

    optional arguments:
      -h, --help            show this help message and exit
      --host HOST           '127.0.0.1'
      -p PORT, --port PORT  8000
      -w WORKERS, --workers WORKERS
                            1
      -d, --debug           False
      -a, --access-log      False


### Ajouter des transformations

La variable d'environnement CIRCE_TRANSFORMATIONS_MODULE contient le nom du module Python contenant les transformations
que vous souhaitez rendre disponible dans le service.

Une transformation est un Python callable (fonction ou classe) prenant en argument le dossier de travail du job, une instance de logging.Logger ainsi qu'un dictionnaire d'options (facultatif). Exemple minimal d'une transformation:

    def ne_fait_rien(working_dir: str, logger: logging.Logger, options: dict = None):
        pass  # ajouter ici le code transformant les documents

L'instance de logging.Logger peut prendre ee paramêtre une chaîne ou un dictionnaire:
	
	logger.info('message de log")
	logger.info({"message": "message de log", "autre info utile": 42}

Les transformations peuvent fournir une description de leur fonctionnement ainsi:

	ne_fait_rien.description = {
		"label": "Ne fait rien",
		"help": "Ne fait rien absolument rien. Utile pour tester l'API.",
		"options": [],  # aucune option pour cette transformation
	}

Ces descriptions sont utiles pour les clients.

Des exemples de transformations sont disponibles dans ce dépôt: https://git.unicaen.fr/certic/circe-transformations

## Clients de référence

Une librairie cliente de référence en python est proposée.

Installation:
    
    pip install circe-client-CERTIC

Utilisation:

    from circe_client import Client
    
    # Les paramètres peuvent être ignorés si les variables
    # d'environnement CIRCE_ENDPOINT, CIRCE_SECRET et CIRCE_APP_UUID
    # existent.    
    client = Client(
        api_endpoint="http://host.tld/,
        secret_key="notsosecret",
        application_uuid="786d1b69a6034eb89178fed2a195a1ed",
    )
    
    if "html2pdf" in client.available_transformations():
        job = client.new_job()
        job.add_file("index.html")
        # on peut adjoindre tout fichier utile à la transformation
        job.add_file("style.css")
        job.add_transformation("html2pdf")
        # en option, une URL qui recevra une notification en POST
        # à la fin du job:
        # job.set_notify_hook("https://acme.tld/notify-me/")
    
        # wait=True pour un appel synchrone à l'API,
        # à privilégier pour les jobs courts et/ou les
        # transformations rapides:
        client.send(job, wait=True)
        
        # pour un appel asynchrone, retournant un UUID de job,
        # à privilégier pour les jobs longs (transformations lentes
        # et/ou nombreux fichiers):
        #
        # client.send(job)
        # print(job.uuid)
        # 
        # On peut ensuite tenter une récupération du job avec
        # un timeout:
        #
        # client.poll(job, timeout=60)
    
        # liste les fichiers disponible dans l'archive de résultat
        # sous la forme d'un tuple (nom de fichier, pointeur vers le fichier)
        for file_name, file_handle in job.result.files:
            print(file_name)


Une [librairie cliente équialente en Java](https://git.unicaen.fr/certic/circe-java-client) est disponible
ainsi qu'une [librairie minimale en PHP](https://git.unicaen.fr/certic/circe-php-client) et un [outil en ligne de commande implémenté en Go](https://git.unicaen.fr/mickael.desfrenes/circe-helper).

## Tests

Un ensemble de tests exécutables par Pytest sont disponibles dans le fichier ```test.py```.
