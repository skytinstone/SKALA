// Main.java
import java.util.*;

//////////////////////////////////////////
// 1) 추상화 (Abstraction)
//////////////////////////////////////////
// 핵심만 드러내는 '형태' 정의: 면적 계산과 그리기
interface Drawable {                // 인터페이스: 행위의 약속
    void draw();
}

abstract class Shape implements Drawable {    // 추상 클래스: 공통 속성/로직 + 추상 메서드
    // 2) 캡슐화 (Encapsulation)
    // 필드를 private으로 숨기고, 유효성 검증을 setter에서 수행
    private String name;

    protected Shape(String name) {            // 공통 생성자
        this.name = name;
    }

    public String getName() {                 // getter
        return name;
    }

    public void setName(String name) {        // setter (간단한 검증)
        if (name == null || name.isBlank()) throw new IllegalArgumentException("name required");
        this.name = name;
    }

    public abstract double area();            // 하위 클래스가 반드시 구현해야 하는 핵심 기능
}

//////////////////////////////////////////
// 4) 상속성 (Inheritance) + 3) 다형성 (Polymorphism-Overriding)
//////////////////////////////////////////
class Circle extends Shape {
    private double r;

    // 오버로딩(같은 이름 다른 매개변수) 예시 포함
    public Circle(double r) { super("Circle"); setRadius(r); }
    public Circle()         { this(1.0); } // 3) 다형성(Overloading) — 생성자 다형성

    public final void setRadius(double r) { // final: 하위에서 변경 불가(불변 규칙 보호)
        if (r <= 0) throw new IllegalArgumentException("radius > 0");
        this.r = r;
    }
    public double getRadius() { return r; }

    @Override
    public double area() {                   // 3) 다형성(Overriding)
        return Math.PI * r * r;
    }

    @Override
    public void draw() {                     // 인터페이스 구현
        System.out.println("○ Drawing " + getName() + " r=" + r);
    }
}

class Rectangle extends Shape {
    private double w, h;

    public Rectangle(double w, double h) {
        super("Rectangle");
        setSize(w, h);
    }

    // 오버로딩 메서드: 같은 이름, 다른 파라미터
    public void setSize(double side) { setSize(side, side); }
    public void setSize(double w, double h) {
        if (w <= 0 || h <= 0) throw new IllegalArgumentException("w,h > 0");
        this.w = w; this.h = h;
    }

    public double getW() { return w; }
    public double getH() { return h; }

    @Override
    public double area() {                    // 3) 다형성(Overriding)
        return w * h;
    }

    @Override
    public void draw() {
        System.out.println("▭ Drawing " + getName() + " " + w + "x" + h);
    }
}

// 상속 확장 예시: Rectangle의 규칙을 그대로 쓰고 의미만 특화
class Square extends Rectangle {
    public Square(double side) {
        super(side, side);                    // 4) 상속성: 부모 생성자 활용
        setName("Square");                    // 보호된 로직/공통 속성 재사용
    }
}

//////////////////////////////////////////
// 유틸: 오버로딩 vs 오버라이딩 비교용
//////////////////////////////////////////
class AreaPrinter {
    // 오버로딩: 파라미터 타입/개수가 다른 같은 이름의 메서드
    public static void print(Shape s) {
        System.out.printf("%-8s area = %.2f%n", s.getName(), s.area());
    }
    public static void print(List<? extends Shape> shapes) {
        for (Shape s : shapes) print(s);
    }
}

//////////////////////////////////////////
// 실행부
//////////////////////////////////////////
public class Main {
    public static void main(String[] args) {
        // 3) 다형성: 상위 타입(Shape) 참조로 다양한 하위 타입을 처리 (런타임 바인딩)
        List<Shape> shapes = List.of(
                new Circle(2.0),
                new Rectangle(3.0, 4.0),
                new Square(5.0),
                new Circle()                 // 오버로딩된 기본 생성자
        );

        // 공통 인터페이스 기반 행위 호출 (draw)
        for (Drawable d : shapes) d.draw();

        // 공통 추상 타입 기반 기능 호출 (area)
        AreaPrinter.print(shapes);

        // 캡슐화 검증 시연
        Circle c = new Circle(1.5);
        // c.r = -1; // 컴파일 오류: private (정보 은닉)
        // c.setRadius(-1); // 런타임 검증으로 예외 발생
    }
}
