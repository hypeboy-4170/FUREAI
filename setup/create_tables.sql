-- FUREAI 洋服一覧テーブル

CREATE TABLE IF NOT EXISTS clothes (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    s3_key VARCHAR(200) NOT NULL,
    category VARCHAR(50),
    color VARCHAR(50),
    tags VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- インデックス
CREATE INDEX idx_clothes_user ON clothes(user_id);

-- 確認
SELECT 'テーブル作成完了' AS status;
