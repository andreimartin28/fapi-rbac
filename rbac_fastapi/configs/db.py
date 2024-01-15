from configs.base import ENVIRONMENT
from configs.database import DB_CONFIG
from libraries.database import Database

db: object = Database(DB_CONFIG[ENVIRONMENT])