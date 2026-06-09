-- KPI 1: National Waiting List
SELECT
SUM(total_incomplete_pathways) AS total_waiting_list
FROM rtt_waiting_list;

-- KPI 2: 52+ Weeks Waiting
SELECT
SUM(total_52_plus) AS total_52_plus_waits
FROM rtt_waiting_list;

-- KPI 3: National Performance Against 18 Weeks
SELECT
ROUND(
SUM(total_within_18_weeks)::numeric
/
NULLIF(SUM(total_incomplete_pathways),0),
4
) AS national_pct_within_18_weeks
FROM rtt_waiting_list;

-- KPI 4: Top 10 Trusts by Waiting List
SELECT
provider_name,
SUM(total_incomplete_pathways) waiting_list
FROM rtt_waiting_list
GROUP BY provider_name
ORDER BY waiting_list DESC
LIMIT 10;

-- KPI 5: Worst Specialties
SELECT
treatment_function,
SUM(total_incomplete_pathways) waiting_list
FROM rtt_waiting_list
GROUP BY treatment_function
ORDER BY waiting_list DESC
LIMIT 20;
