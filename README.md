# Ferrari F1 Dashboard

This project offers an interactive dashboard showcasing the historical performance of the Ferrari Formula 1 team, based on public data from the Ergast Developer API.

The goal is to build a complete data engineering pipeline:
- Extract and transform race results from 1950 onwards
- Store the data in a structured relational SQLite database
- Visualize insights through an interactive Streamlit dashboard

## Database

The `ferrari_f1.db` database contains the following tables:
- `drivers`
- `constructors`
- `circuits`
- `races`
- `results`
Data is retrieved from the Ergast API using full pagination to ensure complete historical coverage.

This project uses SQLite as the relational database engine. SQLite is lightweight, requires no configuration, and is ideal for personal projects or single-user dashboards.

## Dashboard Features

- Total points, wins, podiums, and retirements
- Performance trends by season
- Ferrari driver rankings by total points
- Interactive filter to explore individual driver performance

## Deploy

https://pierre-graef-scuderia-ferrari-dashboard.streamlit.app/

## Author

Pierre Graef

https://www.pierregraef.com/

graef.pierre@gmail.com

## Installation

```bash
git clone https://github.com/PierreGR7/ferrari_f1_db.git
cd ferrari_f1_db
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python etl_ferrari.py
streamlit run dashboard/app.py
