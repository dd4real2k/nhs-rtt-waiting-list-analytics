-- NHS RTT data quality checks

-- 1. Missing provider identifiers
SELECT *
FROM rtt_waiting_list
WHERE provider_code IS NULL
   OR provider_name IS NULL;

-- 2. Missing treatment function identifiers
SELECT *
FROM rtt_waiting_list
WHERE treatment_function_code IS NULL
   OR treatment_function IS NULL;

-- 3. Negative activity values
SELECT *
FROM rtt_waiting_list
WHERE total_incomplete_pathways < 0
   OR total_within_18_weeks < 0
   OR total_52_plus < 0
   OR total_65_plus < 0
   OR total_78_plus < 0;

-- 4. Percentages outside expected 0-1 range
SELECT *
FROM rtt_waiting_list
WHERE pct_within_18_weeks < 0
   OR pct_within_18_weeks > 1
   OR pct_52_plus < 0
   OR pct_52_plus > 1;

-- 5. Logical consistency: within 18 weeks should not exceed total incomplete pathways
SELECT *
FROM rtt_waiting_list
WHERE total_within_18_weeks > total_incomplete_pathways;

-- 6. Long-wait hierarchy check: 78+ should not exceed 65+, and 65+ should not exceed 52+
SELECT *
FROM rtt_waiting_list
WHERE total_78_plus > total_65_plus
   OR total_65_plus > total_52_plus;

-- 7. Duplicate provider-specialty rows for same reporting month
SELECT
    reporting_month,
    provider_code,
    treatment_function_code,
    COUNT(*) AS row_count
FROM rtt_waiting_list
GROUP BY reporting_month, provider_code, treatment_function_code
HAVING COUNT(*) > 1;
