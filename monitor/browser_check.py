from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
    Error,
)
from typing import Dict, Optional

ERROR_KEYWORDS = [
    "bad request",
    "unauthorized",
    "forbidden",
    "not found",
    "error",
    "internal server error",
    "bad gateway",
    "service unavailable",
    "gateway timeout",
    "can't be reached",
    "connection reset",
    "dns_probe_finished",
    "site cannot be reached",
    "address not found",
    "access denied",
]


def verify_website_browser(url: str, timeout: int = 20_000) -> Dict[str, Optional[str]]:
    """
    Verify website availability using a real browser.
    Returns final UP / DOWN status.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True, args=["--ignore-certificate-errors"]
            )
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()
            try:

                page.goto(url, timeout=timeout, wait_until="domcontentloaded")

                # Minimal verification
                body_text = (page.text_content("body") or "").lower()
                title = (page.title() or "").lower()
                if any(k in body_text or k in title for k in ERROR_KEYWORDS):
                    
                    return {
                        "status": "DOWN",
                        "error": "Error keywords detected in page",
                    }

                if len(body_text.strip()) < 50:

                    return {
                        "status": "DOWN",
                        "error": "Page loaded but  content is too small",
                    }
                return {"status": "UP", "error": None}
            finally:
                page.close()
                context.close()
                browser.close()
    except PlaywrightTimeoutError:
        return {"status": "DOWN", "error": "Browser navigation timeout"}

    except Error as e:
        return {"status": "DOWN", "error": f"Playwright network error: {e}"}

    except Exception as exc:
        return {"status": "DOWN", "error": str(exc)}
