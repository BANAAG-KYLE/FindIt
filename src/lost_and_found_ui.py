import hashlib
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import ttkthemes
from lost_and_found_system import LostAndFoundSystem, Item


class LostAndFoundUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lost and Found System")
        self.root.geometry("800x600")
        self.style = ttkthemes.ThemedStyle(self.root)
        self.style.set_theme("equilux")
        self.bg_color = '#2e2e2e'
        self.fg_color = '#ffffff'
        self.accent_color = '#007acc'
        self.root.configure(bg=self.bg_color)
        self.system = LostAndFoundSystem()
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        self.style.configure('Custom.TFrame', background=self.bg_color)
        self.style.configure('Custom.TLabel', background=self.bg_color, foreground=self.fg_color, font=('Helvetica', 10))
        self.style.configure('Custom.TButton', background=self.accent_color, foreground=self.fg_color, padding=10, font=('Helvetica', 10))
        self.style.configure('Title.TLabel', background=self.bg_color, foreground=self.fg_color, font=('Helvetica', 16, 'bold'), padding=10)

    def create_widgets(self):
        # Scrollable Frame Setup
        self.canvas = tk.Canvas(self.root, bg=self.bg_color)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Custom.TFrame')
        self.scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_frame, width=e.width))

        # Main Content
        title_label = ttk.Label(self.scrollable_frame, text="Lost and Found System", style='Title.TLabel')
        title_label.pack(pady=(10, 20))

        self.notebook = ttk.Notebook(self.scrollable_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.notebook.add(self.create_report_tab(), text="Report Lost Item")
        self.notebook.add(self.create_verify_tab(), text="Search and Verify Item Ownership")
        self.notebook.add(self.create_claim_tab(), text="Claim Lost Item")
        self.notebook.add(self.create_view_tab(), text="View All Items")
        self.notebook.add(self.create_admin_tab(), text="Admin Settings")

        exit_btn = ttk.Button(self.scrollable_frame, text="Exit", style='Custom.TButton', command=self.root.destroy)
        exit_btn.pack(pady=10)

    def create_report_tab(self):
        frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        ttk.Label(frame, text="Provide a detailed description of the lost item:", style='Custom.TLabel').pack(anchor='w')
        self.description_entry = ttk.Entry(frame, width=50)
        self.description_entry.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(frame, text="Specify the location where the lost item was found:", style='Custom.TLabel').pack(anchor='w')
        self.location_entry = ttk.Entry(frame, width=50)
        self.location_entry.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(frame, text="State the date on which the item was found (YYYY-MM-DD):", style='Custom.TLabel').pack(anchor='w')
        self.date_entry = ttk.Entry(frame, width=50)
        self.date_entry.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(frame, text="Choose the category that best describes the lost item:", style='Custom.TLabel').pack(anchor='w')
        self.category_combo = ttk.Combobox(frame, values=["Electronics", "Clothing", "Accessories", "Others"], state="readonly")
        self.category_combo.pack(fill=tk.X, pady=(0, 10))
        submit_btn = ttk.Button(frame, text="Submit Report", style='Custom.TButton', command=self.submit_report)
        submit_btn.pack()
        return frame

    def create_verify_tab(self):
        frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        search_frame = ttk.Frame(frame, style='Custom.TFrame')
        search_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(search_frame, text="Search Item:", style='Custom.TLabel').pack(anchor='w')
        self.search_entry = ttk.Entry(search_frame, width=50)
        self.search_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(search_frame, text="Found Date (YYYY-MM-DD):", style='Custom.TLabel').pack(anchor='w')
        self.date_filter_entry = ttk.Entry(search_frame, width=50)
        self.date_filter_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(search_frame, text="Category:", style='Custom.TLabel').pack(anchor='w')
        self.category_filter_combo = ttk.Combobox(search_frame, values=["All", "Electronics", "Clothing", "Accessories", "Others"], state="readonly")
        self.category_filter_combo.set("All")
        self.category_filter_combo.pack(fill=tk.X, pady=(0, 10))

        search_btn = ttk.Button(search_frame, text="Search", style='Custom.TButton', command=self.search_items)
        search_btn.pack(pady=(0, 10))

        self.results_tree = ttk.Treeview(frame, columns=('ID', 'Location', 'Date', 'Category'), show='headings', height=5)
        self.results_tree.heading('ID', text='Item ID')
        self.results_tree.heading('Location', text='Location')
        self.results_tree.heading('Date', text='Found Date')
        self.results_tree.heading('Category', text='Category')
        self.results_tree.pack(fill=tk.X, pady=(0, 20))
        self.results_tree.bind('<<TreeviewSelect>>', self.show_verification_form)

        self.verification_frame = ttk.Frame(frame, style='Custom.TFrame')
        ttk.Label(self.verification_frame, text="Complete Verification Form", style='Title.TLabel').pack(pady=(0, 20))
        ttk.Label(self.verification_frame, text="Full Name:", style='Custom.TLabel').pack(anchor='w')
        self.verify_name_entry = ttk.Entry(self.verification_frame, width=50)
        self.verify_name_entry.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(self.verification_frame, text="Contact Number:", style='Custom.TLabel').pack(anchor='w')
        self.verify_contact_entry = ttk.Entry(self.verification_frame, width=50)
        self.verify_contact_entry.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(self.verification_frame, text="Detailed Item Description:", style='Custom.TLabel').pack(anchor='w')
        self.verify_description_text = tk.Text(self.verification_frame, height=1, width=50)
        self.verify_description_text.pack(fill=tk.X, pady=(0, 10))
        verify_btn = ttk.Button(self.verification_frame, text="Verify Ownership", style='Custom.TButton', command=self.verify_ownership)
        verify_btn.pack(pady=(10, 0))
        self.attempts_label = ttk.Label(self.verification_frame, text="Attempts remaining: 3", style='Custom.TLabel')
        self.attempts_label.pack(pady=(10, 0))
        return frame

    def show_verification_form(self, event):
        selection = self.results_tree.selection()
        if selection:
            self.verify_name_entry.delete(0, tk.END)
            self.verify_contact_entry.delete(0, tk.END)
            self.verify_description_text.delete('1.0', tk.END)
            self.attempts_label.config(text="Attempts remaining: 3")
            self.verification_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        else:
            self.verification_frame.pack_forget()

    def search_items(self):
        search_term = self.search_entry.get().lower()
        selected_category = self.category_filter_combo.get()
        date_filter = self.date_filter_entry.get().strip()
        category_filter = None if selected_category == "All" else selected_category

        if date_filter:
            try:
                datetime.strptime(date_filter, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return

        matching_items = self.system.verify_ownership(search_term, category_filter, date_filter)
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        for item in matching_items:
            self.results_tree.insert('', tk.END, values=(item.item_id, item.location, item.found_date, item.category))

    def verify_ownership(self):
        selection = self.results_tree.selection()
        if not selection:
            return
        item_id = self.results_tree.item(selection[0])['values'][0]
        name = self.verify_name_entry.get().strip()
        contact = self.verify_contact_entry.get().strip()
        description = self.verify_description_text.get('1.0', tk.END).strip()

        if not all([name, contact, description]):
            messagebox.showerror("Error", "All fields are required")
            return

        current_attempts = int(self.attempts_label.cget("text").split(":")[1])
        if current_attempts <= 0:
            messagebox.showerror("Error", "Maximum attempts reached. Please try again later.")
            self.verification_frame.pack_forget()
            return

        result = self.system.verify_ownership_description(item_id, description, name, contact)
        if result["success"]:
            messagebox.showinfo("Success", f"Ownership verified!\nYour claim code is: {result['claim_code']}\n\nPlease keep this code safe.")
            self.verification_frame.pack_forget()
            self.search_entry.delete(0, tk.END)
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
        else:
            remaining_attempts = current_attempts - 1
            self.attempts_label.config(text=f"Attempts remaining: {remaining_attempts}")
            if remaining_attempts > 0:
                messagebox.showwarning("Warning", result["message"] + f" {remaining_attempts} attempts remaining.")
            else:
                messagebox.showerror("Error", "Maximum attempts reached. Please try again later.")
                self.verification_frame.pack_forget()

    def create_claim_tab(self):
        frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        ttk.Label(frame, text="Claim Code:", style='Custom.TLabel').pack(anchor='w')
        self.claim_code_entry = ttk.Entry(frame, width=50)
        self.claim_code_entry.pack(fill=tk.X, pady=(0, 20))
        claim_btn = ttk.Button(frame, text="Claim Item", style='Custom.TButton', command=self.claim_item)
        claim_btn.pack()
        return frame

    def create_view_tab(self):
        frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.items_tree = ttk.Treeview(frame, columns=('ID', 'Location', 'Date', 'Category'), show='headings')
        self.items_tree.heading('ID', text='Item ID')
        self.items_tree.heading('Location', text='Location')
        self.items_tree.heading('Date', text='Found Date')
        self.items_tree.heading('Category', text='Category')
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        refresh_btn = ttk.Button(frame, text="Refresh", style='Custom.TButton', command=self.refresh_items)
        refresh_btn.pack(pady=10)
        return frame

    def create_admin_tab(self):
        frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        ttk.Label(frame, text="Admin Password:", style='Custom.TLabel').pack(anchor='w')
        self.admin_password_entry = ttk.Entry(frame, show="*", width=50)
        self.admin_password_entry.pack(fill=tk.X, pady=(0, 10))
        login_btn = ttk.Button(frame, text="Login", style='Custom.TButton', command=self.admin_login)
        login_btn.pack(pady=(0, 20))
        self.admin_controls = ttk.Frame(frame, style='Custom.TFrame')
        ttk.Button(self.admin_controls, text="View Claimed Items", style='Custom.TButton', command=self.view_claimed_items).pack(pady=5)
        ttk.Button(self.admin_controls, text="Archive Old Claims", style='Custom.TButton', command=self.archive_claims).pack(pady=5)
        return frame

    def submit_report(self):
        try:
            description = self.description_entry.get().strip()
            location = self.location_entry.get().strip()
            found_date = self.date_entry.get().strip()
            category = self.category_combo.get()

            if not location:
                messagebox.showerror("Error", "Location cannot be empty.")
                return

            if not category:
                messagebox.showerror("Error", "Category cannot be empty.")
                return

            if len(description.split()) < 3:
                messagebox.showerror("Error", "Description must be at least 3 words.")
                return

            datetime.strptime(found_date, '%Y-%m-%d')

            item = Item(self.system.generate_item_id(), description, location, found_date, category)
            self.system.items.append(item)
            self.system.save_data()

            messagebox.showinfo("Success", f"Item reported successfully. Item ID: {item.item_id}")

            self.description_entry.delete(0, tk.END)
            self.location_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.category_combo.set('')

        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")

    def claim_item(self):
        claim_code = self.claim_code_entry.get().strip()
        claimant = next((c for c in self.system.claimants if c["claim_code"] == claim_code), None)
        if not claimant:
            messagebox.showerror("Error", "Invalid claim code.")
            return
        item = next((item for item in self.system.items if item.item_id == claimant["item_id"]), None)
        if item and not item.claimed:
            item.claimed = True
            item.status = "Claimed"
            self.system.save_data()
            messagebox.showinfo("Success", 
                "Item claimed successfully!\n\n"
                "Instructions to collect your item:\n"
                "1. Visit the Lost and Found office at Room 101, Admin Building\n"
                "2. Office hours: Monday-Friday, 9:00 AM - 5:00 PM\n"
                "3. Bring your claim code and a valid ID\n"
                "4. Items must be collected within 7 days of claiming"
            )
        else:
            messagebox.showerror("Error", "Item already claimed or not found.")
        self.claim_code_entry.delete(0, tk.END)

    def refresh_items(self):
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        unclaimed_items = [item for item in self.system.items if not item.claimed]
        for item in unclaimed_items:
            self.items_tree.insert('', tk.END, values=(item.item_id, item.location, item.found_date, item.category))

    def admin_login(self):
        password = self.admin_password_entry.get()
        if hashlib.sha256(password.encode()).hexdigest() == self.system.admin_password:
            self.admin_controls.pack(fill=tk.BOTH, expand=True)
            self.admin_password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid password")

    def view_claimed_items(self):
        claimed_items_window = tk.Toplevel(self.root)
        claimed_items_window.title("Claimed Items")
        claimed_items_window.geometry("600x400")
        tree = ttk.Treeview(claimed_items_window, columns=('ID', 'Code', 'Name', 'Contact'), show='headings')
        tree.heading('ID', text='Item ID')
        tree.heading('Code', text='Claim Code')
        tree.heading('Name', text='Claimant Name')
        tree.heading('Contact', text='Contact')
        for claimant in self.system.claimants:
            tree.insert('', tk.END, values=(claimant['item_id'], claimant['claim_code'], claimant['name'], claimant['contact']))
        tree.pack(fill=tk.BOTH, expand=True)

    def archive_claims(self):
        self.system.archive_old_claims()
        messagebox.showinfo("Success", "Old claims archived successfully")

    def run(self):
        self.refresh_items()
        self.root.mainloop()


if __name__ == "__main__":
    app = LostAndFoundUI()
    app.run()