# Remote logging
Securely store your log files on a remote logger, all with templates included!

## Server setup
First set up a rethinkdb
Then install the server with
```bash
pip install https://github.com/romangraef/remotelogging/archive/master.zip#egg=remotelogging[server]
```
is a good start, but you would be better if you would host this using some sort of WSGI application.
## Server config
in the current runtime directory, create a folder called `config`. in that folder put a file called `server_config.json`
the content should be like it follows
```json
{
  "database": {
    "host": "localhost",
    "database": "logging",
    "port": 28015
  },
  "auth": {
    "password": "admin",
    "username": "admin"
  },
  "timezone": "01:00",
  "secret": "randomly generated, long string",
  "serverid": 1
}
```
## Server start
```bash
python -m remotelogging.server
```
## Template setup
Just go to the webinterface of your WSGI application (or localhost:5000) and add templates as you like.
Template texts have variables with `{varname}` as subtition parameters.

When you are already there, you should generate a token for each of your applications. Give it a meaningful name.

On the same website you can view your log entries.

## Client setup.

Install `https://github.com/romangraef/remotelogging/archive/master.zip` via pip and just import `RemoteLogger` from it. all methods from it are coroutines. it is recommend, tho not required to call `.verify` on it first to see if you are logged in correctly.



