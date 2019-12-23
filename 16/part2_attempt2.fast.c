#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <omp.h>

typedef unsigned char number;

void fft_once_part(number *nums, number *out, int length, int thstart, int thlength) {
	for (int i = thstart; i < thstart + thlength; ++i) {
		int sum = 0;
		#pragma clang loop vectorize(enable) interleave(enable)
		for (int j = i; j < length; ++j) {
			sum += nums[j];
		}

		out[i] = sum % 10;
	}
}

void fft_once(number *nums, number *out, int length, int nthreads) {
	int incrs = length / nthreads;
	#pragma omp parallel for
	for (int th = 0; th < nthreads; ++th) {
		int thstart = incrs * th;
		int thlength = th == nthreads - 1 ? length - thstart : incrs;
		fft_once_part(nums, out, length, thstart, thlength);
	}
}

void fft(number *nums, number *out, int length, int count) {
	for (int i = 0; i < count; ++i) {
		fft_once(nums, out, length, 16);
		number *tmp = nums;
		nums = out;
		out = tmp;

		printf("\r%i/%i...", i + 1, count);
		fflush(stdout);
	}
	printf("\n");

	if (count % 2 == 0)
		memcpy(out, nums, length);
}

int main() {
	FILE *f = fopen("input", "r");
	if (f == NULL) {
		perror("input");
		return EXIT_FAILURE;
	}

	char inbuf[4096];
	if (fgets(inbuf, sizeof(inbuf), f) == NULL) {
		perror("input"); // Yes, this could print "input: Success" on failure. IDC.
		return EXIT_FAILURE;
	}
	int insize = strlen(inbuf) - 1;
	inbuf[insize] = '\0';

	char startidxstr[8];
	memcpy(startidxstr, inbuf, 7);
	startidxstr[7] = '\0';
	int startidx = atoi(startidxstr);

	int msgsize = (insize * 10000) - startidx;
	number *msgbuf = malloc(msgsize * sizeof(*msgbuf));
	for (int i = 0; i < msgsize; ++i)
		msgbuf[i] = (number)(inbuf[(i + startidx) % insize] - '0');

	printf("Message buffer is %i bytes (would be %i without skipping %i chars). First 8 chars: ", msgsize, insize * 10000, startidx);
	for (int i = 0; i < 8; ++i)
		printf("%u", msgbuf[i]);
	printf("\n");

	number *outbuf = malloc(msgsize * sizeof(*outbuf));
	fft(msgbuf, outbuf, msgsize, 100);
	printf("First 8 chars of outbuf: ");
	for (int i = 0; i < 8; ++i)
		printf("%u", outbuf[i]);
	printf("\n");

	free(outbuf);
	free(msgbuf);
}
