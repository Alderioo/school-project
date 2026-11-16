import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).with_name("biblioteka.db")

def izveidot_datubazi():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS "Lietotajs" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "vards" TEXT NOT NULL,
        "uzvards" TEXT NOT NULL,
        "vecums" INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "Autors" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "vards" TEXT NOT NULL,
        "uzvards" TEXT NOT NULL,
        "valsts" TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "valstis" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "valsts" TEXT NOT NULL,
        "pilseta" TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "klientu_skaits" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "klienta_kategorija" TEXT NOT NULL,
        "dinamisks_skaits" INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "bibliotekas" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "valsts" TEXT NOT NULL,
        "pilseta" TEXT NOT NULL,
        "nosaukums" TEXT UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "gramatas" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "skaits" INTEGER NOT NULL,
        "nodotas" INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "gramatas_vesture" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "kad_nodota" TEXT NOT NULL,
        "kad_atgriezta" TEXT NOT NULL,
        "lietotaja_id" INTEGER NOT NULL,
        "kur_glabjas" TEXT NOT NULL,
        "nosaukums" TEXT NOT NULL,
        FOREIGN KEY ("lietotaja_id") REFERENCES "Lietotajs"("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("kur_glabjas") REFERENCES "bibliotekas"("nosaukums") ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "darbinieki" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "amats" TEXT NOT NULL,
        "vards" TEXT NOT NULL,
        "uzvards" TEXT NOT NULL,
        "telefona_numurs" INTEGER NOT NULL,
        "vecums" INTEGER NOT NULL,
        "dzimums" TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "algas" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "darbinieka_id" INTEGER NOT NULL,
        "algas_daudzums" INTEGER NOT NULL,
        FOREIGN KEY ("darbinieka_id") REFERENCES "darbinieki"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "Sodi" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "lietotaja_id" INTEGER NOT NULL,
        "soda_daudzums" INTEGER NOT NULL,
        "iemesls" TEXT NOT NULL,
        "datums" TEXT NOT NULL,
        FOREIGN KEY ("lietotaja_id") REFERENCES "Lietotajs"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );
    ''')


    cursor.executescript('''
    INSERT OR IGNORE INTO "Lietotajs" (id, vards, uzvards, vecums) VALUES
        (1, 'Jānis', 'Bērziņš', 25),
        (2, 'Anna', 'Kalniņa', 30),
        (3, 'Mārtiņš', 'Ozoliņš', 22);

    INSERT OR IGNORE INTO "Autors" (id, vards, uzvards, valsts) VALUES
        (1, 'Rainis', '', 'Latvija'),
        (2, 'Aspazija', '', 'Latvija');

    INSERT OR IGNORE INTO "valstis" (id, valsts, pilseta) VALUES
        (1, 'Latvija', 'Rīga'),
        (2, 'Lielbritānija', 'Londona');

    INSERT OR IGNORE INTO "klientu_skaits" (id, klienta_kategorija, dinamisks_skaits) VALUES
        (1, 'Studenti', '150'),
        (2, 'Pensionāri', '80');

    INSERT OR IGNORE INTO "bibliotekas" (id, valsts, pilseta, nosaukums) VALUES
        (1, 'Latvija', 'Rīga', 'Centrālā bibliotēka'),
        (2, 'Latvija', 'Liepāja', 'Pilsētas bibliotēka');

    INSERT OR IGNORE INTO "gramatas" (id, skaits, nodotas) VALUES
        (1, '100', '15'),
        (2, '50', '5');

    INSERT OR IGNORE INTO "gramatas_vesture" (id, kad_nodota, kad_atgriezta, lietotaja_id, kur_glabjas, nosaukums) VALUES
        (1, '2026-10-01', '2026-10-15', 1, 'Centrālā bibliotēka', 'Uguns un nakts');

    INSERT OR IGNORE INTO "darbinieki" (id, amats, vards, uzvards, telefona_numurs, vecums, dzimums) VALUES
        (1, 'Bibliotekārs', 'Ilze', 'Liepa', '+37120000000', 40, 'Sieviete');

    INSERT OR IGNORE INTO "algas" (id, darbinieka_id, algas_daudzums) VALUES
        (1, 1, 1200.50);

    INSERT OR IGNORE INTO "Sodi" (id, lietotaja_id, soda_daudzums, iemesls, datums) VALUES
        (1, 1, 5.00, 'Nokavēts termiņš', '2026-10-16');
    ''')

    conn.commit()
    conn.close()
    print("Datu bāze un tabulas veiksmīgi izveidotas!")

if __name__ == '__main__':
    izveidot_datubazi()
