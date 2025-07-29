-- SQL Source All Lines
-- Made.by SMS 20250728

-- Instructor 테이블
CREATE TABLE public.instructor (
    instructor_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(20)
);

-- Admin 테이블
CREATE TABLE public.admin (
    admin_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(20)
);

-- Course 테이블
CREATE TABLE public.course (
    course_id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    course_time VARCHAR(100),
    instructor_id INTEGER REFERENCES public.instructor(instructor_id),
    admin_id INTEGER REFERENCES public.admin(admin_id)
);

-- 캠퍼스별 스키마 생성
CREATE SCHEMA seoul;
CREATE SCHEMA jeju;