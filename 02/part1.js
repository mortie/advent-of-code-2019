let fs = require("fs");

let inputStr = fs.readFileSync("input", "utf-8");

let memory = inputStr.split(",").map(x => parseInt(x));
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

memory[1] = 12;
memory[2] = 2;
while (evalNext());
console.log("memory[0]:", memory[0]);
