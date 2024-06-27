# archivo de configuracion. Por ahora es simple, pero es convencion

class Config():
    SECRET_KEY = 'secretkey'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'inventario'
    MYSQL_CURSORCLASS = 'DictCursor'

config = {
    'development': DevelopmentConfig
}