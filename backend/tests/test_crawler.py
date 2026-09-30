from app.services.crawler import crawl_page


result = crawl_page("https://example.com")

print("URL:", result["url"])
print("TITLE:", result["title"])
print("HTML LENGTH:", len(result["html"]))
print("TEXT LENGTH:", len(result["text"]))

print("\n--- LINKS ---")

for link in result["links"]:
    print(link["text"], "->", link["url"])


print("\n--- POLICY LINKS ---")

for policy_type, url in result["policy_links"].items():
    print(policy_type, "->", url)