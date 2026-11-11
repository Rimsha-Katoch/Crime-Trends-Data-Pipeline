
CREATE TABLE IF NOT EXISTS crime_records (
    id BIGINT PRIMARY KEY,
    date_time TIMESTAMP NOT NULL,
    type TEXT NOT NULL,
    subtype TEXT,
    location TEXT,
    description TEXT,
    last_updated TIMESTAMP,
    year INTEGER,
    month INTEGER,
    month_name TEXT,
    day INTEGER,
    day_name TEXT,
    hour INTEGER,
    time_period TEXT,
    year_month TEXT,
    is_weekend BOOLEAN
);
