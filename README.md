<div align="center">
  <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/lost_and_found_logo.png" alt="FINDIT Logo" width="400"/>
  
  # FINDIT: Lost and Found Management System
  
  *Lost Today, Found Tomorrow*

  [![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
  
</div>

# Table of Contents
I. [Project Overview](#project-overview)


II. [Python Concepts](#python-concepts)


III. [SDG Integration](#sdg-integration)


IV. [Installation and Usage](#installation-and-usage)


# Project Overview

## About FINDIT
FINDIT is a comprehensive Lost and Found Management System developed to revolutionize how institutions handle lost and found items. Built with Python and modern GUI frameworks, FINDIT offers a secure, efficient, and user-friendly platform for reporting, tracking, and claiming lost items.

## Core Features
- 🖥️ Intuitive graphical user interface
- 🔒 Secure authentication system
- 🔍 Advanced search capabilities
- 📊 Administrative dashboard
- 🔄 Automated archiving
- 💾 Persistent data storage
- 🔐 Robust security measures

# Python Concepts


### 1. **Object-Oriented Programming**
Object-Oriented Programming (OOP) principles are at the core of FINDIT's design, enabling a modular, scalable, and reusable codebase. Key OOP features include:

- **Class Inheritance**: Although not used in the current version, FINDIT's architecture supports class inheritance, allowing for future extensions (e.g., creating specialized `Item` subclasses for electronics or documents).
- **Encapsulation**: Sensitive data such as admin passwords and claim codes are protected within methods or hashed, ensuring they aren't directly accessible. Encapsulation improves security and prevents accidental data modification.

- **Polymorphism**: Methods like `verify_ownership_description` exhibit polymorphic behavior by handling ownership verification for various item types without needing separate implementations.
- **Object Composition**: The system uses the `Item` and `Claimant` classes to encapsulate the attributes and behaviors of individual objects, which are then composed into a larger system for efficient management.

---

### 2. **Data Structures**
Efficient use of data structures ensures smooth operation and scalability.

- **Lists**:
  - All items and claimants are stored in lists to allow dynamic addition, removal, and iteration.
  - Operations like filtering unclaimed items or searching for matching descriptions leverage the flexibility of lists.
- **Dictionaries**:
  - Dictionaries are used in JSON serialization for fast lookups and efficient organization of item and claimant data.
- **Custom Classes**:
  - The `Item` class defines the attributes of each lost or found item, such as description, location, and status.
  - The `Claimant` class stores claim details like the claimant’s name, contact information, and claim code.
- **JSON Integration**:
  - JSON provides a structured format for data persistence, ensuring that all data is human-readable and easy to restore upon restarting the application.

---

### 3. **GUI Programming with Tkinter**
FINDIT’s GUI is built using Tkinter, ensuring an interactive and user-friendly interface.

- **Event-Driven Programming**: Tkinter's event loop handles user interactions, such as button clicks and form submissions, without interrupting other operations.
- **Widget Management and Layout**:
  - Widgets such as buttons, labels, text fields, and tables are arranged using Tkinter’s grid and pack layout managers for a responsive interface.
  - Categories and input fields are organized logically to minimize user confusion.
- **Custom Styling and Themes**:
  - The `ttkthemes` library enhances the visual appeal of widgets, providing a modern look and feel.
  - Consistent styling across all screens ensures a professional appearance.
- **User Input Validation**:
  - All input fields validate user entries to prevent errors (e.g., ensuring dates are in `YYYY-MM-DD` format or that descriptions are non-empty).

---

### 4. **File Operations**
File handling is essential for ensuring data is stored persistently and securely.

- **JSON Data Persistence**:
  - All items and claimants are saved as JSON files, allowing for easy data retrieval and updates across sessions.
- **Error Handling Mechanisms**:
  - The system accounts for potential file issues (e.g., missing files) by initializing data or informing the user, ensuring the application remains robust.
- **File I/O Operations**:
  - Operations like reading from and writing to files are encapsulated within methods, making the code reusable and maintainable.
- **Data Validation and Sanitization**:
  - Input data is validated (e.g., ensuring the format of dates and text fields) before saving, preventing data corruption.

---

### 5. **Security Implementation**
Security is a core feature of FINDIT, ensuring user data integrity and protecting sensitive operations.

- **Password Hashing (SHA-256)**:
  - The admin password is stored as a hashed value using the SHA-256 algorithm. This ensures the actual password is never exposed, even in the event of a data breach.
- **Unique Identifier Generation**:
  - Unique IDs for items and claimants are generated using random number functions, preventing duplication and ensuring traceability.
- **Claim Verification System**:
  - The system verifies ownership through a claim description that must meet a 60% similarity threshold, using Python's `difflib` library to calculate text similarity.
- **Input Sanitization**:
  - Inputs are stripped of unnecessary whitespace, checked for invalid characters, and formatted correctly to avoid injection attacks or errors.


## Libraries and Dependencies
```python
tkinter       # GUI framework
ttkthemes     # Enhanced theming
hashlib       # Security features
json          # Data persistence
datetime      # Date handling
random        # ID generation
difflib       # Text matching
```


# SDG Integration

## SDG 11: Sustainable Cities and Communities
<div align="center"> <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/SDG-11_banner.png" alt="SDG 11 Banner" width="600"/> </div>

### Integration Aspects
FINDIT promotes **efficient resource management** by facilitating the recovery and reuse of lost items, which would otherwise contribute to waste. By streamlining the lost-and-found process, the system ensures that items such as electronics, clothing, or even books are returned to their rightful owners rather than discarded or left behind. This reduces the overall environmental footprint of unnecessary waste. The platform also enhances **community service** by allowing individuals to report lost and found items, encouraging a collaborative approach to item recovery. This fosters a sense of responsibility and social cohesion, as people work together to return lost property to its rightful owner. Furthermore, FINDIT improves **institutional efficiency** by automating item tracking and managing claims, which reduces administrative workload, minimizes errors, and accelerates the process of returning items to their owners. Lastly, the system encourages **sustainable practices** by promoting the proper handling and retention of lost items, which can reduce the demand for new products and thus minimize resource consumption.

## SDG 16: Peace, Justice and Strong Institutions
<div align="center"> <img src="https://github.com/BANAAG-KYLE/FindIt/blob/main/Images/SGD-16_banner.png" alt="SDG 16 Banner" width="600"/> </div>

### Integration Aspects
FINDIT aligns with **SDG 16: Peace, Justice and Strong Institutions** by promoting **transparent management systems**. All actions in the system, from reporting a found item to claiming ownership, are logged and trackable, ensuring accountability at every step. This transparency fosters trust within the community and helps reduce the risk of corruption or misuse of the system. The platform ensures **fair and accountable processes** by implementing verification steps, such as the need for claimants to provide a description of the lost item that matches the details provided by the finder. This reduces the chances of fraudulent claims, ensuring that only legitimate owners can retrieve their items. Additionally, FINDIT upholds **institutional integrity** by using secure technologies such as password hashing and data encryption to protect user information. This gives users confidence that their personal details and claims will be handled securely and fairly. Finally, the system helps **build trust** within the community by maintaining a clear, open, and efficient process for item recovery. As users interact with the platform and experience its reliability, they are more likely to trust the institution managing the lost-and-found system.

## Impact and Contribution
FINDIT contributes to a more sustainable society by **reducing waste** through the recovery of lost items. Many items that are reported as lost often end up discarded or forgotten. By making it easier to track, report, and claim these items, FINDIT helps ensure that useful goods are reused instead of contributing to environmental waste. The platform **enhances institutional efficiency** by automating and organizing the process of reporting, verifying, and claiming lost items, reducing the administrative burden on staff and improving the speed at which items are returned to their rightful owners. This also strengthens **community trust** by ensuring that lost items are managed transparently and equitably, making individuals more likely to engage with the system. Moreover, FINDIT helps improve **resource management** by maintaining an organized database of lost and found items, making it easier for institutions to handle and archive records. This streamlined process saves time and resources, ensuring that valuable items are not lost in an inefficient system.


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


## ⚠️IMPORTANT NOTE⚠️

While aiming for 100% accuracy, please note that small discrepancies might occur due to the current capabilities of the system, as fine-tuning the verification process is still a work in progress. These slight variations, however, are generally minimal and do not hinder the ownership verification.

## For Administrators

### Accessing Admin Panel
1. Click "Admin Settings" tab
2. Enter admin password
3. Access management features

### Administrative Functions
1. **View Claimed Items**
   - Check all claimed items
   - View claimant details
   - Monitor claim status

2. **Archive Management**
   - Archive claims older than 30 days
   - Review archived items
   - Generate reports

3. **System Monitoring**
   - Track verification attempts
   - Monitor system usage
   - Manage user claims

## Best Practices

### For Item Finders
- Report items immediately
- Document item condition
- Note exact location and time
- Handle items with care
- Don't open sealed items

### For Item Owners
- Act promptly when searching
- Provide accurate descriptions
- Keep claim codes secure
- Collect items within deadline
- Bring required documentation

### For Administrators
- Regular system monitoring
- Timely archive management
- Verify claimant identity
- Maintain accurate records
- Update system regularly

---

<div align="center">
  <p>Developed with ❤️ for CS 121 – Advanced Computer Programming</p>
  <p>© 2024 FINDIT. All rights reserved.</p>
</div>
