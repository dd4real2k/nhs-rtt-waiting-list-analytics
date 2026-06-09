-- Phase 4: NHS RTT KPI Summary Report

-- 1. National headline KPIs
SELECT
    reporting_month,
    SUM(total_incomplete_pathways) AS total_waiting_list,
    SUM(total_within_18_weeks) AS total_within_18_weeks,
    ROUND(
        SUM(total_within_18_weeks)::numeric / NULLIF(SUM(total_incomplete_pathways), 0),
        4
    ) AS pct_within_18_weeks,
    SUM(total_52_plus) AS total_52_plus,
    SUM(total_65_plus) AS total_65_plus,
    SUM(total_78_plus) AS total_78_plus
FROM rtt_waiting_list
GROUP BY reporting_month;


-- 2. Top 10 providers by total waiting list
SELECT
    provider_code,
    provider_name,
    SUM(total_incomplete_pathways) AS total_waiting_list
FROM rtt_waiting_list
GROUP BY provider_code, provider_name
ORDER BY total_waiting_list DESC
LIMIT 10;


-- 3. Top 10 treatment functions by waiting list
SELECT
    treatment_function_code,
    treatment_function,
    SUM(total_incomplete_pathways) AS total_waiting_list,
    SUM(total_52_plus) AS waits_52_plus
FROM rtt_waiting_list
GROUP BY treatment_function_code, treatment_function
ORDER BY total_waiting_list DESC
LIMIT 10;


-- 4. Providers with highest long-wait pressure
SELECT
    provider_code,
    provider_name,
    SUM(total_incomplete_pathways) AS total_waiting_list,
    SUM(total_52_plus) AS waits_52_plus,
    ROUND(
        SUM(total_52_plus)::numeric / NULLIF(SUM(total_incomplete_pathways), 0),
        4
    ) AS pct_52_plus
FROM rtt_waiting_list
GROUP BY provider_code, provider_name
HAVING SUM(total_incomplete_pathways) > 0
ORDER BY pct_52_plus DESC
LIMIT 10;


-- 5. Provider-specialty combinations with longest median waits
SELECT
    provider_name,
    treatment_function,
    total_incomplete_pathways,
    median_wait_weeks,
    p92_wait_weeks,
    total_52_plus
FROM rtt_waiting_list
WHERE median_wait_weeks IS NOT NULL
ORDER BY median_wait_weeks DESC
LIMIT 20;
