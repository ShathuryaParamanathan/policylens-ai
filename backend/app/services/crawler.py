
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
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

def crawl_page(url: str):
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000
        )

        title = page.title()
        html = page.content()

        # Extract visible rendered text from the page
        text = page.locator("body").inner_text(timeout=10000)

        browser.close()
        cleaned_text = clean_content(html)



    # Normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    text = text.strip()
    links = extract_links(url, html)

    policy_links = find_policy_links(links)
    headings = extract_headings(html)

    return {
        "url": url,
        "title": title,
        "html": html,
        "text": text,
        "cleaned_text": cleaned_text,
        "links": links,
        "headings": headings,
        "policy_links": policy_links
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

    # Remove elements that usually do not contain useful content
    for element in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "template",
        "nav"
    ]):
        element.decompose()

    # Remove common page-level irrelevant sections
    for element in soup([
        "header",
        "footer"
    ]):
        element.decompose()

    # Extract visible text
    text = soup.get_text(
        separator="\n",
        strip=True
    )

    # Normalize whitespace
    lines = []

    for line in text.splitlines():

        line = re.sub(r"\s+", " ", line).strip()

        if line:
            lines.append(line)

    return "\n".join(lines)
