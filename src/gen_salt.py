import os
import re
from typing import Optional
from logger import logger_config

def gen_salt(env_path_param: Optional[str] = None) -> None:
    logger = logger_config("gen_salt")

    # Get env_path
    if env_path_param:
        if os.path.isdir(env_path_param):
            env_path = os.path.normpath(os.path.join(env_path_param, ".env"))
        else:
            env_path = env_path_param
    else:
        env_path = "../.env"

    # Creating aux function
    def create_salt(env_path: str):
        logger.info("Creating salt...")
        salt = os.urandom(16) # Create 16-byte salt

        # Save it to .env file
        with open(env_path, "w") as file:
            file.write(f"SALT={salt}")
        
        logger.info("Salt created successfully")

    # Checking if .env file exists
    if os.path.exists(env_path):
        with open(env_path, mode="r") as file:
            data = file.read()
        
        # Checking if env variable has already been set
        if re.search("SALT=.*$", data):
            logger.info("Salt already created")
        else:
            create_salt(env_path)
    else:
        create_salt(env_path)
        