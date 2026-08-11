import logging

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)

# Premier fichier logging
file_handler = logging.FileHandler("utils/api.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Deuxième fichier d audit
audit = logging.getLogger("audit")
file_handler1 = logging.FileHandler("utils/audit.log", encoding="utf-8")
file_handler1.setLevel(logging.INFO)
file_handler1.setFormatter(formatter)

logger.addHandler(file_handler)
audit.addHandler(file_handler1)
