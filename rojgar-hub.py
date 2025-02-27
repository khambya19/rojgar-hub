import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sqlite3
from datetime import datetime
from tkinter import font as tkfont

# pushing


def init_db():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            experience TEXT NOT NULL,
            salary TEXT NOT NULL,
            category TEXT NOT NULL,
            post_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open'
        )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            user_id TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            apply_date TEXT NOT NULL,
            feedback TEXT,
            FOREIGN KEY(job_id) REFERENCES jobs(id)
        )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS admin (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )"""
    )

    admin_password = "admin123"
    cursor.execute(
        "INSERT OR IGNORE INTO admin (username, password) VALUES ('admin', ?)",
        (admin_password,),
    )

    conn.commit()
    conn.close()


class RojgarHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Rojgar Hub")
        self.root.geometry("1024x768")

        # Color scheme
        self.colors = {
            "primary": "#2196F3",
            "secondary": "#FFC107",
            "success": "#4CAF50",
            "danger": "#F44336",
            "warning": "#FF9800",
            "info": "#00BCD4",
            "light": "#F5F5F5",
            "dark": "#212121",
            "white": "#352B2A",
            "bg": "#F0F2F5",
        }

        # Configure root window
        self.root.configure(bg=self.colors["bg"])
        self.current_user = None

        # Configure styles
        self.setup_styles()
        self.create_login_screen()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Configure Treeview
        style.configure(
            "Treeview",
            background=self.colors["white"],
            fieldbackground=self.colors["white"],
            foreground=self.colors["dark"],
        )
        style.configure(
            "Treeview.Heading",
            background=self.colors["primary"],
            foreground=self.colors["white"],
            relief="flat",
        )
        style.map("Treeview.Heading", background=[("active", self.colors["info"])])

        # Configure other ttk elements
        style.configure(
            "TButton", padding=6, relief="flat", background=self.colors["primary"]
        )
        style.configure("TEntry", padding=6)
        style.configure("TLabel", background=self.colors["bg"])

    def create_header(self, parent, title):
        header = tk.Frame(parent, bg=self.colors["primary"], height=60)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)

        tk.Label(
            header,
            text=title,
            font=("Helvetica", 16, "bold"),
            bg=self.colors["primary"],
            fg=self.colors["white"],
        ).pack(side="left", padx=20, pady=10)

        return header

    def create_styled_button(self, parent, text, command, color=None, width=None):
        if color is None:
            color = self.colors["primary"]

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=self.colors["white"],
            font=("Helvetica", 10),
            relief="flat",
            activebackground=self.colors["info"],
            activeforeground=self.colors["white"],
            cursor="hand2",
            width=width if width else 20,
            pady=8,
        )
        return btn

    def create_styled_entry(self, parent, show=None):
        entry = tk.Entry(
            parent,
            font=("Helvetica", 10),
            bg=self.colors["white"],
            relief="solid",
            width=30,
        )
        if show:
            entry.configure(show=show)
        return entry

    def create_login_screen(self):
        self.clear_screen()

        # Main container
        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Logo/Header
        tk.Label(
            container,
            text="🌟  Rojgar Hub",
            font=("Helvetica", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["dark"],
        ).pack(pady=30)

        # Login options container
        login_frame = tk.Frame(container, bg=self.colors["white"], padx=40, pady=40)
        login_frame.pack(expand=True, fill="both", padx=200, pady=20)

        tk.Label(
            login_frame,
            text="Welcome! Please select your login type",
            font=("Helvetica", 14),
            bg=self.colors["white"],
        ).pack(pady=(0, 20))

        self.create_styled_button(
            login_frame,
            "👔 Admin Login",
            self.admin_login_screen,
            self.colors["primary"],
        ).pack(pady=10)

        self.create_styled_button(
            login_frame, "👤 User Login", self.user_login_screen, self.colors["success"]
        ).pack(pady=10)

        self.create_styled_button(
            login_frame,
            "✨ Register New User",
            self.register_user_screen,
            self.colors["warning"],
        ).pack(pady=10)

    def admin_login_screen(self):
        self.clear_screen()
        self.create_header(self.root, "Admin Login")

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Login form
        login_frame = tk.Frame(container, bg=self.colors["white"], padx=40, pady=40)
        login_frame.pack(expand=True, fill="both", padx=200, pady=20)

        tk.Label(
            login_frame,
            text="Admin Login",
            font=("Helvetica", 16, "bold"),
            bg=self.colors["white"],
        ).pack(pady=(0, 20))

        # Username
        tk.Label(login_frame, text="Username:", bg=self.colors["white"]).pack()
        username_entry = self.create_styled_entry(login_frame)
        username_entry.pack(pady=(0, 10))

        # Password
        tk.Label(login_frame, text="Password:", bg=self.colors["white"]).pack()
        password_entry = self.create_styled_entry(login_frame, show="*")
        password_entry.pack(pady=(0, 20))

        def attempt_login():
            username = username_entry.get()
            password = password_entry.get()

            conn = sqlite3.connect("jobs.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM admin WHERE username=? AND password=?",
                (username, password),
            )
            admin = cursor.fetchone()
            conn.close()

            if admin:
                self.current_user = username
                self.admin_panel()
            else:
                messagebox.showerror("Error", "Invalid credentials!")

        self.create_styled_button(
            login_frame, "Login", attempt_login, self.colors["primary"]
        ).pack(pady=10)

        self.create_styled_button(
            login_frame, "Back", self.create_login_screen, self.colors["danger"]
        ).pack()

    def user_login_screen(self):
        self.clear_screen()
        self.create_header(self.root, "User Login")

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(expand=True, fill="both", padx=20, pady=20)

        login_frame = tk.Frame(container, bg=self.colors["white"], padx=40, pady=40)
        login_frame.pack(expand=True, fill="both", padx=200, pady=20)

        tk.Label(login_frame, text="Username:", bg=self.colors["white"]).pack()
        username_entry = self.create_styled_entry(login_frame)
        username_entry.pack(pady=(0, 10))

        tk.Label(login_frame, text="Password:", bg=self.colors["white"]).pack()
        password_entry = self.create_styled_entry(login_frame, show="*")
        password_entry.pack(pady=(0, 20))

        def attempt_user_login():
            username = username_entry.get()
            password = password_entry.get()

            conn = sqlite3.connect("jobs.db")
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username=?", (username,))
            user = cursor.fetchone()
            conn.close()

            if user and password == user[0]:
                self.current_user = username
                self.user_panel()
            else:
                messagebox.showerror("Error", "Invalid credentials!")

        self.create_styled_button(
            login_frame, "Login", attempt_user_login, self.colors["primary"]
        ).pack(pady=10)
        self.create_styled_button(
            login_frame, "Back", self.create_login_screen, self.colors["danger"]
        ).pack()

    def register_user_screen(self):
        self.clear_screen()
        self.create_header(self.root, "User Registration")

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(expand=True, fill="both", padx=20, pady=20)

        form_frame = tk.Frame(container, bg=self.colors["white"], padx=40, pady=40)
        form_frame.pack(expand=True, fill="both", padx=200, pady=20)

        tk.Label(form_frame, text="Full Name:", bg=self.colors["white"]).pack()
        full_name_entry = self.create_styled_entry(form_frame)
        full_name_entry.pack(pady=(0, 10))

        tk.Label(form_frame, text="Email:", bg=self.colors["white"]).pack()
        email_entry = self.create_styled_entry(form_frame)
        email_entry.pack(pady=(0, 10))

        tk.Label(form_frame, text="Phone:", bg=self.colors["white"]).pack()
        phone_entry = self.create_styled_entry(form_frame)
        phone_entry.pack(pady=(0, 10))

        tk.Label(form_frame, text="Username:", bg=self.colors["white"]).pack()
        username_entry = self.create_styled_entry(form_frame)
        username_entry.pack(pady=(0, 10))

        tk.Label(form_frame, text="Password:", bg=self.colors["white"]).pack()
        password_entry = self.create_styled_entry(form_frame, show="*")
        password_entry.pack(pady=(0, 20))

        def register_user():
            full_name = full_name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            username = username_entry.get()
            password = password_entry.get()

            if not (full_name and email and phone and username and password):
                messagebox.showerror("Error", "All fields are required!")
                return

            conn = sqlite3.connect("jobs.db")
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (username, full_name, email, phone, password) VALUES (?, ?, ?, ?, ?)",
                    (username, full_name, email, phone, password),
                )
                conn.commit()
                messagebox.showinfo("Success", "User registered successfully!")
                self.create_login_screen()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")
            conn.close()

        self.create_styled_button(
            form_frame, "Register", register_user, self.colors["success"]
        ).pack(pady=10)
        self.create_styled_button(
            form_frame, "Back", self.create_login_screen, self.colors["danger"]
        ).pack()

    def admin_panel(self):
        self.clear_screen()
        self.create_header(self.root, f"Welcome, {self.current_user}")

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Dashboard stats
        stats_frame = tk.Frame(container, bg=self.colors["white"])
        stats_frame.pack(fill="x", padx=20, pady=20)

        # Fetch stats
        conn = sqlite3.connect("jobs.db")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM jobs")
        total_jobs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM applications")
        total_applications = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Selected'")
        selected_candidates = cursor.fetchone()[0]

        conn.close()

        # Display stats
        stats = [
            ("Total Jobs Posted", total_jobs, self.colors["primary"]),
            ("Total Applications", total_applications, self.colors["warning"]),
            ("Selected Candidates", selected_candidates, self.colors["success"]),
        ]

        for title, value, color in stats:
            stat_box = tk.Frame(stats_frame, bg=color, padx=20, pady=10)
            stat_box.pack(side="left", expand=True, fill="both", padx=10, pady=10)

            tk.Label(
                stat_box,
                text=title,
                font=("Helvetica", 12),
                bg=color,
                fg=self.colors["white"],
            ).pack()

            tk.Label(
                stat_box,
                text=str(value),
                font=("Helvetica", 24, "bold"),
                bg=color,
                fg=self.colors["white"],
            ).pack()

        # Action buttons
        button_frame = tk.Frame(container, bg=self.colors["bg"])
        button_frame.pack(pady=20)

        self.create_styled_button(
            button_frame,
            "📝 Post New Job",
            self.create_job_screen,
            self.colors["primary"],
        ).pack(pady=10)

        self.create_styled_button(
            button_frame,
            "👥 View Applications",
            self.view_applications,
            self.colors["warning"],
        ).pack(pady=10)

        self.create_styled_button(
            button_frame, "📊 View Jobs", self.view_jobs, self.colors["info"]
        ).pack(pady=10)

        self.create_styled_button(
            button_frame, "🚪 Logout", self.create_login_screen, self.colors["danger"]
        ).pack(pady=10)

    def edit_application(self, app_id):
        self.clear_screen()
        self.create_header(self.root, "Edit Application")

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(expand=True, fill="both", padx=20, pady=20)

        form_frame = tk.Frame(container, bg=self.colors["white"], padx=40, pady=40)
        form_frame.pack(expand=True, fill="both", padx=200, pady=20)

        conn = sqlite3.connect("jobs.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT j.title, u.full_name, u.email, u.phone, a.status, a.feedback
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            JOIN users u ON a.user_id = u.username
            WHERE a.id = ?
        """,
            (app_id,),
        )
        application = cursor.fetchone()
        conn.close()

        labels = ["Job Title", "Applicant Name", "Email", "Phone", "Status", "Feedback"]
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label + ":", bg=self.colors["white"]).pack()
            entry = self.create_styled_entry(form_frame)
            entry.pack(pady=(0, 10))
            entry.insert(0, application[i])
            entries[label] = entry

        def save_changes():
            status = entries["Status"].get()
            feedback = entries["Feedback"].get()

            conn = sqlite3.connect("jobs.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE applications SET status = ?, feedback = ? WHERE id = ?",
                (status, feedback, app_id),
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Application updated successfully!")
            self.view_applications()

        self.create_styled_button(
            form_frame, "💾 Save Changes", save_changes, self.colors["success"]
        ).pack(pady=10)

        self.create_styled_button(
            form_frame, "⬅️ Back", self.view_applications, self.colors["danger"]
        ).pack(pady=10)

    def delete_application(self, app_id):
        if messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this application?"
        ):
            conn = sqlite3.connect("jobs.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Application deleted successfully!")
            self.view_applications()

    def view_applications(self):
        self.clear_screen()
        self.create_header(self.root, "Job Applications")

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Create Treeview
        columns = ("Job", "Applicant", "Email", "Phone", "Status", "Applied Date")
        tree = ttk.Treeview(container, columns=columns, show="headings")

        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Add scrollbars
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")

        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        tree.pack(expand=True, fill="both", pady=(0, 20))

        # Fetch applications
        conn = sqlite3.connect("jobs.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                j.title,
                u.full_name,
                u.email,
                u.phone,
                a.status,
                a.apply_date,
                a.id
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            JOIN users u ON a.user_id = u.username
            ORDER BY a.apply_date DESC
        """
        )
        applications = cursor.fetchall()
        conn.close()

        for app in applications:
            tree.insert("", "end", values=app[:-1], tags=(app[-1],))

        # Action buttons
        button_frame = tk.Frame(container, bg=self.colors["bg"])
        button_frame.pack(pady=10)

        def select_applicant():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select an application")
                return

            app_id = tree.item(selected_item[0])["tags"][0]
            feedback = simpledialog.askstring(
                "Feedback", "Enter feedback for the applicant (optional):"
            )

            conn = sqlite3.connect("jobs.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE applications SET status = ?, feedback = ? WHERE id = ?",
                ("Selected", feedback, app_id),
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Applicant has been selected!")
            self.view_applications()

        def reject_applicant():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select an application")
                return

            app_id = tree.item(selected_item[0])["tags"][0]
            feedback = simpledialog.askstring(
                "Feedback", "Enter feedback for the applicant (optional):"
            )

            conn = sqlite3.connect("jobs.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE applications SET status = ?, feedback = ? WHERE id = ?",
                ("Rejected", feedback, app_id),
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Applicant has been rejected!")
            self.view_applications()

        def edit_selected_application():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select an application")
                return

            app_id = tree.item(selected_item[0])["tags"][0]
            self.edit_application(app_id)

        def delete_selected_application():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select an application")
                return

            app_id = tree.item(selected_item[0])["tags"][0]
            self.delete_application(app_id)

        self.create_styled_button(
            button_frame, "✅ Select", select_applicant, self.colors["success"]
        ).pack(side="left", padx=5)

        self.create_styled_button(
            button_frame, "❌ Reject", reject_applicant, self.colors["danger"]
        ).pack(side="left", padx=5)

        self.create_styled_button(
            button_frame, "✏️ Edit", edit_selected_application, self.colors["warning"]
        ).pack(side="left", padx=5)

        self.create_styled_button(
            button_frame, "🗑️ Delete", delete_selected_application, self.colors["danger"]
        ).pack(side="left", padx=5)

        self.create_styled_button(
            button_frame, "⬅️ Back", self.admin_panel, self.colors["primary"]
        ).pack(side="left", padx=5)

    def view_applications(self):
        self.clear_screen()
        self.create_header(self.root, "Job Applications")

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Create Treeview
        columns = ("Job", "Applicant", "Email", "Phone", "Status", "Applied Date")
        tree = ttk.Treeview(container, columns=columns, show="headings")

        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Add scrollbars
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")

        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        tree.pack(expand=True, fill="both", pady=(0, 20))

        # Fetch applications
        conn = sqlite3.connect("jobs.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                j.title,
                u.full_name,
                u.email,
                u.phone,
                a.status,
                a.apply_date,
                a.id
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            JOIN users u ON a.user_id = u.username
            ORDER BY a.apply_date DESC
        """
        )
        applications = cursor.fetchall()
        conn.close()

        for app in applications:
            tree.insert("", "end", values=app[:-1], tags=(app[-1],))

        # Action buttons
        button_frame = tk.Frame(container, bg=self.colors["bg"])
        button_frame.pack(pady=10)

        def select_applicant():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select an application")
                return

            app_id = tree.item(selected_item[0])["tags"][0]
            feedback = simpledialog.askstring(
                "Feedback", "Enter feedback for the applicant (optional):"
            )

            conn = sqlite3.connect("jobs.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE applications SET status = ?, feedback = ? WHERE id = ?",
                ("Selected", feedback, app_id),
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Applicant has been selected!")
            self.view_applications()

        def reject_applicant():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select an application")
                return

            app_id = tree.item(selected_item[0])["tags"][0]
            feedback = simpledialog.askstring(
                "Feedback", "Enter feedback for the applicant (optional):"
            )

            conn = sqlite3.connect("jobs.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE applications SET status = ?, feedback = ? WHERE id = ?",
                ("Rejected", feedback, app_id),
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Applicant has been rejected!")
            self.view_applications()

        self.create_styled_button(
            button_frame, "✅ Select", select_applicant, self.colors["success"]
        ).pack(side="left", padx=5)

        self.create_styled_button(
            button_frame, "❌ Reject", reject_applicant, self.colors["danger"]
        ).pack(side="left", padx=5)

        self.create_styled_button(
            button_frame, "⬅️ Back", self.admin_panel, self.colors["primary"]
        ).pack(side="left", padx=5)

    def view_jobs(self):
        self.clear_screen()
        self.create_header(self.root, "Posted Jobs")

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Define columns
        columns = ("Title", "Category", "Experience", "Salary", "Posted Date", "Status")

        # Create Treeview
        tree = ttk.Treeview(container, columns=columns, show="headings")

        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Scrollbars (placed outside the loop)
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")

        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        tree.pack(expand=True, fill="both", pady=(0, 20))

        # Fetch jobs
        conn = sqlite3.connect("jobs.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT title, category, experience, salary, post_date, status, id
            FROM jobs
            ORDER BY post_date DESC
            """
        )
        jobs = cursor.fetchall()
        conn.close()

        for job in jobs:
            tree.insert("", "end", values=job[:-1], tags=(job[-1],))

        # Action buttons
        button_frame = tk.Frame(container, bg=self.colors["bg"])
        button_frame.pack(pady=10)

        def close_job():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a job")
                return

            job_id = tree.item(selected_item[0])["tags"][0]

            conn = sqlite3.connect("jobs.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE jobs SET status = ? WHERE id = ?", ("Closed", job_id)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Job has been closed!")
            self.view_jobs()

        def edit_job():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a job to edit")
                return

            job_values = tree.item(selected_item[0])["values"]
            job_id = tree.item(selected_item[0])["tags"][0]

            # Open a new window for editing
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Job")

            labels = [
                "Title",
                "Category",
                "Experience",
                "Salary",
                "Posted Date",
                "Status",
            ]
            entries = {}

            for i, label in enumerate(labels):
                tk.Label(edit_window, text=label).grid(row=i, column=0, padx=10, pady=5)
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(0, job_values[i])
                entries[label] = entry

            def save_changes():
                updated_values = [entries[label].get() for label in labels]

                conn = sqlite3.connect("jobs.db")
                cursor = conn.cursor()
                cursor.execute(
                    """UPDATE jobs SET title=?, category=?, experience=?, salary=?, post_date=?, status=?
                    WHERE id=?""",
                    (*updated_values, job_id),
                )
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Job updated successfully!")
                edit_window.destroy()
                self.view_jobs()

            tk.Button(edit_window, text="Save", command=save_changes).grid(
                row=6, column=0, columnspan=2, pady=10
            )

        def delete_job():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a job to delete")
                return

            job_id = tree.item(selected_item[0])["tags"][0]

            confirm = messagebox.askyesno(
                "Confirm", "Are you sure you want to delete this job?"
            )
            if confirm:
                conn = sqlite3.connect("jobs.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Job deleted successfully!")
                self.view_jobs()

        self.create_styled_button(
            button_frame, "🔒 Close Job", close_job, self.colors["warning"]
        ).pack(side="left", padx=5)
        self.create_styled_button(
            button_frame, "✏️ Edit Job", edit_job, self.colors["primary"]
        ).pack(side="left", padx=5)
        self.create_styled_button(
            button_frame, "🗑️ Delete Job", delete_job, self.colors["danger"]
        ).pack(side="left", padx=5)
        self.create_styled_button(
            button_frame, "⬅️ Back", self.admin_panel, self.colors["primary"]
        ).pack(side="left", padx=5)

    def create_job_screen(self):
        self.clear_screen()
        self.create_header(self.root, "Post New Job")

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Job form
        form_frame = tk.Frame(container, bg=self.colors["white"], padx=40, pady=40)
        form_frame.pack(expand=True, fill="both", padx=200)

        # Create form fields
        fields = {}
        labels = {
            "title": "Job Title",
            "category": "Category",
            "experience": "Required Experience",
            "salary": "Salary Range",
            "description": "Job Description",
        }

        for field, label in labels.items():
            tk.Label(
                form_frame,
                text=label + ":",
                font=("Helvetica", 10, "bold"),
                bg=self.colors["white"],
            ).pack(pady=(10, 0))

            if field == "description":
                entry = tk.Text(form_frame, height=4, width=40)
            else:
                entry = self.create_styled_entry(form_frame)
            entry.pack()
            fields[field] = entry

        def save_job():
            values = {}
            for field, entry in fields.items():
                if isinstance(entry, tk.Text):
                    values[field] = entry.get("1.0", "end-1c").strip()
                else:
                    values[field] = entry.get().strip()

            if all(values.values()):
                conn = sqlite3.connect("jobs.db")
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO jobs (title, category, experience, salary, description, post_date, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        values["title"],
                        values["category"],
                        values["experience"],
                        values["salary"],
                        values["description"],
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Open",
                    ),
                )
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Job posted successfully!")
                self.admin_panel()
            else:
                messagebox.showerror("Error", "All fields are required!")

        button_frame = tk.Frame(form_frame, bg=self.colors["white"])
        button_frame.pack(pady=20)

        self.create_styled_button(
            button_frame, "💾 Save Job", save_job, self.colors["success"]
        ).pack(side="left", padx=5)

        self.create_styled_button(
            button_frame, "⬅️ Back", self.admin_panel, self.colors["danger"]
        ).pack(side="left", padx=5)

    def user_panel(self):
        self.clear_screen()
        self.create_header(self.root, f"Welcome, {self.current_user}")

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Create notebook for tabs
        notebook = ttk.Notebook(container)
        notebook.pack(expand=True, fill="both")

        # Available Jobs tab
        jobs_frame = tk.Frame(notebook, bg=self.colors["bg"])
        notebook.add(jobs_frame, text="🔍 Available Jobs")

        # My Applications tab
        applications_frame = tk.Frame(notebook, bg=self.colors["bg"])
        notebook.add(applications_frame, text="📋 My Applications")

        self.populate_available_jobs(jobs_frame)
        self.populate_my_applications(applications_frame)

        # Logout button at bottom
        self.create_styled_button(
            container, "🚪 Logout", self.create_login_screen, self.colors["danger"]
        ).pack(pady=10)

    def populate_available_jobs(self, container):
        # Create Treeview
        columns = ("Title", "Category", "Experience", "Salary", "Posted Date")
        tree = ttk.Treeview(container, columns=columns, show="headings")

        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Add scrollbars
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")

        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Fetch jobs
        conn = sqlite3.connect("jobs.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, title, category, experience, salary, post_date
            FROM jobs
            WHERE status = 'Open'
            ORDER BY post_date DESC
        """
        )
        jobs = cursor.fetchall()
        conn.close()

        for job in jobs:
            tree.insert("", "end", values=job[1:], tags=(job[0],))

        def apply_for_job():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a job")
                return

            job_id = tree.item(selected_item[0])["tags"][0]

            # Check if already applied
            conn = sqlite3.connect("jobs.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM applications WHERE job_id = ? AND user_id = ?",
                (job_id, self.current_user),
            )
            if cursor.fetchone():
                messagebox.showinfo("Info", "You have already applied for this job")
                conn.close()
                return

            # Apply for job
            cursor.execute(
                """
                INSERT INTO applications (job_id, user_id, status, apply_date)
                VALUES (?, ?, ?, ?)
            """,
                (
                    job_id,
                    self.current_user,
                    "Pending",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Successfully applied for the job!")

        self.create_styled_button(
            container,
            "📝 Apply for Selected Job",
            apply_for_job,
            self.colors["success"],
        ).pack(pady=10)

    def populate_my_applications(self, container):
        # Create Treeview
        columns = ("Job Title", "Status", "Applied Date", "Feedback")
        tree = ttk.Treeview(container, columns=columns, show="headings")

        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Add scrollbars
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")

        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Fetch applications
        conn = sqlite3.connect("jobs.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT j.title, a.status, a.apply_date, COALESCE(a.feedback, 'No feedback yet')
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            WHERE a.user_id = ?
            ORDER BY a.apply_date DESC
        """,
            (self.current_user,),
        )
        applications = cursor.fetchall()
        conn.close()

        for app in applications:
            tree.insert("", "end", values=app)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    init_db()
    app = RojgarHub(root)
    root.mainloop()
