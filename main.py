from logging_config import setup_logging

setup_logging()
import json
import time
import logging
from datetime import datetime, timezone
from pathlib import Path

from monitor.browser_check import verify_website_browser
from monitor.http_check import check_website_http
from monitor.notifier import send_email_alert
from monitor.state_manager import update_state
from monitor.utils import internet_check


def load_config(path="data/config.json"):
    path = Path(path)
    try:

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        logging.exception("file not found: %s", e)  # Lazy Evaluation instead of f" ".
        raise
    except json.JSONDecodeError:
        logging.exception(
            "File is invalid"
        )  # Since logging.exception captures the exception info by default
        raise


def monitor_cycle(config):
    for url in config["sites"]:
        try:
            logging.info(f"[{datetime.now(timezone.utc)}] checking {url}")

            http_result = check_website_http(url)

            if http_result["status"] == "UP":
                final_status = "UP"
                error = None

            else:
                browser_result = verify_website_browser(url)
                final_status = browser_result["status"]
                error = browser_result["error"]

            state_result = update_state(
                url,
                final_status,
            )
            if state_result["changed"]:
                subject = f"[ALERT] website {final_status} - {url}"
                body = f"""
        Website: {url}
        Previous status: {state_result['previous_status']}
        Current status: {final_status}
        Time (UTC): {datetime.now(timezone.utc).isoformat()}
        Error: {error}
                        """.strip()

                send_email_alert(
                    subject=subject,
                    body=body,
                )

                logging.info(f"[ALERT] website {final_status} -{url}")

            else:
                if state_result["previous_status"] is None:
                    logging.info(f"first time seeing this site {url} ({final_status})")
                else:
                    logging.info(f"No status change for {url} ({final_status})")

        except Exception:
            logging.exception(f"monitor for {url} crash")


def main():

    try:
        internet_check()
    except OSError:
        logging.exception("connection problem, exiting program")
        raise SystemExit(1)  # without raise it won't work
    try:
        config = load_config()
        interval = config.get("interval_second", 60)
    except Exception:
        logging.exception("error in input data file, exiting program")
        raise SystemExit(1)

    logging.info("Uptime monitor started")
    try:

        while True:

            cycle_start = time.time()

            monitor_cycle(config)

            elapsed = time.time() - cycle_start

            sleep_time = max(0, interval - elapsed)
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        logging.info("Monitor stopped by user")
    except Exception:
        logging.exception("Monitor loop crashed")


if __name__ == "__main__":
    try:
        main()

    except Exception:
        logging.exception("main stop")
