import sys

if 'LOCAL' in sys.argv:
    TOKEN = '000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    LOCAL = True
else:
    TOKEN = '000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    LOCAL = False
    WEBHOOK_HOST = '11.222.33.444'
    WEBHOOK_PORT = 8443 # 443, 80, 88 или 8443 (порт должен быть открыт!)
    WEBHOOK_LISTEN = '11.222.33.444'  # На некоторых серверах придется указывать такой же IP, что и выше

    WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
    WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

    WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
    WEBHOOK_URL_PATH = "/{}/".format(TOKEN)
