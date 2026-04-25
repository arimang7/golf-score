import json
import os

# 1. JSON 데이터 로드
json_path = 'db-src/업종별골프장현황.json'
if not os.path.exists(json_path):
    print(f"Error: {json_path} not found.")
    exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    courses = json.load(f)

sql = []
sql.append('-- 1. Table Creation (DDL)')
sql.append('DROP TABLE IF EXISTS round_scores;')
sql.append('DROP TABLE IF EXISTS rounds;')
sql.append('DROP TABLE IF EXISTS golf_courses;')
sql.append('DROP TABLE IF EXISTS users;')

sql.append('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    google_id VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR,
    picture_url VARCHAR,
    is_approved BOOLEAN DEFAULT 0,
    is_admin BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);''')

sql.append('''
CREATE TABLE golf_courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    address VARCHAR,
    holes INTEGER DEFAULT 18,
    region VARCHAR,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);''')

sql.append('''
CREATE TABLE rounds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER REFERENCES golf_courses(id),
    date DATETIME NOT NULL,
    players TEXT NOT NULL, -- SQLite에서는 JSON 대신 TEXT(JSON format) 사용
    created_by INTEGER REFERENCES users(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);''')

sql.append('''
CREATE TABLE round_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    round_id INTEGER REFERENCES rounds(id) ON DELETE CASCADE,
    hole_number INTEGER NOT NULL,
    par INTEGER DEFAULT 4,
    score_a INTEGER,
    score_b INTEGER,
    score_c INTEGER,
    score_d INTEGER,
    voice_transcript TEXT
);''')

sql.append('\n-- 2. Initial Data (DML)')
sql.append("-- 관리자 계정 추가 (ID: admin / PW: config.py 설정값 사용)")
sql.append("INSERT INTO users (google_id, email, name, is_approved, is_admin) VALUES ('admin_manual', 'admin@internal', 'System Admin', 1, 1);")

sql.append('\n-- 골프장 데이터 추가')
for c in courses:
    name = c.get('BIZPLC_NM', '').replace("'", "''")
    addr = (c.get('REFINE_ROADNM_ADDR') or c.get('REFINE_LOTNO_ADDR') or '').replace("'", "''")
    holes = c.get('GOLFCRS_HOLE_CNT', 18)
    reg = addr[:2] if addr else '기타'
    if name:
        sql.append(f"INSERT INTO golf_courses (name, address, holes, region) VALUES ('{name}', '{addr}', {holes}, '{reg}');")

# 3. SQL 파일 저장
with open('migration.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql))

print(f"✅ migration.sql generated with {len(courses)} courses.")
