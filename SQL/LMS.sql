-- 수강생 테이블
CREATE TABLE Student (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

-- 강사 테이블
CREATE TABLE Instructor (
    instructor_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

-- 운영자 테이블
CREATE TABLE Admin (
    admin_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

-- 교육 과정 테이블
CREATE TABLE Course (
    course_id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    instructor_id INTEGER REFERENCES Instructor(instructor_id),
    admin_id INTEGER REFERENCES Admin(admin_id)
);

-- 과정 설명 테이블
CREATE TABLE CourseDescription (
    course_id INTEGER PRIMARY KEY REFERENCES Course(course_id),
    description_text TEXT
);

-- 리뷰 테이블
CREATE TABLE Review (
    review_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES Student(student_id),
    course_id INTEGER REFERENCES Course(course_id),
    review_text TEXT,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5)
);
