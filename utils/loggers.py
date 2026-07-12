import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s - %(process)d",
    handlers=[logging.FileHandler("utils/api.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)






logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s - %(process)d",
    handlers=[logging.FileHandler("utils/audit.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)