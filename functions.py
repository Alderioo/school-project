import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).with_name("biblioteka.db")


def izveidot_datubazi():
  conn = sqlite3.connect(DATABASE_PATH)
  cursor = conn.cursor()

  cursor.execute("PRAGMA foreign_keys = ON;")

  cursor.executescript("""
    CREATE TABLE IF NOT EXISTS "valstis" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "valsts" TEXT NOT NULL,
        "pilseta" TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "Autors" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "vards" TEXT NOT NULL,
        "uzvards" TEXT NOT NULL,
        "valsts" TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "Lietotajs" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "vards" TEXT NOT NULL,
        "uzvards" TEXT NOT NULL,
        "vecums" INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS "bibliotekas" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "valsts_id" INTEGER NOT NULL,
        "nosaukums" TEXT UNIQUE NOT NULL,
        FOREIGN KEY ("valsts_id") REFERENCES "valstis"("id") ON UPDATE CASCADE ON DELETE RESTRICT
    );

    CREATE TABLE IF NOT EXISTS "klientu_skaits" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "bibliotekas_id" INTEGER NOT NULL,
        "klienta_kategorija" TEXT NOT NULL,
        "dinamisks_skaits" INTEGER NOT NULL,
        FOREIGN KEY ("bibliotekas_id") REFERENCES "bibliotekas"("id") ON UPDATE CASCADE ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS "gramatas" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "bibliotekas_id" INTEGER NOT NULL,
        "autora_id" INTEGER NOT NULL,
        "nosaukums" TEXT NOT NULL,
        "skaits" INTEGER NOT NULL,
        "nodotas" INTEGER NOT NULL,
        FOREIGN KEY ("bibliotekas_id") REFERENCES "bibliotekas"("id") ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY ("autora_id") REFERENCES "Autors"("id") ON UPDATE CASCADE ON DELETE RESTRICT
    );

    CREATE TABLE IF NOT EXISTS "gramatas_vesture" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "gramatas_id" INTEGER NOT NULL,
        "lietotaja_id" INTEGER NOT NULL,
        "bibliotekas_id" INTEGER NOT NULL,
        "kad_nodota" TEXT NOT NULL,
        "kad_atgriezta" TEXT NOT NULL,
        FOREIGN KEY ("gramatas_id") REFERENCES "gramatas"("id") ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY ("lietotaja_id") REFERENCES "Lietotajs"("id") ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY ("bibliotekas_id") REFERENCES "bibliotekas"("id") ON UPDATE CASCADE ON DELETE RESTRICT
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
        FOREIGN KEY ("darbinieka_id") REFERENCES "darbinieki"("id") ON UPDATE CASCADE ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS "Sodi" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "lietotaja_id" INTEGER NOT NULL,
        "soda_daudzums" INTEGER NOT NULL,
        "iemesls" TEXT NOT NULL,
        "datums" TEXT NOT NULL,
        FOREIGN KEY ("lietotaja_id") REFERENCES "Lietotajs"("id") ON UPDATE CASCADE ON DELETE CASCADE
    );
    """)

  cursor.executescript("""
    INSERT OR IGNORE INTO "valstis" (id, valsts, pilseta) VALUES
        (1, 'Latvija', 'Rīga'),
        (2, 'Latvija', 'Liepāja'),
        (3, 'Lielbritānija', 'Londona');

    INSERT OR IGNORE INTO "Autors" (id, vards, uzvards, valsts) VALUES
        (1, 'Rainis', '', 'Latvija'),
        (2, 'Aspazija', '', 'Latvija');

    INSERT OR IGNORE INTO "Lietotajs" (id, vards, uzvards, vecums) VALUES
        (1, 'Jānis', 'Bērziņš', 25),
        (2, 'Anna', 'Kalniņa', 30),
        (3, 'Mārtiņš', 'Ozoliņš', 22);

    INSERT OR IGNORE INTO "bibliotekas" (id, valsts_id, nosaukums) VALUES
        (1, 1, 'Centrālā bibliotēka'),
        (2, 2, 'Pilsētas bibliotēka');

    INSERT OR IGNORE INTO "klientu_skaits" (id, bibliotekas_id, klienta_kategorija, dinamisks_skaits) VALUES
        (1, 1, 'Studenti', 150),
        (2, 1, 'Pensionāri', 80);

    INSERT OR IGNORE INTO "gramatas" (id, bibliotekas_id, autora_id, nosaukums, skaits, nodotas) VALUES
        (1, 1, 1, 'Uguns un nakts', 100, 15),
        (2, 2, 2, 'Sudraba šķidrauts', 50, 5);

    INSERT OR IGNORE INTO "gramatas_vesture" (id, gramatas_id, lietotaja_id, bibliotekas_id, kad_nodota, kad_atgriezta) VALUES
        (1, 1, 1, 1, '2026-10-01', '2026-10-15');

    INSERT OR IGNORE INTO "darbinieki" (id, amats, vards, uzvards, telefona_numurs, vecums, dzimums) VALUES
        (1, 'Bibliotekārs', 'Ilze', 'Liepa', 37120000000, 40, 'Sieviete');

    INSERT OR IGNORE INTO "algas" (id, darbinieka_id, algas_daudzums) VALUES
        (1, 1, 1200);

    INSERT OR IGNORE INTO "Sodi" (id, lietotaja_id, soda_daudzums, iemesls, datums) VALUES
        (1, 1, 5, 'Nokavēts termiņš', '2026-10-16');
    """)

  conn.commit()
  conn.close()
  print("Datu bāze un tabulas veiksmīgi izveidotas!")


if __name__ == "__main__":
  izveidot_datubazi()
