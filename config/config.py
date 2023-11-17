import configparser as cp

config = cp.ConfigParser()
config.read('config/config.ini')

base_url = config['API']['base_url']
endpoint = config['API']['end_point']
