from prettyconf import config

MAX_OVERFLOW = config("MAX_OVERFLOW", default=20)
POOL_SIZE = config("POOL_SIZE", default=10)
SILENT_ENVIROMENTS = config("SILENT_ENVIROMENTS", default=("staging", "prod", "production"))

SQLALCHEMY_DATABASE_URL = config(
    "SQLALCHEMY_DATABASE_URL",
    default="postgresql://postgres:@localhost:5432/par_de_jarro_test",
)


JWT_REFRESH_SECRET_KEY = config("JWT_REFRESH_SECRET_KEY", default="refresh")
JWT_SECRET_KEY = config("JWT_SECRET_KEY", default="secret")
AWS_BUCKET_NAME = config("AWS_BUCKET_NAME", default="par-de-jarro")
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="par-de-jarro")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default=None)
GOOGLE_API_ADDRESS_KEY = config("GOOGLE_API_ADDRESS_KEY", default=None)
API_TOKEN_AUTH_PASSWORD = config("API_TOKEN_AUTH_PASSWORD", default="par-de-jarro")
