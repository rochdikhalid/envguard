from envguard.schema import Schema

class Config(Schema):
    PORT: int
    DB_URL: str
    DEBUG: bool = False

print(Config.__fields__)
