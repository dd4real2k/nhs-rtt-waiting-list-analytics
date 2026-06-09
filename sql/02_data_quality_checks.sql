-- NHS RTT data quality checks

-- 1. Check total row count
SELECT COUNT(*) AS total_rows
FROM rtt_waiting_list;

-- 2. Check missing provider identifiers
SELECT *
FROM rtt_waiting_list
WHERE provider_code IS NULL
   OR provider_name IS NULL;

-- 3. Check missing treatment function identifiers
SELECT *
FROM rtt_waiting_list
WHERE treatment_function_code IS NULL
   OR treatment_function IS NULL;

-- 4. Check negative waiting list values
SELECT *
FROM rtt_waiting_list
WHERE total_incomplete_pathways < 0
   OR total_within_18_weeks < 0
   OR total_52_plus < 0
   OR total_65_plus < 0
   OR total_78_plus < 0;

-- 5. Check invalid percentages
SELECT *
FROM rtt_waiting_list
WHERE pct_within_18_weeks < 0
   OR pct_within_18_weeks > 1
   OR pct_52_plus < 0
   OR pct_52_plus > 1;

-- 6. Check impossible logic:
-- patients within 18 weeks should not exceed total incomplete pathways
SELECT *
FROM rtt_waiting_list
WHERE total_within_18_weeks > total_incomplete_pathways;

-- 7. Check long waits logic:
-- 78+ waits should not exceed 65+ waits, and 65+ waits should not exceed 52+ waits
SELECT *
FROM rtt_waiting_list
WHERE total_78_plus > total_65_plus
   OR total_65_plus > total_52_plus;

-- 8. Check duplicate provider-specialty-month records
SELECT
    reporting_month,
    provider_code,
    treatment_function_code,
    COUNT(*) AS duplicate_count
FROM rtt_waiting_list
GROUP BY reporting_month, provider_code, treatment_function_code
HAVING COUNT(*) > 1;
