"""
Constants that can be changed for mroe or less data
retrieved from the OFF API
"""
# Number of categories to be extracted from API, Default is 3
NBR_CAT = 3

# Number of product per category to be extracted from API, Default is 20
NBR_PROD = 10

# Number of results per page in the results page
NBR_RESULTS_PER_PAGE = 8

# ERROR: user not logged_in
NOT_LOGGED_IN = ("Vous devez vous identifier"
                 " pour pouvoir effectuer cette action")

# ERROR: Invalid credentials
INVALID_CREDENTIALS = (
    "Une erreur s'est glissée dans "
    "votre nom ou votre mot de passe, veuillez reessayer")

# ERROR: no match for searched product in the DB
NO_PROD_FOUND = (
    "Désolé, aucun produit de notre base de données ne correspond"
    "à vorte recherche\nessayez par exemple 'Nutella',"
    " ou 'produit à l'abricot")

# user_message: log out is ok
LOG_OUT_OK = "Votre déconnexion a bien été prise en compte"

# user_message: log in is ok
LOG_IN_OK = "Vous êtes désormais identifié"

# time between each selenium test
WAIT_TIME = 0
