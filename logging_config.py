import logging
import time         #(instead of datetime) to a computer, a date is just a very large amount of time("Unix Time" Legacy).


def setup_logging():
    if logging.getLogger().hasHandlers():
        return
    # Set the formatter to use UTC/GMT move it before basicConfig for reliable UTC timestamp conversion
    logging.Formatter.converter = time.gmtime    #function object.(gmtime) 

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%SZ',  # lowercase m , d is standard for month and day
                                       # uppercase M for minutes for standard timestamps 
        handlers=[
            logging.FileHandler("data/alerts.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )