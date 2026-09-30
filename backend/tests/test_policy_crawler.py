from app.services.crawler import crawl_page, crawl_policy_pages


WEBSITE_URL = "https://www.python.org"

print("========================================")
print("STEP 1: CRAWLING WEBSITE")
print("========================================")

homepage = crawl_page(WEBSITE_URL)

print("URL:", homepage["url"])
print("TITLE:", homepage["title"])

print("\nDiscovered links:", len(homepage["links"]))

print("\n--- POLICY LINKS ---")

if homepage["policy_links"]:

    for policy_type, url in homepage["policy_links"].items():
        print(policy_type, "->", url)

else:

    print("No policy pages found.")


print("\n========================================")
print("STEP 2: CRAWLING POLICY PAGES")
print("========================================")

documents = crawl_policy_pages(
    homepage["policy_links"]
)

print("\nDocuments crawled:", len(documents))


for document in documents:

    print("\n----------------------------------------")

    print("TYPE:", document["document_type"])
    print("TITLE:", document["title"])
    print("URL:", document["url"])

    print("TEXT LENGTH:", len(document["text"]))

    print("HEADINGS:", len(document["headings"]))

    print("\n--- ORIGINAL TEXT ---")
    print(document["text"][:500])

    print("\n--- CLEANED TEXT ---")
    print(document["cleaned_text"][:1000])