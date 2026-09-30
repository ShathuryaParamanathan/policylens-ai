from bson import ObjectId

from app.database import db, check_database_connection
from app.services.crawler import crawl_page, crawl_policy_pages
from app.services.document_service import save_policy_document


WEBSITE_URL = "https://www.python.org"


print("========================================")
print("STEP 1: DATABASE CONNECTION")
print("========================================")

if not check_database_connection():
    print("MongoDB connection failed.")
    raise SystemExit(1)

print("MongoDB connection: OK")


print("\n========================================")
print("STEP 2: CRAWLING WEBSITE")
print("========================================")

homepage = crawl_page(WEBSITE_URL)

print("Website:", homepage["url"])
print("Title:", homepage["title"])

print("\nPolicy links:")

for policy_type, url in homepage["policy_links"].items():
    print(policy_type, "->", url)


print("\n========================================")
print("STEP 3: CRAWLING POLICY PAGES")
print("========================================")

documents = crawl_policy_pages(
    homepage["policy_links"]
)

print("Documents crawled:", len(documents))


print("\n========================================")
print("STEP 4: CREATE WEBSITE")
print("========================================")

website = {
    "url": WEBSITE_URL,
    "domain": "www.python.org",
    "status": "crawled",
}

website_result = db.websites.insert_one(website)

website_id = website_result.inserted_id

print("Website ID:", website_id)


print("\n========================================")
print("STEP 5: STORE DOCUMENTS")
print("========================================")

for document in documents:

    document_id = save_policy_document(
        website_id=website_id,
        document=document,
    )

    print(
        document["document_type"],
        "->",
        document_id
    )


print("\n========================================")
print("STEP 6: VERIFY DATABASE")
print("========================================")

stored_documents = db.documents.count_documents({
    "website_id": website_id
})

print("Documents stored:", stored_documents)