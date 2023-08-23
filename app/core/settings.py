from prettyconf import config

MAX_OVERFLOW = config("MAX_OVERFLOW", default=20)
POOL_SIZE = config("POOL_SIZE", default=10)
SILENT_ENVIROMENTS = config("SILENT_ENVIROMENTS", default=("staging", "prod", "production"))

SQLALCHEMY_DATABASE_URL = config(
    "SQLALCHEMY_DATABASE_URL",
    default="postgresql://postgres:@localhost:5432/clicampo_test",
)
