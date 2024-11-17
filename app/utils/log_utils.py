import logging
from logging import Logger

 
def init_logger() -> Logger:

    # ロガーの設定
    logger = logging.getLogger("Kondatemaker")
    logger.setLevel(logging.DEBUG)
 
    # コンソールハンドラの設定
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
 
    # ファイルハンドラの設定
    file_handler = logging.FileHandler('./logs/server.log')
    file_handler.setLevel(logging.WARN)

    # フォーマッタの設定
    formatter = logging.Formatter('%(asctime)s,%(levelname)s,%(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
 
    # ハンドラをロガーに追加
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
 
    return logger

logger = init_logger()