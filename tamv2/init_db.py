"""À exécuter UNE SEULE FOIS depuis une machine de confiance avec les variables de production."""
import os
from app import initialize_database
if not os.getenv('DATABASE_URL') or not os.getenv('ADMIN_EMAIL') or not os.getenv('ADMIN_PASSWORD') or not os.getenv('SECRET_KEY'):
    raise SystemExit('Variables DATABASE_URL, ADMIN_EMAIL, ADMIN_PASSWORD et SECRET_KEY requises')
initialize_database()
print('Base initialisée et compte administrateur créé si absent.')
