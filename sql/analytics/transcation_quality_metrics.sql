-- Transaction quality metrics analytics
-- This view aggregates quality metrics by failure reason and time period

CREATE OR REPLACE VIEW reliability.transaction_quality_metrics AS
SELECT
    DATE_TRUNC('day', created_at) AS day,
    failure_reason,
    COUNT(*) AS failed_count,
    COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY DATE_TRUNC('day', created_at)) AS failure_rate
FROM reliability.quarantine
GROUP BY 1, 2
ORDER BY 1 DESC, 3 DESC;

-- Additional metrics: overall success rate by day
CREATE OR REPLACE VIEW reliability.daily_success_rate AS
SELECT
    DATE_TRUNC('day', created_at) AS day,
    COUNT(CASE WHEN failure_reason IS NULL THEN 1 END) AS clean_count,
    COUNT(*) AS total_count,
    ROUND(COUNT(CASE WHEN failure_reason IS NULL THEN 1 END) / COUNT(*)::numeric, 4) AS success_rate
FROM (
    SELECT created_at, failure_reason FROM reliability.quarantine
    UNION ALL
    SELECT created_at, NULL AS failure_reason FROM reliability.clean_transactions
) AS all_transactions
GROUP BY 1
ORDER BY 1 DESC;
