#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

// We need timer logic to know we shrekked bendik
#include <time.h>

typedef uint64_t idkint;
#define IDKVAL ((idkint)(11260 * 2 + 100))

double now() {
	struct timespec tv;
	clock_gettime(CLOCK_MONOTONIC, &tv);
	return (double)tv.tv_sec + (double)tv.tv_nsec * (1.0 / 1000000000.0);
}

struct point {
	int x;
	int y;
};

idkint point2idk(struct point p) {
	return (p.x + IDKVAL / 2) * IDKVAL + (p.y + IDKVAL / 2);
}
struct point idk2point(idkint idk) {
	struct point p = { (int)(idk / IDKVAL) - IDKVAL / 2, (int)(idk % IDKVAL) - IDKVAL / 2 };
	return p;
}

void goThrough(uint8_t *points, char *inp, uint8_t id) {
	struct point pos = { 0, 0 };

	for (char *c = inp; *c != '\n';) {
		char dir = *c;
		char *numStr = c + 1;
		long count = strtol(numStr, &c, 10);
		if (*c != '\n') c += 1;

		for (long i = 0; i < count; ++i) {
			if (dir == 'U') pos.y -= 1;
			else if (dir == 'R') pos.x += 1;
			else if (dir == 'L') pos.x -= 1;
			else pos.y += 1;

			points[point2idk(pos)] |= id;
		}
	}
}

int main() {
	FILE *f = fopen("input", "r");
	fseek(f, 0, SEEK_END);
	long flen = ftell(f);
	rewind(f);

	char *input = malloc(flen);
	if (fread(input, 1, flen, f) != flen) abort();
	fclose(f);

	char *line1 = input;
	char *line2 = strchr(line1, '\n') + 1;

	double startTime = now();
	size_t pointslen = IDKVAL * IDKVAL + IDKVAL;
	uint8_t *points = calloc(1, pointslen);

	goThrough(points, line1, 0b01);
	goThrough(points, line2, 0b10);

	idkint idx = 0;
	struct point shortest = { IDKVAL, IDKVAL };
	int shortestdist = INT_MAX;
	while (1) {
		uint8_t *chr = memchr(points + idx, 0b11, pointslen - idx);
		if (chr == NULL) break;
		idx = chr - points;

		struct point p = idk2point(idx);
		int dist = abs(p.x) + abs(p.y);
		if (dist < shortestdist) {
			shortest = p;
			shortestdist = dist;
		}

		idx += 1;
	}

	double endTime = now();
	printf("Shortest: (%i, %i) - Distance %i\n", shortest.x, shortest.y, abs(shortest.x) + abs(shortest.y));
	printf("Found solution in %f seconds.\n", endTime - startTime);
	free(input);
	free(points);
}
