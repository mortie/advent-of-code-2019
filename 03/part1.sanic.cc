#include <vector>
#include <optional>
#include <algorithm>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include <limits.h>
#include <chrono>

struct Point {
	int x;
	int y;

	Point operator+(Point p) { return Point{ x + p.x, y + p.y }; }
	Point operator-(Point p) { return Point{ x - p.x, y - p.y }; }
	void operator+=(Point p) { x += p.x; y += p.y; }
	void operator-=(Point p) { x -= p.x; y -= p.y; }
	bool operator==(Point p) { return x == p.x && y == p.y; }
	bool operator!=(Point p) { return !(*this == p); }

	int manhattanDist() {
		return abs(x) + abs(y);
	}

	std::string toString() {
		return "(" + std::to_string(x) + ", " + std::to_string(y) + ")";
	}
};

struct Line {
	enum class Direction { HOR, VERT };

	Direction dir;
	Point start;
	int len;

	Line(Point s, Point e) {
		if (s.y == e.y) {
			dir = Direction::HOR;
			start.y = s.y;
			start.x = std::min(s.x, e.x);
			len = std::abs(e.x - s.x);
		} else {
			dir = Direction::VERT;
			start.x = s.x;
			start.y = std::min(s.y, e.y);
			len = std::abs(e.y - s.y);
		}
	}

	std::optional<Point> intersectsWith(Line other) {
		if (
				dir == Direction::HOR && other.dir == Direction::VERT &&
				other.start.x >= start.x && other.start.x <= start.x + len &&
				other.start.y <= start.y && other.start.y + other.len >= start.y)
			return Point{ other.start.x, start.y };
		else if (
				dir == Direction::VERT && other.dir == Direction::HOR &&
				other.start.y >= start.y && other.start.y <= start.y + len &&
				other.start.x <= start.x && other.start.x + other.len >= start.x)
			return Point{ start.x, other.start.y };
		return std::nullopt;
	}

	std::string toString() {
		if (dir == Direction::HOR)
			return start.toString() + " - " + Point{ start.x + len, start.y }.toString();
		else
			return start.toString() + " - " + Point{ start.x, start.y + len }.toString();
	}
};

struct Path {
	std::vector<Point> points{ Point{0, 0} };

	void readPath(FILE *f) {
		while (readInstr(f));
	}

	bool readInstr(FILE *f) {
		char dir;
		int num;
		if (fscanf(f, "%c%i", &dir, &num) != 2) abort();

		// Move <num> steps in <dir> from the previous point
		Point p = points.back();
		if (dir == 'U') p -= Point{ 0, num };
		else if (dir == 'D') p += Point{ 0, num };
		else if (dir == 'L') p -= Point{ num, 0 };
		else if (dir == 'R') p += Point{ num, 0 };
		else abort();
		points.push_back(p);

		// If the next character we read is a newline, we're done. If it's not,
		// it'll be a comma, so we have more input.
		return fgetc(f) != '\n';
	}

	std::vector<Line> lines() {
		std::vector<Line> vec;
		vec.reserve(points.size() - 1);

		size_t size = points.size();
		for (size_t i = 1; i < size; ++i) {
			vec.push_back(Line{ points[i - 1], points[i] });
		}

		return vec;
	}
};

int main() {
	FILE *f = fopen("input", "r");
	Path p1; p1.readPath(f);
	Path p2; p2.readPath(f);
	fclose(f);

	auto start = std::chrono::high_resolution_clock::now();

	std::optional<Point> nearest;
	for (Line p1line: p1.lines()) {
		for (Line p2line: p2.lines()) {
			auto point = p1line.intersectsWith(p2line);
			if (point && *point != Point{ 0, 0 }) {
				if (!nearest || point->manhattanDist() < nearest->manhattanDist())
					nearest = point;
			}
		}
	}

	auto end = std::chrono::high_resolution_clock::now();
	auto elapsed = std::chrono::duration<double, std::milli>(end - start);

	std::cout
		<< "Nearest: " << nearest->toString() << ", dist " << nearest->manhattanDist()
		<< " in " << elapsed.count() << "ms\n";
}
