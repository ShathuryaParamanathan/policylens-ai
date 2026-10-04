
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from .url_security import validate_url

import re

POLICY_KEYWORDS = {
    "privacy_policy": [
        "privacy",
        "privacy policy",
        "privacy-policy",
        "privacy_policy"
    ],

    "terms": [
        "terms",
        "terms of service",
        "terms and conditions",
        "terms-of-service",
        "terms-and-conditions"
    ],

    "cookie_policy": [
        "cookie",
        "cookies",
        "cookie policy",
        "cookie-policy"
    ],

    "refund_policy": [
        "refund",
        "refund policy",
        "refund-policy",
        "return policy",
        "returns"
    ],

    "security_policy": [
        "security",
        "security policy",
        "security-policy"
    ]
}

MAX_HTML_SIZE = 5 * 1024 * 1024       # 5 MB
MAX_TEXT_LENGTH = 500_000             # 500k characters
MAX_LINKS = 100
MAX_POLICY_LINKS = 20
MAX_REDIRECTS = 5
PAGE_TIMEOUT_MS = 30_000

def extract_links(page_url: str, html: str):

    soup = BeautifulSoup(html, "html.parser")

    links = []
    seen_urls = set()

    for anchor in soup.find_all("a", href=True):

        href = anchor["href"].strip()

        link_text = anchor.get_text(" ", strip=True)

        # Ignore non-web links
        if href.startswith(("mailto:", "tel:", "javascript:")):
            continue

        # Convert relative URL to absolute URL
        absolute_url = urljoin(page_url, href)

        # Normalize URL
        normalized_url = normalize_url(absolute_url)

        # Only keep links from the same website
        if not is_same_domain(page_url, normalized_url):
            continue

        # Avoid duplicates
        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)

        links.append({
            "url": normalized_url,
            "text": link_text
        })

    return links

def validate_request_url(request_url: str) -> str:
    """
    Validate every URL requested by Playwright.

    This protects against:
    - unsafe redirects
    - internal network requests
    - private IP addresses
    - localhost access
    """

    return validate_url(request_url)

def crawl_page(url: str):

    # -----------------------------------------
    # 1. Validate initial URL
    # -----------------------------------------

    safe_url = validate_url(
        url
    )

    # -----------------------------------------
    # 2. Launch browser
    # -----------------------------------------

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        # -------------------------------------
        # 3. Intercept browser requests
        # -------------------------------------

        page.route(
            "**/*",
            handle_route
        )

        # -------------------------------------
        # 4. Navigate
        # -------------------------------------

        page.goto(
            safe_url,
            wait_until="domcontentloaded",
            timeout=PAGE_TIMEOUT_MS
        )

        title = page.title()

        html = page.content()

        # -------------------------------------
        # 5. HTML size protection
        # -------------------------------------

        html_size = len(
            html.encode("utf-8")
        )

        if html_size > MAX_HTML_SIZE:

            browser.close()

            raise ValueError(
                "Page HTML exceeds the maximum "
                "allowed size."
            )

        # -------------------------------------
        # 6. Extract rendered text
        # -------------------------------------

        text = page.locator(
            "body"
        ).inner_text(
            timeout=10000
        )

        # -------------------------------------
        # 7. Text size protection
        # -------------------------------------

        if len(text) > MAX_TEXT_LENGTH:

            text = text[
                :MAX_TEXT_LENGTH
            ]

        browser.close()

    # -----------------------------------------
    # 8. Clean content
    # -----------------------------------------

    cleaned_text = clean_content(
        html
    )

    # -----------------------------------------
    # 9. Normalize text
    # -----------------------------------------

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n\s*\n+",
        "\n\n",
        text
    )

    text = text.strip()

    # -----------------------------------------
    # 10. Extract links
    # -----------------------------------------

    links = extract_links(
        safe_url,
        html
    )

    links = links[
        :MAX_LINKS
    ]

    # -----------------------------------------
    # 11. Find policy links
    # -----------------------------------------

    policy_links = find_policy_links(
        links
    )

    policy_links = policy_links[
        :MAX_POLICY_LINKS
    ]

    # -----------------------------------------
    # 12. Extract headings
    # -----------------------------------------

    headings = extract_headings(
        html
    )

    return {
        "url": safe_url,
        "title": title,
        "html": html,
        "text": text,
        "cleaned_text": cleaned_text,
        "links": links,
        "headings": headings,
        "policy_links": policy_links,
    }

def normalize_url(url: str):
    parsed = urlparse(url)

    normalized = parsed._replace(fragment="")

    return normalized.geturl().rstrip("/")

def is_same_domain(base_url: str, target_url: str):
    base_domain = urlparse(base_url).netloc.lower()
    target_domain = urlparse(target_url).netloc.lower()

    return base_domain == target_domain

def find_policy_links(links):

    policy_links = {}

    for link in links:

        url = link["url"].lower()
        text = link["text"].lower()

        combined = f"{text} {url}"

        for policy_type, keywords in POLICY_KEYWORDS.items():

            for keyword in keywords:

                if keyword in combined:

                    if policy_type not in policy_links:
                        policy_links[policy_type] = link["url"]

                    break

    return policy_links

def extract_headings(html: str):

    soup = BeautifulSoup(html, "html.parser")

    headings = []

    for heading in soup.find_all(["h1", "h2", "h3"]):

        text = heading.get_text(" ", strip=True)

        if text:
            headings.append({
                "level": heading.name,
                "text": text
            })

    return headings

def crawl_policy_pages(policy_links):

    documents = []

    for policy_type, url in policy_links.items():

        try:

            document = crawl_page(url)

            document["document_type"] = policy_type

            documents.append(document)

        except Exception as e:

            print(f"Failed to crawl {url}: {e}")

    return documents

def clean_content(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # Remove elements that are not useful for policy analysis
    for element in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "template",
        "nav",
        "header",
        "footer",
        "form"
    ]):
        element.decompose()

    text = soup.get_text(
        separator="\n",
        strip=True
    )

    # Remove PGP public key blocks
    text = re.sub(
        r"-----BEGIN PGP PUBLIC KEY BLOCK-----.*?"
        r"-----END PGP PUBLIC KEY BLOCK-----",
        "",
        text,
        flags=re.DOTALL
    )

    # Normalize spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def handle_route(route):

    request = route.request

    if request.resource_type in BLOCKED_RESOURCE_TYPES:
        route.abort()
        return

    try:

        validate_request_url(
            request.url
        )

        route.continue_()

    except ValueError as error:

        print(
            "Blocked unsafe request:",
            request.url
        )

        print(
            "Reason:",
            error
        )

        route.abort()       
