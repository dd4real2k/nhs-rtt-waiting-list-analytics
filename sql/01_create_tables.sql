DROP TABLE IF EXISTS rtt_waiting_list;

CREATE TABLE rtt_waiting_list (
    reporting_month DATE NOT NULL,
    region_code VARCHAR(20) NOT NULL,
    provider_code VARCHAR(20) NOT NULL,
    provider_name VARCHAR(255) NOT NULL,
    treatment_function_code VARCHAR(20) NOT NULL,
    treatment_function VARCHAR(255) NOT NULL,
    total_incomplete_pathways INTEGER,
    total_within_18_weeks INTEGER,
    pct_within_18_weeks NUMERIC(10,6),
    median_wait_weeks NUMERIC(10,2),
    p92_wait_weeks NUMERIC(10,2),
    total_52_plus INTEGER,
    total_65_plus INTEGER,
    total_78_plus INTEGER,
    pct_52_plus NUMERIC(10,6)
);

CREATE INDEX idx_rtt_provider_code ON rtt_waiting_list(provider_code);
CREATE INDEX idx_rtt_treatment_function_code ON rtt_waiting_list(treatment_function_code);
CREATE INDEX idx_rtt_reporting_month ON rtt_waiting_list(reporting_month);
