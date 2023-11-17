import logging as l


l.basicConfig(filename='logs/data.log',
              level=l.INFO,
              format='[%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s',
              datefmt='%Y-%m-%d %H:%M:%S')


def get_logger(module_name: str):
    return l.getLogger(module_name)
