from configlib import BaseConfig
import rethinkdb as r

class RethinkConfig(object):
    host: str
    port: int
    database: str


class AuthMethod(object):
    username: str
    password: str


class ServerConfig(BaseConfig):
    database: RethinkConfig
    timezone: str

    @property
    def r_timezone(self):
        return r.make_timezone(self.timezone)

    auth: AuthMethod
    serverid: int


config: ServerConfig = ServerConfig.get_instance()

__all__ = ['config', 'ServerConfig', 'RethinkConfig', 'AuthMethod']
