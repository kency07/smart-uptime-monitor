import logging
import socket


def internet_check():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3).close()
        logging.info("you are online, now program will procceed")
        return True
    except OSError :
        
            logging.exception("Connection failed")
            raise
