import requests
import pandas as pd
import time
import sqlite3
from datetime import datetime

current_year = datetime.now().year
DB_PATH = "ferrari_f1.db"

def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drivers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        driver_id TEXT UNIQUE,
        code TEXT,
        forename TEXT,
        surname TEXT,
        nationality TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS constructors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        constructor_id TEXT UNIQUE,
        name TEXT,
        nationality TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS circuits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        circuit_id TEXT UNIQUE,
        name TEXT,
        location TEXT,
        country TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS races (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        race_id TEXT UNIQUE,
        year INTEGER,
        round INTEGER,
        race_name TEXT,
        date TEXT,
        circuit_id TEXT,
        FOREIGN KEY (circuit_id) REFERENCES circuits (circuit_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        race_id TEXT,
        driver_id TEXT,
        constructor_id TEXT,
        position INTEGER,
        points REAL,
        status TEXT,
        FOREIGN KEY (race_id) REFERENCES races (race_id),
        FOREIGN KEY (driver_id) REFERENCES drivers (driver_id),
        FOREIGN KEY (constructor_id) REFERENCES constructors (constructor_id)
    )
    """)

    conn.commit()

def insert_ignore(conn, table, data):
    keys = ', '.join(data.keys())
    question_marks = ', '.join(['?'] * len(data))
    sql = f"INSERT OR IGNORE INTO {table} ({keys}) VALUES ({question_marks})"
    conn.execute(sql, list(data.values()))

def load_f1_history(conn):
    for year in range(1950, current_year + 1):
        print(f"Année {year} (Ferrari only) ...")
        offset = 0
        batch_size = 100

        while True:
            url = f"https://ergast.com/api/f1/{year}/constructors/ferrari/results.json?limit={batch_size}&offset={offset}"
            r = requests.get(url)
            data = r.json()

            races = data['MRData']['RaceTable']['Races']
            if not races:
                break  # plus rien à paginer

            for race in races:
                race_id = f"{race['season']}_{race['round']}"

                circuit = race['Circuit']
                insert_ignore(conn, 'circuits', {
                    'circuit_id': circuit['circuitId'],
                    'name': circuit['circuitName'],
                    'location': circuit['Location']['locality'],
                    'country': circuit['Location']['country']
                })

                insert_ignore(conn, 'races', {
                    'race_id': race_id,
                    'year': int(race['season']),
                    'round': int(race['round']),
                    'race_name': race['raceName'],
                    'date': race['date'],
                    'circuit_id': circuit['circuitId']
                })

                for result in race['Results']:
                    driver = result['Driver']
                    constructor = result['Constructor']

                    insert_ignore(conn, 'drivers', {
                        'driver_id': driver['driverId'],
                        'code': driver.get('code'),
                        'forename': driver['givenName'],
                        'surname': driver['familyName'],
                        'nationality': driver['nationality']
                    })

                    insert_ignore(conn, 'constructors', {
                        'constructor_id': constructor['constructorId'],
                        'name': constructor['name'],
                        'nationality': constructor['nationality']
                    })

                    insert_ignore(conn, 'results', {
                        'race_id': race_id,
                        'driver_id': driver['driverId'],
                        'constructor_id': constructor['constructorId'],
                        'position': int(result['position']),
                        'points': float(result['points']),
                        'status': result['status']
                    })

            conn.commit()
            offset += batch_size
            time.sleep(1.2)

    print("Chargement Ferrari terminé.")



if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    load_f1_history(conn)
    conn.close()
