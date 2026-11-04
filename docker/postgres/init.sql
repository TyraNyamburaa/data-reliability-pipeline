CREATE SCHEMA IF NOT EXISTS reliability;

COMMENT ON SCHEMA reliability IS 'Data reliability pipeline objects';

CREATE TABLE IF NOT EXISTS reliability.transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50),
    agent_id VARCHAR(50),
    region VARCHAR(100),
    transaction_date DATE,
    amount NUMERIC(15, 2),
    currency VARCHAR(10),
    status VARCHAR(20),
    payment_method VARCHAR(50),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_file VARCHAR(255),
    CONSTRAINT uq_reliability_transactions_tx UNIQUE (transaction_id)
);

CREATE INDEX IF NOT EXISTS idx_reliability_transactions_date ON reliability.transactions (transaction_date);
CREATE INDEX IF NOT EXISTS idx_reliability_transactions_status ON reliability.transactions (status);

CREATE TABLE IF NOT EXISTS reliability.clean_transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50),
    agent_id VARCHAR(50),
    region VARCHAR(100),
    transaction_date DATE,
    amount NUMERIC(15, 2),
    currency VARCHAR(10),
    status VARCHAR(20),
    payment_method VARCHAR(50),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    batch_id VARCHAR(100)
);

CREATE INDEX IF NOT EXISTS idx_reliability_clean_tx_date ON reliability.clean_transactions (transaction_date);
CREATE INDEX IF NOT EXISTS idx_reliability_clean_tx_status ON reliability.clean_transactions (status);

CREATE TABLE IF NOT EXISTS reliability.quarantine (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50),
    customer_id VARCHAR(50),
    agent_id VARCHAR(50),
    region VARCHAR(100),
    transaction_date DATE,
    amount NUMERIC(15, 2),
    currency VARCHAR(10),
    status VARCHAR(20),
    payment_method VARCHAR(50),
    failure_reason VARCHAR(50) NOT NULL,
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    batch_id VARCHAR(100),
    source_file VARCHAR(255)
);

CREATE INDEX IF NOT EXISTS idx_reliability_quarantine_reason ON reliability.quarantine (failure_reason);
CREATE INDEX IF NOT EXISTS idx_reliability_quarantine_date ON reliability.quarantine (load_timestamp);

CREATE TABLE IF NOT EXISTS reliability.data_quality_runs (
    id SERIAL PRIMARY KEY,
    run_id VARCHAR(100) UNIQUE NOT NULL,
    pipeline_env VARCHAR(50),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    processed_records INTEGER,
    passed_records INTEGER,
    failed_records INTEGER,
    failure_breakdown JSONB
);
