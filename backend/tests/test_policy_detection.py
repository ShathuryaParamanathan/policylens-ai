from app.services.crawler import find_policy_links


test_links = [
    {
        "text": "Privacy Policy",
        "url": "https://example.com/privacy"
    },
    {
        "text": "Terms of Service",
        "url": "https://example.com/terms"
    },
    {
        "text": "Cookie Policy",
        "url": "https://example.com/legal/cookies"
    },
    {
        "text": "Refund Policy",
        "url": "https://example.com/refunds"
    },
    {
        "text": "Security",
        "url": "https://example.com/security"
    }
]


result = find_policy_links(test_links)


print("--- POLICY DETECTION TEST ---")

for policy_type, url in result.items():
    print(policy_type, "->", url)