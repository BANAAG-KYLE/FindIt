import json
import os
from datetime import datetime, timedelta
import hashlib
import random
from difflib import SequenceMatcher


class Item:
    def __init__(self, item_id, description, location, found_date, category, claimed=False, status="Unclaimed"):
        self.item_id = item_id
        self.description = description
        self.location = location
        self.found_date = found_date
        self.category = category
        self.claimed = claimed
        self.status = status


class Claimant:
    def __init__(self, item_id, claim_code, name, contact):
        self.item_id = item_id
        self.claim_code = claim_code
        self.name = name
        self.contact = contact


class LostAndFoundSystem:
    def __init__(self):
        self.items_file = "items.json"
        self.claimants_file = "claimants.json"
        self.items = []
        self.claimants = []
        self.load_data()
        self.admin_password = hashlib.sha256("admin123".encode()).hexdigest()

    def load_data(self):
        try:
            with open(self.items_file, 'r') as f:
                items_data = json.load(f)
                self.items = [Item(**item) for item in items_data]
        except FileNotFoundError:
            print("No items data found.")

        try:
            with open(self.claimants_file, 'r') as f:
                self.claimants = json.load(f)
        except FileNotFoundError:
            print("No claimants data found.")

    def save_data(self):
        with open(self.items_file, 'w') as f:
            json.dump([vars(item) for item in self.items], f, indent=4)
        with open(self.claimants_file, 'w') as f:
            json.dump(self.claimants, f, indent=4)

    def generate_item_id(self):
        while True:
            item_id = str(random.randint(100, 999))
            if not any(item.item_id == item_id for item in self.items):
                return item_id

    def validate_description(self, description):
        if not description.strip():
            return "Description cannot be empty."
        if len(description.split()) < 3:
            return "Description must be at least 3 words."
        return None

    def report_lost_item(self, description, location, found_date, category):
        validation_error = self.validate_description(description)
        if validation_error:
            return validation_error
        item_id = self.generate_item_id()
        new_item = Item(item_id, description, location, found_date, category)
        self.items.append(new_item)
        self.save_data()
        return f"Item reported successfully with ID: {item_id}"

    def verify_ownership(self, search_term, category_filter=None, date_filter=None):
        results = []
        for item in self.items:
            if item.claimed:  # Exclude claimed items
                continue
            if search_term and search_term not in item.description.lower():
                continue
            if category_filter and category_filter != item.category:
                continue
            if date_filter and date_filter != item.found_date:
                continue
            results.append(item)
        return results

    def verify_ownership_description(self, item_id, description, name, contact):
        selected_item = next((item for item in self.items if item.item_id == str(item_id)), None)
        if not selected_item:
            return {"success": False, "message": "Item not found"}

        similarity = SequenceMatcher(None, description.lower(), selected_item.description.lower()).ratio()
        if similarity >= 0.6:
            claim_code = f"CLAIM-{random.randint(1000, 9999)}"
            self.claimants.append({"item_id": str(item_id), "claim_code": claim_code, "name": name, "contact": contact})
            self.save_data()
            return {"success": True, "claim_code": claim_code}
        return {"success": False, "message": "Description doesn't match"}

    def claim_item(self, claim_code):
        claimant = next(
            (c for c in self.claimants if c["claim_code"] == claim_code), None
        )
        if not claimant:
            return "Invalid claim code."

        item = next((item for item in self.items if item.item_id == claimant["item_id"]), None)
        if item and not item.claimed:
            item.claimed = True
            item.status = "Claimed"
            self.save_data()
            return "Item claimed successfully!"
        else:
            return "Error: Item already claimed or not found."

    def view_items(self):
        unclaimed_items = [item for item in self.items if not item.claimed]
        if not unclaimed_items:
            print("No unclaimed items found.")
            return
        print("\nUnclaimed Items:")
        for item in unclaimed_items:
            print(f"Item ID: {item.item_id} | Location: {item.location} | Found Date: {item.found_date} | Category: {item.category}")

    def admin_menu(self):
        password = input("Enter admin password: ")
        if hashlib.sha256(password.encode()).hexdigest() != self.admin_password:
            print("Invalid password.")
            return

        while True:
            print("\nAdmin Menu:")
            print("1. Search claimed items")
            print("2. View all claimed items")
            print("3. Archive old claims")
            print("4. Go back")

            choice = input("Enter choice: ")
            if choice == "1":
                item_id = input("Enter item ID: ")
                claimant = next((c for c in self.claimants if c["item_id"] == item_id), None)
                if claimant:
                    print(f"\nItem ID: {claimant['item_id']}")
                    print(f"Claim Code: {claimant['claim_code']}")
                    print(f"Claimant Name: {claimant['name']}")
                    print(f"Claimant Contact: {claimant['contact']}")
                else:
                    print("Item not found.")
            elif choice == "2":
                claimed_items = [c for c in self.claimants]
                if claimed_items:
                    print("\nClaimed Items:")
                    for c in claimed_items:
                        print(f"Item ID: {c['item_id']} | Claim Code: {c['claim_code']} | Name: {c['name']} | Contact: {c['contact']}")
                else:
                    print("No claimed items.")
            elif choice == "3":
                self.archive_old_claims()
            elif choice == "4":
                break

    def archive_old_claims(self):
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        archived = 0
        for item in self.items[:]:
            if item.claimed and item.found_date < thirty_days_ago:
                self.items.remove(item)
                archived += 1
        self.save_data()
        return f"Archived {archived} items."

    def run(self):
        while True:
            print("\nLost and Found System")
            print("1. Report a lost item")
            print("2. Verify item ownership")
            print("3. Claim item")
            print("4. View all items")
            print("5. Admin settings")
            print("6. Exit")

            choice = input("Enter choice: ")
            if choice == "1":
                description = input("Enter description: ")
                location = input("Enter location: ")
                found_date = input("Enter found date (YYYY-MM-DD): ")
                category = input("Enter category: ")
                print(self.report_lost_item(description, location, found_date, category))
            elif choice == "2":
                search_term = input("Enter item description to search: ")
                matching_items = self.verify_ownership(search_term)
                if matching_items:
                    print("\nMatching Items:")
                    for item in matching_items:
                        print(f"Item ID: {item.item_id} | Location: {item.location} | Found Date: {item.found_date} | Category: {item.category}")
                else:
                    print("No matching items found.")
            elif choice == "3":
                claim_code = input("Enter claim code: ")
                print(self.claim_item(claim_code))
            elif choice == "4":
                self.view_items()
            elif choice == "5":
                self.admin_menu()
            elif choice == "6":
                print("Thank you for using the Lost and Found System!")
                break
            else:
                print("Invalid choice. Please try again.")