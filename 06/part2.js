let fs = require("fs");

class Node {
	constructor(name) {
		this.name = name;
		this.orbits = [];
		this.orbitedBy = [];
	}

	countOrbits() {
		return this.orbits.reduce((acc, o) => acc + o.countOrbits() + 1, 0);
	}

	tree(depth = 0) {
		let space = new Array(depth + 1).join("  ");
		console.log(space+this.name+")");
		for (let o of this.orbitedBy) {
			o.tree(depth + 1);
		}
	}

	pathsTo(name, visited = []) {
		if (visited.indexOf(this) != -1)
			return [];

		visited.push(this);

		if (this.name == name)
			return [[ this ]];

		let paths = [];
		let neighbours = this.orbits.concat(this.orbitedBy);
		for (let o of neighbours) {
			let subpaths = o.pathsTo(name, visited.slice());

			for (let sub of subpaths) {
				sub.push(this);
				paths.push(sub);
			}
		}

		return paths;
	}
}

let nodes = {};
for (let line of fs.readFileSync("input", "utf-8").split("\n")) {
	let [orbitedName, orbiterName] = line.split(")");
	let orbited = nodes[orbitedName] = nodes[orbitedName] ? nodes[orbitedName] : new Node(orbitedName);
	let orbiter = nodes[orbiterName] = nodes[orbiterName] ? nodes[orbiterName] : new Node(orbiterName);
	orbiter.orbits.push(orbited);
	orbited.orbitedBy.push(orbiter);
}

let paths = nodes["YOU"].pathsTo("SAN");
console.log(paths.map(arr => arr.reverse().map(o => o.name).join(" => ")));
let shortest = paths.reduce((acc, arr) => arr.length < acc.length ? arr : acc, paths[0])
console.log("Shortest arr is", shortest.length, "long, meaning", shortest.length - 3, " orbital transfers.");
