from pymongo import MongoClient
import random
from datetime import datetime, timedelta

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Database
db = client["payment_service_db"]

# Collections
users_coll = db["users"]
transactions_coll = db["transactions"]
merchants_coll = db["merchants"]

# Clear old data (optional)
users_coll.delete_many({})
transactions_coll.delete_many({})
merchants_coll.delete_many({})

# --- Insert Users ---
users = []
for i in range(300):
    user = {
        "user_id": f"U{i+1:04d}",
        "name": {
            "first": f"User{i+1}",
            "last": "Test"
        },
        "email": f"user{i+1}@mail.com",
        "phone": f"+91-9000{random.randint(100000, 999999)}",
        "kyc_status": random.choice(["pending", "verified", "rejected"]),
        "created_at": datetime.utcnow() - timedelta(days=random.randint(0, 365))
    }
    users.append(user)

users_coll.insert_many(users)
print("✅ Inserted 300 users")

# --- Insert Merchants ---
merchants = []
merchant_names = ["Amazon", "Flipkart", "Myntra", "Swiggy", "Zomato", "Paytm", "BigBasket"]
for i in range(300):
    merchant = {
        "merchant_id": f"M{i+1:04d}",
        "name": random.choice(merchant_names),
        "category": random.choice(["ecommerce", "food_delivery", "travel", "entertainment"]),
        "contact_email": f"support{i+1}@merchant.com",
        "contact_phone": f"+91-1800-{random.randint(1000,9999)}-{random.randint(100,999)}",
        "address": {
            "city": random.choice(["Bangalore", "Delhi", "Mumbai", "Hyderabad"]),
            "state": random.choice(["Karnataka", "Maharashtra", "Delhi NCR", "Telangana"]),
            "country": "India"
        },
        "created_at": datetime.utcnow() - timedelta(days=random.randint(0, 1000))
    }
    merchants.append(merchant)

merchants_coll.insert_many(merchants)
print("✅ Inserted 300 merchants")

# --- Insert Transactions ---
transactions = []
for i in range(300):
    user = random.choice(users)         # pick an existing user
    merchant = random.choice(merchants) # pick an existing merchant

    txn = {
        "txn_id": f"TXN{i+1:05d}",
        "user_id": user["user_id"],  # linked to users collection
        "amount": round(random.uniform(50, 5000), 2),
        "currency": "INR",
        "status": random.choice(["success", "pending", "failed"]),
        "payment_method": {
            "type": random.choice(["card", "upi", "wallet"]),
            "card": {
                "last4": str(random.randint(1000, 9999)),
                "network": random.choice(["VISA", "MasterCard", "RuPay"])
            } if random.choice([True, False]) else None
        },
        "merchant": {
            "merchant_id": merchant["merchant_id"],  # linked to merchants collection
            "name": merchant["name"]
        },
        "created_at": datetime.utcnow() - timedelta(days=random.randint(0, 90))
    }
    transactions.append(txn)

transactions_coll.insert_many(transactions)
print("✅ Inserted 300 transactions linked with users and merchants")