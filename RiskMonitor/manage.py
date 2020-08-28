from config import config
from app import create_app


if __name__ == '__main__':
    env = 'default'
    host = config[env].HOST
    port = config[env].PORT
    app = create_app(env)

    app.run(host= host, port= port)