-- ------------------------------
-- USERS
-- ------------------------------
INSERT INTO users (email, password_hash, role) VALUES
('admin@ssems.net', 'hash_admin', 'admin'),
('analyst@ssems.net', 'hash_analyst', 'analyst'),
('auditor@ssems.net', 'hash_auditor', 'auditor'),
('developer@ssems.net', 'hash_dev', 'developer'),
('tester@ssems.net', 'hash_tester', 'tester'),
('security@ssems.net', 'hash_security', 'security'),
('intern@ssems.net', 'hash_intern', 'intern'),
('lead@ssems.net', 'hash_lead', 'lead'),
('manager@ssems.net', 'hash_manager', 'manager'),
('qa@ssems.net', 'hash_qa', 'qa');

-- ------------------------------
-- CLEAN LOGS (700)
-- ------------------------------
DO $$
DECLARE 
    i INT := 1;
BEGIN
    WHILE i <= 700 LOOP
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
        op := (ARRAY['DROP','DELETE','GRANT','ALTER','UPDATE'])[1 + floor(random()*5)];
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
