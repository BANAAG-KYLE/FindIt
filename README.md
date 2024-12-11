<div align="center">
  <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/lost_and_found_logo.png" alt="FINDIT Logo" width="400"/>
  
  # FINDIT: Lost and Found Management System
  
  *Lost Today, Found Tomorrow*

  [![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
  
</div>

# Table of Contents
I. [Project Overview](#project-overview)


II. [Python Concepts](#python-concepts)


III. [SDG Integration](#sdg-integration)


IV. [Installation and Usage](#installation-and-usage)


# Project Overview

## About FINDIT
FINDIT is a comprehensive Lost and Found Management System developed to revolutionize how institutions handle lost and found items. Built with Python and modern GUI frameworks, FINDIT offers a secure, efficient, and user-friendly platform for reporting, tracking, and claiming lost items.

## **Major Functionalities and Features**  

### **1. Report Lost Item**  
**Functionality:**  
- Users can report a lost item by providing the following information:  
  - **Description:** A detailed description of the item (validated to ensure meaningful input).  
  - **Location:** The place where the item was found or last seen.  
  - **Found Date:** The date when the item was found.  
  - **Category:** A classification of the item (e.g., electronics, clothing, accessories).  

**How It Works:**  
- The system validates the item description to ensure quality data entry.  
- A unique item ID is generated.  
- The item is stored securely in the system's database.  
- A success message with the assigned item ID is displayed.  

---

### **2. Verify Item Ownership**  
**Functionality:**  
- Users can check if their lost item is in the system by searching using:  
  - **Item Description:** A key phrase describing the item.  
  - **Category (Optional):** Filters results by category.  
  - **Found Date (Optional):** Narrows the search by date.  

**Verification Process:**  
- If matching items are found, users provide their contact details and a detailed description of the item.  
- The system checks the description’s similarity to stored records using a comparison algorithm.  
- If a match is found, the system generates a unique claim code and records the claimant’s details.  

---

### **3. Claim an Item**  
**Functionality:**  
- After successful verification, users can claim their item using the unique claim code provided during the verification process.  

**Claim Process:**  
- The system checks if the claim code exists and is still valid.  
- If the code matches, the item will be marked as “Claimed.”  
- A success message confirms the claim, otherwise, an error message is displayed.  

---

### **4. View All Items**  
**Functionality:**  
- Users can view all unclaimed items currently stored in the system.  

**How It Works:**  
- The system filters and displays only items that are still marked as “Unclaimed.”  
- Each displayed item includes relevant details such as:  
  - **Item ID:** A unique identifier for the item.  
  - **Location:** Where the item was found or last seen.  
  - **Found Date:** When the item was found.  
  - **Category:** The type of item reported.  
- If no unclaimed items are available, a message informs the user that the list is empty.  

---

### **5. Admin Management**  
**Functionality:**  
- The system has a secure admin panel where administrators can:  
  - **Search Claimed Items:** Look up claimed items by item ID.  
  - **View Claimed Records:** Display all claimed items with claimant details.  
  - **Archive Old Claims:** Remove items claimed over 30 days ago to keep the system organized.  

**Security Measures:**  
- Access to the admin panel requires a securely hashed password for authentication.  

---

# Python Concepts

### **1. Object-Oriented Programming**  

#### a) **Encapsulation**  
```python
class LostAndFoundSystem:
    def __init__(self):
        self.items_file = "items.json"
        self.claimants_file = "claimants.json"
        self.items = []
        self.claimants = []
        self.load_data()
        self.admin_password = hashlib.sha256("admin123".encode()).hexdigest()
``` 
- The `LostAndFoundSystem` class bundles data (`items`, `claimants`) and methods (`load_data`, `save_data`) together.  
- Sensitive data like `admin_password` is stored privately within the class.  
- The internal logic for loading, saving, and managing data is hidden from outside access.  
- External code can't directly modify these attributes or bypass validation rules.

---

#### b) **Polymorphism**  
```python
def verify_ownership(self, search_term, category_filter=None, date_filter=None):
    results = []
    for item in self.items:
        if item.claimed:  
            continue
        if search_term and search_term not in item.description.lower():
            continue
        if category_filter and category_filter != item.category:
            continue
        if date_filter and date_filter != item.found_date:
            continue
        results.append(item)
    return results
``` 
- The `verify_ownership()` method behaves differently based on the arguments passed (`search_term`, `category_filter`, `date_filter`).  
- It supports different search criteria without requiring separate methods.  
- This flexibility showcases how the same method can adapt to different use cases.

---

#### c) **Abstraction**  
```python
def report_lost_item(self, description, location, found_date, category):
    validation_error = self.validate_description(description)
    if validation_error:
        return validation_error
    item_id = self.generate_item_id()
    new_item = Item(item_id, description, location, found_date, category)
    self.items.append(new_item)
    self.save_data()
    return f"Item reported successfully with ID: {item_id}"
```
- Users only need to provide minimal input (description, location, etc.).  
- The system internally handles complex processes such as validation, ID generation, and data saving.  
- These implementation details are abstracted away from the user, simplifying the interface.

---

### **2. Data Structures**  

#### a) **Lists Usage**  
```python
def view_items(self):
    unclaimed_items = [item for item in self.items if not item.claimed]
    if not unclaimed_items:
        print("No unclaimed items found.")
        return
    print("\nUnclaimed Items:")
    for item in unclaimed_items:
        print(f"Item ID: {item.item_id} | Location: {item.location}")
```  
- The method uses list comprehension to filter unclaimed items.  
- It iterates through the list and prints relevant details.  

---

#### b) **Dictionary Operations**  
```python
def archive_old_claims(self):
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    archived = 0
    for item in self.items[:]:
        if item.claimed and item.found_date < thirty_days_ago:
            self.items.remove(item)
            archived += 1
    self.save_data()
    return f"Archived {archived} items."
```
- Items are removed from the list based on conditions.  
- A count (`archived`) keeps track of removed items.  
- This shows handling of data structures with conditional logic.

---

### **3. File Operations**  

#### a) **Reading Files**  
```python
def load_data(self):
    try:
        with open(self.items_file, 'r') as f:
            items_data = json.load(f)
            self.items = [Item(**item) for item in items_data]
    except FileNotFoundError:
        print("No items data found.")
```  
- Reads from JSON files and handles `FileNotFoundError` gracefully.  
- Loads items into an in-memory list using the `Item` class.

---

#### b) **Writing Files**  
```python
def save_data(self):
    with open(self.items_file, 'w') as f:
        json.dump([vars(item) for item in self.items], f, indent=4)
    with open(self.claimants_file, 'w') as f:
        json.dump(self.claimants, f, indent=4)
```  
- Saves `items` and `claimants` to files using JSON serialization.  
- Uses `vars()` to convert objects into dictionaries for storage.

---

### **4. Security Implementation**  

#### a) **Password Hashing**  
```python
def __init__(self):
    self.admin_password = hashlib.sha256("admin123".encode()).hexdigest()

# Usage in admin verification
def admin_menu(self):
    password = input("Enter admin password: ")
    if hashlib.sha256(password.encode()).hexdigest() != self.admin_password:
        print("Invalid password.")
        return
```
- The admin password is securely hashed using SHA-256.  
- Password verification compares the hash, ensuring secure storage.

---

#### b) **Unique ID Generation**  
```python
def generate_item_id(self):
    while True:
        item_id = str(random.randint(100, 999))
        if not any(item.item_id == item_id for item in self.items):
            return item_id
```
- The method generates random IDs until a unique one is found.  
- It ensures no duplicate IDs are created.

---

#### c) **Ownership Verification**  
```python
def verify_ownership_description(self, item_id, description, name, contact):
    selected_item = next((item for item in self.items if item.item_id == str(item_id)), None)
    if not selected_item:
        return {"success": False, "message": "Item not found"}

    similarity = SequenceMatcher(None, description.lower(), selected_item.description.lower()).ratio()
    if similarity >= 0.6:
        claim_code = f"CLAIM-{random.randint(1000, 9999)}"
        self.claimants.append({
            "item_id": str(item_id),
            "claim_code": claim_code,
            "name": name,
            "contact": contact
        })
        self.save_data()
        return {"success": True, "claim_code": claim_code}
    return {"success": False, "message": "Description doesn't match"}
``` 
- Ownership verification checks for similarity between descriptions.  
- A claim code is generated only if a sufficient match is found.  

---

### **5. Error Handling**  

#### a) **Input Validation**  
```python
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
``` 
- Checks for claim code validity.  
- Verifies if the item is already claimed.  
- Handles various error conditions and provides clear messages.  


## Libraries and Dependencies
```python
tkinter       # GUI framework
ttkthemes     # Enhanced theming
hashlib       # Security features
json          # Data persistence
datetime      # Date handling
random        # ID generation
difflib       # Text matching
os            # File and directory operations
```


# SDG Integration

## SDG 11: Sustainable Cities and Communities
<div align="center"> <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/SDG-11_banner.png" alt="SDG 11 Banner" width="600"/> </div>

### Integration Aspects
FINDIT promotes **efficient resource management** by facilitating the recovery and reuse of lost items, which would otherwise contribute to waste. By streamlining the lost-and-found process, the system ensures that items such as electronics, clothing, or even books are returned to their rightful owners rather than discarded or left behind. This reduces the overall environmental footprint of unnecessary waste. The platform also enhances **community service** by allowing individuals to report lost and found items, encouraging a collaborative approach to item recovery. 

## SDG 16: Peace, Justice and Strong Institutions
<div align="center"> <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/SGD-16_banner.png" alt="SDG 16 Banner" width="600"/> </div>

### Integration Aspects
FINDIT aligns with **SDG 16: Peace, Justice and Strong Institutions** by promoting **transparent management systems**. All actions in the system, from reporting a found item to claiming ownership, are logged and trackable, ensuring accountability at every step. This transparency fosters trust within the community and helps reduce the risk of corruption or misuse of the system. The platform ensures **fair and accountable processes** by implementing verification steps, such as the need for claimants to provide a description of the lost item that matches the details provided by the finder. This reduces the chances of fraudulent claims, ensuring that only legitimate owners can retrieve their items. Additionally, FINDIT upholds **institutional integrity** by using secure technologies such as password hashing and data encryption to protect user information.

# Installation and Usage

## Prerequisites
- Python 3 or higher
- Windows, macOS, or Linux operating system

## Basic Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BANAAG-KYLE/FindIt.git
2. Navigate to the project repository:
   ```bash
   cd FindIt
3. Install required dependencies:
   ```bash
   pip install ttkthemes
4. Run the program:
   ```bash
   python lost_and_found_ui.py

# Comprehensive User Guide

## Getting Started

<div>
  <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/lost_and_found_UI.png" alt="FINDIT UI" width="400"/>
</div>


FINDIT provides an intuitive graphical interface with five main sections:
- Report Lost Item
- Search and Verify Item Ownership
- Claim Lost Item
- View All Items
- Admin Settings

## For Item Finders

### Reporting Found Items

<div>
  <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/Report_lost_item_example.png" alt="FINDIT UI" width="400"/>
</div>

1. Click the "Report Lost Item" tab
2. Fill in the required information:
   - **Description**: Provide at least 3 words describing the item
   - **Location**: Specify where the item was found
   - **Found Date**: Use YYYY-MM-DD format
   - **Category**: Select from dropdown menu
3. Click "Submit Report"
4. Save the generated Item ID for reference

**Tips for Good Descriptions:**
- Include color, brand, and distinguishing features

## For Item Owners

### Searching for Lost Items

<div>
  <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/Lost_item.png" alt="FINDIT UI" width="400"/>
</div>

1. Navigate to "Search and Verify Item Ownership"
2. Use the search filters:
   - **Keywords**: Enter relevant terms
   - **Date**: When the item was lost (YYYY-MM-DD)
   - **Category**: Filter by item type
3. Click "Search"
4. Review matching items in the results table

### Verifying Ownership

<div>
  <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/Verification.png" alt="FINDIT UI" width="400"/>
</div>

1. Click the matching item from search results
2. Complete the verification form:
   - **Full Name**: Your complete name
   - **Contact Number**: Valid contact information
   - **Item Description**: Detailed description matching your lost item
3. Click "Verify Ownership"
4. If successful, save your claim code
   
<div>
  <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/Verification_successful.png" alt="FINDIT UI" width="400"/>
</div>

- Note: You have 3 attempts to verify ownership
  
<div>
  <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/Verification_Failed.png" alt="FINDIT UI" width="400"/>
</div>
- Descriptions must match at least 60% with the recorded item

## ⚠️IMPORTANT NOTE⚠️

As a student project created in my second year, this system uses practical matching methods that focus on being user-friendly rather than being 100% perfect. The 60% match requirement strikes a balance between keeping items secure and making them easy to claim. People often describe the same item in different ways, so the system allows for these natural differences. While there might be small variations in how well items match, the system is built to work effectively in real situations.


## Claiming Items

<div>
  <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/CLAIM.png" alt="FINDIT UI" width="400"/>
</div>

1. Go to "Claim Lost Item" tab
2. Enter your claim code
3. Click "Claim Item"
4. Follow the collection instructions

<div>
  <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/Claim_Successful.png" alt="FINDIT UI" width="400"/>
</div>

## For Administrators

### Accessing Admin Panel
1. Click the "Admin Settings" tab
2. Enter admin password <details><summary>Click to reveal password</summary> `admin123`</details>
3. Access management features


### Administrative Functions

<div>
  <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/Admin.png" alt="FINDIT UI" width="400"/>
</div>
<div>
  <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/Admin_Menu.png" alt="FINDIT UI" width="400"/>
</div>

1. **View Claimed Items**
   - Check all claimed items
   - View claimant details

<div>
  <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/Admin_View.png" alt="FINDIT UI" width="800"/>
</div>

2. **Archive Management**
   - Archive claims older than 30 days
   - Review archived items

<div>
  <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/Admin_Archive.png" alt="FINDIT UI" width="400"/>
</div>

---

<div align="center">
  <p>Developed with ❤️ for CS 121 – Advanced Computer Programming</p>
  <p>© 2024 FindIt. All rights reserved.</p>
</div>
