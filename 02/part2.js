let fs = require("fs");

let inputStr = fs.readFileSync("input", "utf-8");
let input = inputStr.split(",").map(x => parseInt(x));

function eval(memory) {
	let iptr = 0;
	function read() {
		return memory[iptr++];
	}

	let oprs = {
		1: function() {
			let aIdx = read();
			let bIdx = read();
			let destIdx = read();
			memory[destIdx] = memory[aIdx] + memory[bIdx];
			return true;
		},
		2: function() {
			let aIdx = read();
			let bIdx = read();
			let destIdx = read();
			memory[destIdx] = memory[aIdx] * memory[bIdx];
			return true;
		},
		99: function() {
			return false;
		},
	};

	function evalNext() {
		let opcode = read();
		if (!oprs[opcode])
			throw new Error("Unknown op code: " + opcode);
		return oprs[opcode]();
	}

	while (evalNext());
}

for (let noun = 0; noun < 100; ++noun) {
	for (let verb = 0; verb < 100; ++verb) {
		input[1] = noun;
		input[2] = verb;
		let memory = input.slice();
		eval(memory);
		if (memory[0] == 19690720) {
			console.log("Found 19690720:", noun, verb, 100 * noun + verb);
		}
	}
}
