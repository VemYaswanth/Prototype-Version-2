CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(50) CHECK (role IN ('admin','auditor','viewer')),
    mfa_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS query_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    query_text TEXT NOT NULL,
    operation_type VARCHAR(10) CHECK (operation_type IN ('SELECT','INSERT','UPDATE','DELETE')),
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    client_ip VARCHAR(45),
    session_id UUID,
    blockchain_hash TEXT
);

CREATE TABLE IF NOT EXISTS anomalies (
    anomaly_id SERIAL PRIMARY KEY,
    log_id INTEGER REFERENCES query_logs(log_id),
    anomaly_score FLOAT NOT NULL,
    is_anomalous BOOLEAN NOT NULL,
    model_version VARCHAR(50),
    flagged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alerts (
    alert_id SERIAL PRIMARY KEY,
    anomaly_id INTEGER REFERENCES anomalies(anomaly_id),
    alert_type VARCHAR(100),
    confidence FLOAT,
    status VARCHAR(20) DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS blockchain_logs (
    blockchain_id SERIAL PRIMARY KEY,
    log_id INTEGER REFERENCES query_logs(log_id),
    block_hash TEXT NOT NULL,
    block_index INTEGER,
    transaction_id TEXT,
    committed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_config (
    config_id SERIAL PRIMARY KEY,
    param_name VARCHAR(100),
    param_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);