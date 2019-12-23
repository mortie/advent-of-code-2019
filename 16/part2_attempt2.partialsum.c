#include <stdlib.h>
#include <string.h>
#include <stdio.h>

typedef unsigned char number;

void fft_once(number *nums, number *out, int length) {
	int sum = 0;
	for (int i = length - 1; i >= 0; --i) {
		sum += nums[i];
		out[i] = sum % 10;
	}
}

void fft(number *nums, number *out, int length, int count) {
	for (int i = 0; i < count; ++i) {
		fft_once(nums, out, length);
		number *tmp = nums;
		nums = out;
		out = tmp;
	}

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
