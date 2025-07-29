-- 제주캠퍼스 (학생, 리뷰, 과정 설명)
-- 수강생 테이블
CREATE TABLE jeju.student (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(20)
);

-- 리뷰 테이블
CREATE TABLE jeju.review (
    review_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES jeju.student(student_id),
    course_id INTEGER REFERENCES public.course(course_id),
    review_text TEXT,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5)
);

-- 과정 설명 테이블
CREATE TABLE jeju.course_description (
    course_id INTEGER PRIMARY KEY REFERENCES public.course(course_id),
    description_text TEXT
);
