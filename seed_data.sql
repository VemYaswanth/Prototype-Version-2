-- Ensure users exist (1–10)
INSERT INTO users (email, password_hash, role)
VALUES
('admin@ssems.net', 'hash', 'admin'),
('analyst@ssems.net', 'hash', 'analyst'),
('auditor@ssems.net', 'hash', 'auditor'),
('developer@ssems.net', 'hash', 'developer'),
('tester@ssems.net', 'hash', 'tester'),
('security@ssems.net', 'hash', 'security'),
('intern@ssems.net', 'hash', 'viewer'),
('lead@ssems.net', 'hash', 'viewer'),
('manager@ssems.net', 'hash', 'admin'),
('qa@ssems.net', 'hash', 'viewer')
ON CONFLICT (email) DO NOTHING;

-- ------------------------------
-- NORMAL LOGS (300)
-- ------------------------------
DO $$
DECLARE 
    i INT := 1;
BEGIN
    WHILE i <= 300 LOOP
        INSERT INTO query_logs (user_id, query_text, operation_type, client_ip)
        VALUES (
            (1 + floor(random() * 10))::INT,
            CONCAT(
                'SELECT * FROM ',
                (ARRAY['products','customers','orders','inventory','sessions'])[1 + floor(random()*5)],
                ' WHERE id = ', (1 + floor(random() * 500))::INT, ';'
            ),
            'SELECT',
            CONCAT('10.0.0.', (1 + floor(random()*200))::INT)
        );
        i := i + 1;
    END LOOP;
END $$;

-- ------------------------------
-- SUSPICIOUS LOGS (300)
-- ------------------------------
DO $$
DECLARE 
    i INT := 1;
    op TEXT;
    act TEXT;
BEGIN
    WHILE i <= 300 LOOP
        -- Force into allowed op types to satisfy constraint
        op := (ARRAY['UPDATE','DELETE'])[1 + floor(random()*2)];
        act := (ARRAY[
            'DROP TABLE users;',
            'DELETE FROM orders WHERE 1=1;',
            'GRANT ALL PRIVILEGES ON DATABASE securitydb TO public;',
            'ALTER TABLE payments DISABLE TRIGGER ALL;',
            'UPDATE users SET role=''admin'' WHERE id = 5;'
        ])[1 + floor(random()*5)];

        INSERT INTO query_logs (user_id, query_text, operation_type, client_ip)
        VALUES (
            (1 + floor(random() * 10))::INT,
            act,
            op,
            CONCAT('192.168.1.', (10 + floor(random()*50))::INT)
        );
        i := i + 1;
    END LOOP;
END $$;
