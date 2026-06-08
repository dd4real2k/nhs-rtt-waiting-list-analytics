CREATE TABLE rtt_waiting_list (
    reporting_month DATE,

    region_code VARCHAR(20),

    provider_code VARCHAR(20),

    provider_name VARCHAR(255),

    treatment_function_code VARCHAR(50),

    treatment_function VARCHAR(255),

    total_incomplete_pathways INTEGER,

    total_within_18_weeks INTEGER,

    pct_within_18_weeks NUMERIC(10,4),

    median_wait_weeks NUMERIC(10,2),

    p92_wait_weeks NUMERIC(10,2),

    total_52_plus INTEGER,

    total_65_plus INTEGER,

    total_78_plus INTEGER,

    pct_52_plus NUMERIC(10,4)
);
