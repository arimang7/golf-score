-- 1. Table Creation (DDL)
DROP TABLE IF EXISTS round_scores;
DROP TABLE IF EXISTS rounds;
DROP TABLE IF EXISTS golf_courses;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    google_id VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR,
    picture_url VARCHAR,
    is_approved BOOLEAN DEFAULT 0,
    is_admin BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE golf_courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    address VARCHAR,
    holes INTEGER DEFAULT 18,
    region VARCHAR,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rounds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER REFERENCES golf_courses(id),
    date DATETIME NOT NULL,
    players TEXT NOT NULL, -- SQLite에서는 JSON 대신 TEXT(JSON format) 사용
    created_by INTEGER REFERENCES users(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

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
);

-- 2. Initial Data (DML)
-- 관리자 계정 추가 (시스템용 & 사용자용)
INSERT INTO users (google_id, email, name, is_approved, is_admin) VALUES ('admin_manual', 'admin@internal', 'System Admin', 1, 1);
INSERT INTO users (google_id, email, name, is_approved, is_admin) VALUES ('alex.maeng', 'alex.maeng@gmail.com', 'Alex Maeng', 1, 1);

-- 골프장 데이터 추가
INSERT INTO golf_courses (name, address, holes, region) VALUES ('빅토리아', '경기도 여주시 가남읍 송삼로 191', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('아리지', '경기도 여주시 가남읍 아리지그린길 68', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('금강', '경기도 여주시 가남읍 여주남로 541', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('금강', '경기도 여주시 가남읍 여주남로 541', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('자유', '경기도 여주시 가남읍 자유그린길 69', 36, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('남여주', '경기도 여주시 가여로 532', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('베뉴지', '경기도 가평군 가평읍 용추로171번길 100', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('크리스탈밸리', '경기도 가평군 상면 대보간선로 602-111', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('가평베네스트', '경기도 가평군 상면 둔덕말길 232', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('마이다스밸리청평', '경기도 가평군 설악면 다락재로 73-111', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('프리스틴밸리', '경기도 가평군 설악면 유명로 1243-199', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('리앤리', '경기도 가평군 조종면 운악청계로 702-24', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('썬힐', '경기도 가평군 조종면 운악청계로 809', 36, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('아난티', '경기도 가평군 설악면 유명로 961-34', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('한양파인', '경기도 고양시 덕양구 고양대로1643번길 164', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('한양', '경기도 고양시 덕양구 고양대로1643번길 164', 36, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('뉴코리아', '경기도 고양시 덕양구 신원2로 57', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('올림픽', '경기도 고양시 덕양구 혜음로 301', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('일산스프링힐스', '경기도 고양시 일산동구 산황로 108', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('그린힐', '경기도 광주시 곤지암읍 내선길 176', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('로제비앙', '경기도 광주시 곤지암읍 오향길 180', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('강남300', '경기도 광주시 새말길 353', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('남양주', '경기도 남양주시 오남읍 진건오남로 516-31', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('한림광릉', '경기도 남양주시 진접읍 팔야로 280', 6, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('해비치', '경기도 남양주시 화도읍 재재기로190번길 160', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('남서울', '경기도 성남시 분당구 판교백현로 161', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('더헤븐', '경기도 안산시 단원구 대선로 466', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('한성', '경기도 용인시 기흥구 구교동로 151', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('골드', '경기도 용인시 기흥구 기흥단지로 398', 36, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('남부', '경기도 용인시 기흥구 사은로 163', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('수원', '경기도 용인시 기흥구 중부대로 495', 36, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('태광', '경기도 용인시 기흥구 흥덕4로 77', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('플라자', '경기도 용인시 처인구 남사읍 봉무로153번길 79', 36, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('레이크사이드', '경기도 용인시 처인구 모현읍 능원로 181', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('레이크사이드', '경기도 용인시 처인구 모현읍 능원로 181', 36, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('용인', '경기도 용인시 처인구 백암면 황새울로 255', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('은화삼', '경기도 용인시 처인구 백옥대로 860-38', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('양지파인', '경기도 용인시 처인구 양지면 남평로 112', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('블루원용인', '경기도 용인시 처인구 원삼면 보개원삼로1534번길 40', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('지산', '경기도 용인시 처인구 원삼면 죽양대로2000번길 60', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('지산퍼블릭', '경기도 용인시 처인구 원삼면 죽양대로2000번길 60', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('해솔리아', '경기도 용인시 처인구 이동읍 백자로 369', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('신원', '경기도 용인시 처인구 이동읍 이원로 225', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('화산', '경기도 용인시 처인구 이동읍 화산로 239', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('더반', '경기도 이천시 대월면 대월로 627-141', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('뉴스프링빌', '경기도 이천시 모가면 사실로527번길 158', 36, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('뉴스프링빌', '경기도 이천시 모가면 사실로527번길 158', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('비에이비스타', '경기도 이천시 모가면 어농로 272', 41, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('1.2.3', '경기도 고양시 덕양구 통일로 43-168', 6, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('고양', '경기도 고양시 덕양구 흥도로 304-23', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('이스트밸리', '경기도 광주시 곤지암읍 건업길 195', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('중부', '경기도 광주시 곤지암읍 경충대로 451', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('남촌', '경기도 광주시 곤지암읍 부항길 135-38', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('곤지암', '경기도 광주시 도척면 도척윗로 280', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('뉴서울', '경기도 광주시 삼지곡길 95', 36, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('안양', '경기도 군포시 군포로 364', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('김포SEASIDE', '경기도 김포시 월곶면 김포대로2801번길 219', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('한림광릉', '경기도 남양주시 진접읍 팔야로 280', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('비전힐스', '경기도 남양주시 화도읍 마치로 226-220', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('양주', '경기도 남양주시 화도읍 북한강로 1525-52', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('티클라우드', '경기도 동두천시 평화로 3202', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('솔트베이', '경기도 시흥시 마유로 987', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('아세코밸리', '경기도 시흥시 마전로 307', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('해슬리나인브릿지', '경기도 여주시 명품1로 76', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('신라', '경기도 여주시 북내면 신라그린길 84', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('스카이밸리', '경기도 여주시 북내면 운촌길 254', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('렉스필드', '경기도 여주시 산북면 광여로 1115', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('렉스필드', '경기도 여주시 산북면 광여로 1115', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('YJC', '경기도 여주시 월평로 78', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('소피아그린', '경기도 여주시 점동면 소피아그린길 84', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('자유로', '경기도 연천군 백학면 노아로297번길 179-55', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('여주썬밸리', '경기도 여주시 강천면 강문로 872', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('캐슬파인', '경기도 여주시 강천면 부평로 580', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('360도', '경기도 여주시 강천면 부평로 609', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('이포', '경기도 여주시 금사면 장흥로 416', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('블루헤런', '경기도 여주시 대신면 고달사로 67', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('스카이밸리', '경기도 여주시 북내면 운촌길 254', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('ROUTE52', '경기도 여주시 북내면 중암1길 36', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('세라지오', '경기도 여주시 여양로 530', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('페럼', '경기도 여주시 점동면 점동로 181', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('한림용인', '경기도 용인시 처인구 남사읍 경기동로 628', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('코리아', '경기도 용인시 기흥구 기흥단지로 224', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('국가보훈부 88', '경기도 용인시 기흥구 석성로521번길 169', 36, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('태광', '경기도 용인시 기흥구 흥덕4로 77', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('한원', '경기도 용인시 처인구 남사읍 전나무골길2번길 94', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('써닝포인트', '경기도 용인시 처인구 백암면 고안로51번길 205', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('석천', '경기도 용인시 처인구 백암면 황새울로 255', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('아시아나', '경기도 용인시 처인구 양지면 양대로 290', 36, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('블루원용인', '경기도 용인시 처인구 원삼면 보개원삼로1534번길 40', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('코리아', '경기도 용인시 처인구 이동읍 기흥단지로 579', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('세현', '경기도 용인시 처인구 이동읍 백자로 450', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('글렌로스', '경기도 용인시 처인구 포곡읍 에버랜드로562번길 69', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('사우스스프링스', '경기도 이천시 모가면 공원로 64', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('웰링턴', '경기도 이천시 모가면 사실로725번길 119-73', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('비에이비스타', '경기도 이천시 모가면 어농로 272', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('이천실크밸리', '경기도 이천시 율면 임오산로 296', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('에이치원', '경기도 이천시 호법면 장자터로 115', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('더크로스비', '경기도 이천시 호법면 중부대로798번길 177', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('서원밸리', '경기도 파주시 광탄면 서원길 333', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('서원힐스', '경기도 파주시 광탄면 서원길 333', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('노스팜', '경기도 파주시 광탄면 쇠장이길 265', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('서서울', '경기도 파주시 광탄면 혜음로 324', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('타이거', '경기도 파주시 법원읍 술이홀로 1803', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('푸른솔', '경기도 포천시 가산면 금우로 276', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('샴발라', '경기도 포천시 군내면 청군로 2856-93', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('포천아도니스', '경기도 포천시 신북면 포천로 2499', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('몽베르', '경기도 포천시 영북면 산정호수로 359-12', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('힐마루', '경기도 포천시 영중면 금화봉4길 77-1', 45, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('일동레이크대중제', '경기도 포천시 일동면 화동로 738', 12, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('포천힐스', '경기도 포천시 군내면 반월산성로375번길 34', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('기흥', '경기도 화성시 풀무골로106번길 244', 36, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('링크나인', '경기도 화성시 마도면 해운로630번길 49', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('발리오스', '경기도 화성시 팔탄면 3.1만세로 641-28', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('제일', '경기도 안산시 상록구 태마당로 28', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('안성베네스트', '경기도 안성시 금광면 삼흥로 660', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('이글몬트', '경기도 안성시 보개면 보삼로 106', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('골프존카운티안성W', '경기도 안성시 양성면 교동길 19-70', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('마에스트로', '경기도 안성시 양성면 안성맞춤대로 2134-36', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('한림안성', '경기도 안성시 양성면 양성로 349-61', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('골프클럽Q', '경기도 안성시 죽산면 장계길 20-229', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('레이크우드', '경기도 양주시 만송로 244', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('양평TPC', '경기도 양평군 지평면 대평평장길 113-8', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('마이다스레이크 이천', '경기도 이천시 설성면 설가로 602', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('블랙스톤', '경기도 이천시 장호원읍 장여로 459-160', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('블랙스톤', '경기도 이천시 장호원읍 장여로 459-160', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('베스트밸리', '경기도 파주시 광탄면 장지산로200번길 32-41', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('스마트KU골프파빌리온', '경기도 파주시 법원읍 보광로 1616', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('파주', '경기도 파주시 법원읍 화합로 306', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('J-Public', '경기도 파주시 조리읍 장곡로 100', 6, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('포레스트힐', '경기도 포천시 화현면 봉화로 253', 24, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('라싸', '경기도 포천시 이동면 제비울2길 161', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('참밸리', '경기도 포천시 삼육사로 1982', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('포천아도니스', '경기도 포천시 신북면 포천로 2499', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('몽베르', '경기도 포천시 영북면 산정호수로 359-12', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('필로스', '경기도 포천시 일동면 운악청계로 1507', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('일동레이크', '경기도 포천시 일동면 화동로 738', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('베어크리크', '경기도 포천시 화현면 달인동로 35', 36, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('캐슬렉스', '경기도 하남시 감이로 317', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('리베라', '경기도 화성시 중리길 183', 36, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('화성상록', '경기도 화성시 풀무골로60번길 80', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('라비돌', '경기도 화성시 정남면 세자로 286', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('발리오스', '경기도 화성시 팔탄면 3.1만세로 641-28', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('화성', '경기도 화성시 남양읍 화성로 1393-27', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('신안', '경기도 안성시 고삼면 개울말길 149', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('신안', '경기도 안성시 고삼면 개울말길 149', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('안성베네스트', '경기도 안성시 금광면 삼흥로 660', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('골프존카운티안성H', '경기도 안성시 보개면 보삼로 302', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('윈체스트', '경기도 안성시 서운면 오촌길 97-31', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('포웰CC안성', '경기도 안성시 양성면 약산길 67-6', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('파인크리크', '경기도 안성시 양성면 안성맞춤대로 2417-13', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('안성', '경기도 안성시 죽산면 걸미로 487', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('에덴블루', '경기도 안성시 죽산면 녹배길 175', 27, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('송추', '경기도 양주시 광적면 쇠장이길 435', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('레이크우드', '경기도 양주시 만송로 244', 9, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('더스타휴', '경기도 양평군 양동면 양동로 756', 18, '경기');
INSERT INTO golf_courses (name, address, holes, region) VALUES ('솔모로', '경기도 여주시 가남읍 솔모로그린길 171', 36, '경기');