-- サンプルデータ投入

INSERT INTO clothes (user_id, s3_key, category, color, tags) VALUES
('user_test_001', 'user_test_001/shirt_white.jpg', 'tops', 'white', 'formal'),
('user_test_001', 'user_test_001/shirt_blue.jpg', 'tops', 'blue', 'formal'),
('user_test_001', 'user_test_001/tshirt_black.jpg', 'tops', 'black', 'casual'),
('user_test_001', 'user_test_001/jacket_navy.jpg', 'outer', 'navy', 'formal'),
('user_test_001', 'user_test_001/pants_gray.jpg', 'bottoms', 'gray', 'formal'),
('user_test_001', 'user_test_001/jeans_blue.jpg', 'bottoms', 'blue', 'casual'),
('user_test_001', 'user_test_001/coat_black.jpg', 'outer', 'black', 'formal,winter'),
('user_test_001', 'user_test_001/shorts_beige.jpg', 'bottoms', 'beige', 'casual,summer');

-- 確認
SELECT 'サンプルデータ投入完了' AS status;
SELECT COUNT(*) AS clothes_count FROM clothes WHERE user_id = 'user_test_001';
SELECT * FROM clothes WHERE user_id = 'user_test_001';
