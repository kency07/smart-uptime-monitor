import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict

STATE_FILE = Path("data/state.json")


def load_state() -> Dict:
    if not STATE_FILE.exists():
        return {}
    try:
        with STATE_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        logging.warning(f"{STATE_FILE} is corrupted, backing it up")
        try:  # Safe to run multiple times: backups are timestamped,
            # so existing *.corrupted.json files won't conflict
            backup = STATE_FILE.with_name(
                f"{STATE_FILE.stem}.{int(datetime.now(timezone.utc).timestamp())}.corrupted.json"
            )
            STATE_FILE.rename(backup)

        except Exception as exc:
            logging.exception(f"Failed to rename corrupted  {STATE_FILE}")
            return {}
    except Exception as e:
        logging.exception(f"Failed to load the file{STATE_FILE}")
        return {}


def save_status(state: Dict) -> None:
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with STATE_FILE.open("w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        logging.exception("Failed to save state")


def update_state(url: str, current_status: str) -> Dict:
    """
    Update state and detect status change.
    Returns:
        {
            changed: bool,
            previous_status: str | None
        }
    """
    state = load_state()
    now = datetime.now(timezone.utc).isoformat()

    previous = state.get(url)

    # 1. Determine if status changed
    # If previous is None (first run), we treat changed as False to avoid initial spam
    changed = False
    previous_status_val = None

    if previous:
        previous_status_val = previous.get("status")
        if previous_status_val != current_status:
            changed = True

    if not previous:
        # First time seeing this site
        state[url] = {
            "status": current_status,
            "last_checked": now,
            "last_changed": now,
        }

    else:  
        state[url]["last_checked"] = now
        if changed:
            state[url]["status"] = current_status
            state[url]["last_changed"] = now
    save_status(state)
    return {
        "changed": changed,
        "previous_status": previous_status_val,
    }
