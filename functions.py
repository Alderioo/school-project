import sqlite3

def izveidot_datubazi():
    conn = sqlite3.connect('biblioteka.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Lietotajs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Vards TEXT,
        Uzvards TEXT,
        Vecums INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Autors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Vards TEXT,
        Uzvards TEXT,
        Valsts TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS valsti_no_kurienas_ir_gramatas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Valsts TEXT,
        Pilsēta TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS klientu_skaits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Klienta_kategorija TEXT,
        Dinamisks_skaits TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bibliotekas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Valsts TEXT,
        Pilsēta TEXT,
        Nosaukums TEXT UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS gramatas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Skaits TEXT,
        Nodotas TEXT,
        FOREIGN KEY (id) REFERENCES valsti_no_kurienas_ir_gramatas(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS gramatas_vesture (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Kad_nodota TEXT,
        Kad_atgriezta TEXT,
        Lietotaja_id INTEGER,
        Kur_glabjas TEXT,
        Nosaukums TEXT,
        FOREIGN KEY (Lietotaja_id) REFERENCES Lietotajs(id),
        FOREIGN KEY (Kur_glabjas) REFERENCES bibliotekas(Nosaukums)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS darbinieki (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Amats TEXT,
        Vards TEXT,
        Uzvards TEXT,
        Telefona_numurs TEXT,
        Vecums INTEGER,
        Dzimums TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS algas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Darbinieka_id INTEGER,
        Algas_daudzums REAL,
        FOREIGN KEY (Darbinieka_id) REFERENCES darbinieki(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sodi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Lietotaja_id INTEGER,
        Soda_daudzums REAL,
        Iemesls TEXT,
        Datums TEXT,
        FOREIGN KEY (Lietotaja_id) REFERENCES Lietotajs(id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Datu bāze un tabulas veiksmīgi izveidotas!")

if __name__ == '__main__':
    izveidot_datubazi()