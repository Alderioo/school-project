from contextlib import closing
from pathlib import Path
import sqlite3

DATABASE_PATH = Path(__file__).with_name("biblioteka.db")


def connect():
  database = sqlite3.connect(DATABASE_PATH)
  database.execute("PRAGMA foreign_keys = ON")
  return database


def add_Lietotajs(vards, uzvards, vecums):
  with closing(connect()) as database:
    with database:
      cursor = database.execute(
          'INSERT INTO "Lietotajs" (vards, uzvards, vecums) VALUES (?, ?, ?)',
          (vards, uzvards, vecums),
      )
      return cursor.lastrowid


def add_Autors(vards, uzvards, valsts):
  with closing(connect()) as database:
    with database:
      cursor = database.execute(
          'INSERT INTO "Autors" (vards, uzvards, valsts) VALUES (?, ?, ?)',
          (vards, uzvards, valsts),
      )
      return cursor.lastrowid


def add_valstis(valsts, pilseta):
  with closing(connect()) as database:
    with database:
      cursor = database.execute(
          'INSERT INTO "valstis" (valsts, pilseta) VALUES (?, ?)',
          (valsts, pilseta),
      )
      return cursor.lastrowid


def add_bibliotekas(valsts_id, nosaukums):
  with closing(connect()) as database:
    with database:
      cursor = database.execute(
          'INSERT INTO "bibliotekas" (valsts_id, nosaukums) VALUES (?, ?)',
          (valsts_id, nosaukums),
      )
      return cursor.lastrowid


def add_klientu_skaits(bibliotekas_id, klienta_kategorija, dinamisks_skaits):
  with closing(connect()) as database:
    with database:
      cursor = database.execute(
          'INSERT INTO "klientu_skaits" (bibliotekas_id, klienta_kategorija,'
          " dinamisks_skaits) VALUES (?, ?, ?)",
          (bibliotekas_id, klienta_kategorija, dinamisks_skaits),
      )
      return cursor.lastrowid


def add_gramatas(bibliotekas_id, autora_id, nosaukums, skaits, nodotas):
  with closing(connect()) as database:
    with database:
      cursor = database.execute(
          'INSERT INTO "gramatas" (bibliotekas_id, autora_id, nosaukums,'
          " skaits, nodotas) VALUES (?, ?, ?, ?, ?)",
          (bibliotekas_id, autora_id, nosaukums, skaits, nodotas),
      )
      return cursor.lastrowid


def add_gramatas_vesture(
    gramatas_id, lietotaja_id, bibliotekas_id, kad_nodota, kad_atgriezta
):
  with closing(connect()) as database:
    with database:
      cursor = database.execute(
          'INSERT INTO "gramatas_vesture" (gramatas_id, lietotaja_id,'
          " bibliotekas_id, kad_nodota, kad_atgriezta) VALUES (?, ?, ?, ?,"
          " ?)",
          (gramatas_id, lietotaja_id, bibliotekas_id, kad_nodota, kad_atgriezta),
      )
      return cursor.lastrowid


def add_darbinieki(amats, vards, uzvards, telefona_numurs, vecums, dzimums):
  with closing(connect()) as database:
    with database:
      cursor = database.execute(
          'INSERT INTO "darbinieki" (amats, vards, uzvards, telefona_numurs,'
          " vecums, dzimums) VALUES (?, ?, ?, ?, ?, ?)",
          (amats, vards, uzvards, telefona_numurs, vecums, dzimums),
      )
      return cursor.lastrowid


def add_algas(darbinieka_id, algas_daudzums):
  with closing(connect()) as database:
    with database:
      cursor = database.execute(
          'INSERT INTO "algas" (darbinieka_id, algas_daudzums) VALUES (?, ?)',
          (darbinieka_id, algas_daudzums),
      )
      return cursor.lastrowid


def add_Sodi(lietotaja_id, soda_daudzums, iemesls, datums):
  with closing(connect()) as database:
    with database:
      cursor = database.execute(
          'INSERT INTO "Sodi" (lietotaja_id, soda_daudzums, iemesls, datums)'
          " VALUES (?, ?, ?, ?)",
          (lietotaja_id, soda_daudzums, iemesls, datums),
      )
      return cursor.lastrowid


def get_Lietotajs():
  with closing(connect()) as database:
    return database.execute(
        'SELECT id, vards, uzvards, vecums FROM "Lietotajs" ORDER BY id'
    ).fetchall()


def get_Autors():
  with closing(connect()) as database:
    return database.execute(
        'SELECT id, vards, uzvards, valsts FROM "Autors" ORDER BY id'
    ).fetchall()


def get_valstis():
  with closing(connect()) as database:
    return database.execute(
        'SELECT id, valsts, pilseta FROM "valstis" ORDER BY id'
    ).fetchall()


def get_bibliotekas():
  with closing(connect()) as database:
    return database.execute(
        'SELECT id, valsts_id, nosaukums FROM "bibliotekas" ORDER BY id'
    ).fetchall()


def get_klientu_skaits():
  with closing(connect()) as database:
    return database.execute(
        'SELECT id, bibliotekas_id, klienta_kategorija, dinamisks_skaits FROM'
        ' "klientu_skaits" ORDER BY id'
    ).fetchall()


def get_gramatas():
  with closing(connect()) as database:
    return database.execute(
        'SELECT id, bibliotekas_id, autora_id, nosaukums, skaits, nodotas FROM'
        ' "gramatas" ORDER BY id'
    ).fetchall()


def get_gramatas_vesture():
  with closing(connect()) as database:
    return database.execute(
        'SELECT id, gramatas_id, lietotaja_id, bibliotekas_id, kad_nodota,'
        ' kad_atgriezta FROM "gramatas_vesture" ORDER BY id'
    ).fetchall()


def get_darbinieki():
  with closing(connect()) as database:
    return database.execute(
        'SELECT id, amats, vards, uzvards, telefona_numurs, vecums, dzimums'
        ' FROM "darbinieki" ORDER BY id'
    ).fetchall()


def get_algas():
  with closing(connect()) as database:
    return database.execute(
        'SELECT id, darbinieka_id, algas_daudzums FROM "algas" ORDER BY id'
    ).fetchall()


def get_Sodi():
  with closing(connect()) as database:
    return database.execute(
        'SELECT id, lietotaja_id, soda_daudzums, iemesls, datums FROM "Sodi"'
        " ORDER BY id"
    ).fetchall()


def delete_record(table, record_id):
  with closing(connect()) as database:
    with database:
      cursor = database.execute(
          f'DELETE FROM "{table}" WHERE id = ?', (record_id,)
      )
      return cursor.rowcount


def update_record(table, columns, values, record_id):
  assignments = ", ".join(f"{column} = ?" for column in columns)
  with closing(connect()) as database:
    with database:
      cursor = database.execute(
          f'UPDATE "{table}" SET {assignments} WHERE id = ?',
          (*values, record_id),
      )
      return cursor.rowcount


def search_records(table, column, pattern):
  with closing(connect()) as database:
    return database.execute(
        f'SELECT * FROM "{table}" WHERE {column} LIKE ? ORDER BY id',
        (pattern,),
    ).fetchall()
