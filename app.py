import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

import main as db

TABLES = {
    "Lietotajs": ["vards", "uzvards", "vecums"],
    "Autors": ["vards", "uzvards", "valsts"],
    "valstis": ["valsts", "pilseta"],
    "klientu_skaits": ["klienta_kategorija", "dinamisks_skaits"],
    "bibliotekas": ["valsts", "pilseta", "nosaukums"],
    "gramatas": ["skaits", "nodotas"],
    "gramatas_vesture": [
        "kad_nodota",
        "kad_atgriezta",
        "lietotaja_id",
        "kur_glabjas",
        "nosaukums",
    ],
    "darbinieki": [
        "amats",
        "vards",
        "uzvards",
        "telefona_numurs",
        "vecums",
        "dzimums",
    ],
    "algas": ["darbinieka_id", "algas_daudzums"],
    "Sodi": ["lietotaja_id", "soda_daudzums", "iemesls", "datums"],
}


class InputModal(tk.Toplevel):

  def __init__(self, parent, title, columns, current_values=None):
    super().__init__(parent)
    self.title(title)
    self.geometry("450x500")
    self.configure(bg="#0f111a")
    self.resizable(False, False)

    self.transient(parent)
    self.grab_set()

    self.columns = columns
    self.current_values = current_values
    self.result = None

    self.create_widgets()

    self.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
    y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
    self.geometry(f"+{x}+{y}")

  def create_widgets(self):
    main_frame = ttk.Frame(self, padding=20)
    main_frame.pack(fill="both", expand=True)

    title_label = ttk.Label(
        main_frame, text=self.title(), font=("Segoe UI", 12, "bold")
    )
    title_label.pack(anchor="w", pady=(0, 15))

    fields_card = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
    fields_card.pack(fill="both", expand=True, pady=(0, 15))

    self.entries = {}
    for i, column in enumerate(self.columns):
      lbl = ttk.Label(fields_card, text=column.replace("_", " ").capitalize())
      lbl.pack(anchor="w", pady=(5, 2))

      entry = ttk.Entry(fields_card, width=35)
      entry.pack(fill="x", pady=(0, 10))

      if self.current_values and i < len(self.current_values):
        entry.insert(0, str(self.current_values[i]))

      self.entries[column] = entry

    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(fill="x", pady=(5, 0))

    save_btn = ttk.Button(
        btn_frame,
        text="Saglabāt",
        style="Accent.TButton",
        command=self.on_save,
    )
    save_btn.pack(side="right", padx=(8, 0))

    cancel_btn = ttk.Button(
        btn_frame, text="Atcelt", command=self.destroy
    )
    cancel_btn.pack(side="right")

    first_key = list(self.entries.keys())[0]
    self.entries[first_key].focus_set()

  def on_save(self):
    values = []
    
    numeric_columns = ["vecums", "telefona_numurs", "skaits", "dinamisks_skaits", "algas_daudzums", "soda_daudzums", "lietotaja_id", "darbinieka_id"]
    
    text_columns = ["vards", "uzvards", "valsts", "pilseta", "nosaukums", "amats", "dzimums", "iemesls", "klienta_kategorija"]

    for column in self.columns:
      val = self.entries[column].get().strip()

      if column in numeric_columns:
        if not val.isdigit(): 
          messagebox.showerror(
              "Kļūda",
              f"Laukā '{column}' drīkst ievadīt TIKAI ciparus!",
              parent=self,
          )
          return  
      elif column in text_columns:
        if val.isdigit():
          messagebox.showerror(
              "Kļūda",
              f"Laukā '{column}' drīkst ievadīt TIKAI tekstu (nevis ciparus)!",
              parent=self,
          )
          return 

      if val.isdigit():
        values.append(int(val))
      else:
        try:
          values.append(float(val))
        except ValueError:
          values.append(val)

    self.result = values
    self.destroy()


class LibraryApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Nexus Library System")
    self.root.geometry("1200x700")
    self.root.configure(bg="#0f111a")

    self.setup_styles()

    self.table_var = tk.StringVar(value=list(TABLES.keys())[0])
    self.search_field_var = tk.StringVar()

    self.create_widgets()
    self.load_table()

  def setup_styles(self):
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        ".",
        background="#0f111a",
        foreground="#ffffff",
        fieldbackground="#161821",
        troughcolor="#161821",
        selectbackground="#3b4261",
        selectforeground="#ffffff",
        font=("Segoe UI", 10),
    )

    style.configure("TFrame", background="#0f111a")
    style.configure("Card.TFrame", background="#1a1b26", relief="flat")

    style.configure(
        "TLabel",
        background="#1a1b26",
        foreground="#7aa2f7",
        font=("Segoe UI", 10, "bold"),
    )
    style.configure(
        "Header.TLabel",
        background="#1a1b26",
        foreground="#bb9af7",
        font=("Segoe UI", 11, "bold"),
    )

    style.configure(
        "TButton",
        background="#3b82f6",
        foreground="#ffffff",
        borderwidth=0,
        focusthickness=0,
        font=("Segoe UI", 10, "bold"),
        padding=8,
    )
    style.map(
        "TButton",
        background=[("active", "#2563eb"), ("pressed", "#1d4ed8")],
    )

    style.configure(
        "Accent.TButton",
        background="#10b981",
        foreground="#ffffff",
        font=("Segoe UI", 10, "bold"),
        padding=8,
    )
    style.map(
        "Accent.TButton",
        background=[("active", "#059669"), ("pressed", "#047857")],
    )

    style.configure(
        "Danger.TButton",
        background="#ef4444",
        foreground="#ffffff",
        font=("Segoe UI", 10, "bold"),
        padding=8,
    )
    style.map(
        "Danger.TButton",
        background=[("active", "#dc2626"), ("pressed", "#b91c1c")],
    )

    style.configure(
        "TCombobox",
        fieldbackground="#161821",
        background="#1a1b26",
        foreground="#f10000",
        arrowcolor="#7aa2f7",
        borderwidth=1,
    )

    style.configure(
        "TEntry",
        fieldbackground="#161821",
        foreground="#0ee232",
        insertcolor="#ffffff",
        borderwidth=1,
    )

    style.configure(
        "Treeview",
        background="#161821",
        foreground="#c0caf5",
        fieldbackground="#161821",
        borderwidth=0,
        rowheight=35,
        font=("Segoe UI", 10),
    )
    style.configure(
        "Treeview.Heading",
        background="#1f2335",
        foreground="#7aa2f7",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padding=8,
    )
    style.map(
        "Treeview",
        background=[("selected", "#3b4261")],
        foreground=[("selected", "#ffffff")],
    )

  def create_widgets(self):
    main_container = ttk.Frame(self.root, padding=20)
    main_container.pack(fill="both", expand=True)

    top_frame = ttk.Frame(main_container, style="Card.TFrame", padding=15)
    top_frame.pack(fill="x", pady=(0, 15))

    ttk.Label(top_frame, text="TABULA:", style="Header.TLabel").pack(
        side="left", padx=(0, 8)
    )
    self.table_box = ttk.Combobox(
        top_frame,
        textvariable=self.table_var,
        values=list(TABLES.keys()),
        state="readonly",
        width=18,
    )
    self.table_box.pack(side="left", padx=(0, 25))
    self.table_box.bind("<<ComboboxSelected>>", self.load_table)

    ttk.Label(top_frame, text="ПОИСК ПО:", style="Header.TLabel").pack(
        side="left", padx=(0, 8)
    )
    self.search_field_box = ttk.Combobox(
        top_frame,
        textvariable=self.search_field_var,
        state="readonly",
        width=16,
    )
    self.search_field_box.pack(side="left", padx=(0, 10))

    self.search_entry = ttk.Entry(top_frame, width=22)
    self.search_entry.pack(side="left", padx=(0, 10))
    self.search_entry.bind("<Return>", self.search)

    ttk.Button(top_frame, text="🔍 Meklēt", command=self.search).pack(
        side="left", padx=(0, 8)
    )
    ttk.Button(top_frame, text="🔄 Atiestatīt", command=self.load_table).pack(
        side="left"
    )

    tree_container = ttk.Frame(main_container, style="Card.TFrame", padding=5)
    tree_container.pack(fill="both", expand=True, pady=(0, 15))

    self.tree = ttk.Treeview(
        tree_container, show="headings", selectmode="browse"
    )
    scrollbar = ttk.Scrollbar(
        tree_container, orient="vertical", command=self.tree.yview
    )
    self.tree.configure(yscrollcommand=scrollbar.set)

    self.tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    buttons_frame = ttk.Frame(main_container)
    buttons_frame.pack(fill="x")

    ttk.Button(
        buttons_frame,
        text="+ Pievienot ierakstu",
        style="Accent.TButton",
        command=self.add_record,
    ).pack(side="left", padx=(0, 12))
    ttk.Button(
        buttons_frame, text="✏ Rediģēt izvēlēto", command=self.edit_record
    ).pack(side="left", padx=(0, 12))
    ttk.Button(
        buttons_frame,
        text="🗑 Dzēst izvēlēto",
        style="Danger.TButton",
        command=self.delete_record,
    ).pack(side="left")

  def show_rows(self, rows, columns):
    self.tree.delete(*self.tree.get_children())
    self.tree["columns"] = columns
    for column in columns:
      self.tree.heading(column, text=column.upper())
      self.tree.column(column, width=160, anchor="w")

    for index, row in enumerate(rows):
      tag = "even" if index % 2 == 0 else "odd"
      self.tree.insert("", "end", iid=str(row[0]), values=row, tags=(tag,))

    self.tree.tag_configure("even", background="#161821", foreground="#c0caf5")
    self.tree.tag_configure("odd", background="#1a1b26", foreground="#c0caf5")

  def load_table(self, event=None):
    table = self.table_var.get()
    columns = TABLES[table]
    self.search_field_box["values"] = columns
    self.search_field_var.set(columns[0])
    try:
      rows = getattr(db, "get_" + table)()
      self.show_rows(rows, ["id"] + columns)
    except AttributeError:
      messagebox.showerror(
          "Kļūda", f"Funkcija get_{table} nav atrasta modulī main.py"
      )

  def search(self, event=None):
    text = self.search_entry.get().strip()
    if not text:
      self.load_table()
      return
    table = self.table_var.get()
    try:
      rows = db.search_records(table, self.search_field_var.get(), f"%{text}%")
      self.show_rows(rows, ["id"] + TABLES[table])
    except AttributeError:
      messagebox.showerror(
          "Kļūda", "Funkcija search_records nav atrasta modulī main.py"
      )

  def selected_id(self):
    selection = self.tree.selection()
    if not selection:
      messagebox.showinfo("Uzmanību", "Vispirms izvēlieties ierakstu.")
      return None
    return selection[0]

  def add_record(self):
    table = self.table_var.get()
    modal = InputModal(
        self.root, f"Pievienot ierakstu: {table}", TABLES[table]
    )
    self.root.wait_window(modal)  # Ждем закрытия кастомного окна

    if modal.result:
      try:
        getattr(db, "add_" + table)(*modal.result)
        self.load_table()
      except sqlite3.Error as error:
        messagebox.showerror("Datubāzes kļūda", str(error))

  def edit_record(self):
    record_id = self.selected_id()
    if not record_id:
      return
    table = self.table_var.get()
    current_values = self.tree.item(record_id, "values")[1:]

    modal = InputModal(
        self.root,
        f"Rediģēt ierakstu #{record_id} ({table})",
        TABLES[table],
        current_values,
    )
    self.root.wait_window(modal)

    if modal.result is not None:
      try:
        db.update_record(table, TABLES[table], modal.result, int(record_id))
        self.load_table()
      except sqlite3.Error as error:
        messagebox.showerror("Datubāzes kļūda", str(error))

  def delete_record(self):
    record_id = self.selected_id()
    if not record_id:
      return
    if messagebox.askyesno(
        "Apstiprinājums", f"Vai tiešām vēlaties dzēst ierakstu #{record_id}?"
    ):
      try:
        db.delete_record(self.table_var.get(), int(record_id))
        self.load_table()
      except sqlite3.Error as error:
        messagebox.showerror("Datubāzes kļūda", str(error))


if __name__ == "__main__":
  root = tk.Tk()
  app = LibraryApp(root)
  root.mainloop()
