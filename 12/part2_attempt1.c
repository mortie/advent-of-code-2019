#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct moon {
	int x, y, z;
	int vx, vy, vz;
};

void moon_gravity(struct moon *moon, struct moon *others, int others_len) {
	for (int  i = 0; i < others_len; ++i) {
		if (others + i == moon) continue;

		int xx = others[i].x - moon->x;
		moon->vx += (xx > 0) - (xx < 0);

		int yy = others[i].y - moon->y;
		moon->vy += (yy > 0) - (yy < 0);

		int zz = others[i].z - moon->z;
		moon->vz += (zz > 0) - (zz < 0);
	}
}

void moon_pair_gravity(struct moon *m1, struct moon *m2) {
	int xx = m2->x - m1->x;
	int xs = (xx > 0) - (xx < 0);
	m1->vx += xs;
	m2->vx -= xs;

	int yy = m2->y - m1->y;
	int ys = (yy > 0) - (yy < 0);
	m1->vy += ys;
	m2->vy -= ys;

	int zz = m2->z - m1->z;
	int zs = (zz > 0) - (zz < 0);
	m1->vz += zs;
	m2->vz -= zs;
}

void moon_update(struct moon *moon) {
	moon->x += moon->vx;
	moon->y += moon->vy;
	moon->z += moon->vz;
}

int moon_energy(struct moon *moon) {
	return
		(abs(moon->x) + abs(moon->y) + abs(moon->z)) *
		(abs(moon->vx) + abs(moon->vy) + abs(moon->vz));
}

void print_moons(struct moon *moons, int len) {
	for (int i = 0; i < len; ++i) {
		if (i != 0) printf(" ");
		printf("%i:((%i, %i, %i), (%i, %i, %i))", i,
			moons[i].x, moons[i].y, moons[i].z,
			moons[i].vx, moons[i].vy, moons[i].vz);
	}

	printf("\n");
}

/*
2772 iterations
Total energy: 0

real	0m0.001s
user	0m0.001s
sys	0m0.000s
*/
struct moon example1[] = {
	{ -1, 0, 2, 0, 0, 0 },
	{ 2, -10, -7, 0, 0, 0 },
	{ 4, -8, 8, 0, 0, 0 },
	{ 3, 5, -1, 0, 0, 0 },
};

/*
4686774924 iterations
Total energy: 0

real	1m43.184s
user	1m43.178s
sys	0m0.004s
*/
struct moon example2[] = {
	{ -8, -10, 0, 0, 0, 0 },
	{ 5, 5, 10, 0, 0, 0 },
	{ 2, -7, 3, 0, 0, 0 },
	{ 9, -8, -3, 0, 0, 0 },
};

struct moon actual[] = {
	{ 15, -2, -6, 0, 0, 0 },
	{ -5, -4, -11, 0, 0, 0 },
	{ 0, -6, 0, 0, 0, 0 },
	{ 5, 9, 6, 0, 0, 0 },
};

#define moonarray actual

int main() {
	int len = sizeof(moonarray) / sizeof(*moonarray);
	print_moons(moonarray, len);

	struct moon original[sizeof(moonarray) / sizeof(*moonarray)];
	memcpy(original, moonarray, sizeof(moonarray));

	struct moon *moonpairs[][2] = {
		{ &moonarray[0], &moonarray[1] },
		{ &moonarray[0], &moonarray[2] },
		{ &moonarray[0], &moonarray[3] },
		{ &moonarray[1], &moonarray[2] },
		{ &moonarray[1], &moonarray[3] },
		{ &moonarray[2], &moonarray[3] },
	};
	int pairlen = sizeof(moonpairs) / sizeof(*moonpairs);

	size_t idx = 0;
	int count = 0;
	do {
		for (int j = 0; j < pairlen; ++j)
			moon_pair_gravity(moonpairs[j][0], moonpairs[j][1]);

		for (int j = 0; j < len; ++j)
			moon_update(&moonarray[j]);

		count += 1;
		if (count >= 10000000) {
			idx += 10000000;
			count = 0;
			printf("After %zu: ", idx);
			print_moons(moonarray, len);
		}
	} while (memcmp(moonarray, original, sizeof(moonarray)) != 0);
	idx += count;
	printf("%zi iterations\n", idx);

	int energy = 0;
	for (int i = 0; i < len; ++i)
		energy += moon_energy(&moonarray[i]);
	printf("Total energy: %i\n", energy);
}
