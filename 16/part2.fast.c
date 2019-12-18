#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <omp.h>

int pat[] = { 0, 1, 0, -1 };
int pattern(int n, int k) {
	return pat[(n / k) % 4];
}

void phase(int *input, int *output, int begin, int length, int totallength, int printer) {
	for (int i = begin; i < begin + length; ++i) {
		int sum = 0;

		for (int j = 0; j < totallength; ++j) {
			int p = pattern(j + 1, i + 1);
			sum += input[j] * p;
		}

		output[i] = abs(sum) % 10;

		if (printer && i % 1 == 0) {
			double frac = ((double)i - (double)begin) / (double)length;
			printf("  %f%%\r", frac * 100.0);
		}
	}

	if (printer)
		printf("\n");
}

void fft_parallel(int *input, int *output, int length, int count, int nthreads) {
	for (int i = 0; i < count; ++i) {
		printf("%i/%i...\n", i + 1, count);
		#pragma omp parallel for
		for (int th = 0; th < nthreads; ++th) {
			int begin = th * (length / nthreads);
			int len = i == (nthreads - 1) ? length - begin : (length / nthreads);
			phase(input, output, begin, len, length, th == (nthreads - 1));
		}
		int *t = input;
		input = output;
		output = t;
	}

	if (count % 2 == 0)
		memcpy(output, input, length * sizeof(*output));
}

void fft_sequential(int *input, int *output, int length, int count) {
	for (int i = 0; i < count; ++i) {
		printf("%i/%i...\n", i + 1, count);
		phase(input, output, 0, length, length, 1);
		int *t = input;
		input = output;
		output = t;
	}

	if (count % 2 == 0)
		memcpy(output, input, length * sizeof(*output));

}

int main() {
	char buf[4096];
	FILE *f = fopen("input", "r");
	fgets(buf, sizeof(buf), f);
	int length = strlen(buf) - 1;
	int msglength = length * 10000;
	printf("Length: %i (%i)\n", length, msglength);

	int *input = malloc(msglength * sizeof(*input));
	for (int i = 0; i < msglength; ++i) {
		char in = buf[i % length];
		input[i] = in - '0';
	}

	int *output = malloc(msglength * sizeof(*input));

	fft_parallel(input, output, msglength, 100, 8);
	for (int i = 0; i < 8; ++i)
		printf("%i ", output[i]);
	printf("\n");
}
