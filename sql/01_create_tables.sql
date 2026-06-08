-- sql/01_create_tables.sql

CREATE TABLE rtt_waiting_list (
    id SERIAL PRIMARY KEY,
    provider_code VARCHAR(20),
    provider_name VARCHAR(255),
    specialty VARCHAR(255),
    reporting_month DATE,
    waiting_patients INTEGER
);
