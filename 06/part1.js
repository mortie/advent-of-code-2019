let fs = require("fs");

class Node {
	constructor() {
		this.orbits = [];
	}

	countOrbits() {
		return this.orbits.reduce((acc, o) => acc + o.countOrbits() + 1, 0);
	}
}

let nodes = {};
for (let line of fs.readFileSync("input", "utf-8").split("\n")) {
	let [orbitedName, orbiterName] = line.split(")");
	let orbited = nodes[orbitedName] = nodes[orbitedName] ? nodes[orbitedName] : new Node();
	let orbiter = nodes[orbiterName] = nodes[orbiterName] ? nodes[orbiterName] : new Node();
	orbiter.orbits.push(orbited);
}

let indirectSum = 0;
for (let key in nodes) {
	indirectSum += nodes[key].countOrbits();
}
console.log(indirectSum - 1);
