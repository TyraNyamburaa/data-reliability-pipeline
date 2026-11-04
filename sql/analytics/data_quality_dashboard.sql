-- Data quality dashboard queries

CREATE OR REPLACE VIEW reliability.vw_transaction_quality_dashboard AS
SELECT
    DATE_TRUNC('day', load_timestamp) AS report_date,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (WHERE failure_reason IS NOT NULL) AS failed_count,
    COUNT(*) FILTER (WHERE failure_reason IS NULL) AS passed_count,
    ROUND(
        COUNT(*) FILTER (WHERE failure_reason IS NULL)::numeric / NULLIF(COUNT(*), 0) * 100,
        2
    ) AS pass_rate_percent
FROM (
    SELECT load_timestamp, NULL::VARCHAR AS failure_reason FROM reliability.clean_transactions
    UNION ALL
    SELECT load_timestamp, failure_reason FROM reliability.quarantine
) all_tx
GROUP BY DATE_TRUNC('day', load_timestamp)
ORDER BY report_date DESC;

CREATE OR REPLACE VIEW reliability.vw_failure_breakdown AS
SELECT
    failure_reason,
    COUNT(*) AS count,
    ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER () * 100, 2) AS percentage
FROM reliability.quarantine
GROUP BY failure_reason
ORDER BY count DESC;

CREATE OR REPLACE VIEW reliability.vw_daily_metrics AS
SELECT
    DATE_TRUNC('day', started_at) AS run_date,
    COUNT(*) AS pipeline_runs,
    SUM(processed_records) AS total_processed,
    SUM(passed_records) AS total_passed,
    SUM(failed_records) AS total_failed,
    AVG(failed_records::numeric / NULLIF(processed_records, 0)) * 100 AS avg_failure_rate_percent
FROM reliability.data_quality_runs
WHERE completed_at IS NOT NULL
GROUP BY DATE_TRUNC('day', started_at)
ORDER BY run_date DESC;
