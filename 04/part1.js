let start = 172930;
let end = 683082;

function isValid(pass) {
	let str = pass.toString().padStart(6, '0');

	for (let i = 1; i < str.length; ++i)
		if (parseInt(str[i - 1]) > parseInt(str[i]))
			return false;

	for (let i = 1; i < str.length; ++i)
		if (str[i - 1] == str[i])
			return true;

	return false;
}

let password = 0;
let count = 0;
for (i = start; i <= end; ++i) {
	if (isValid(i))
		count += 1;
}

console.log("Count:", count);
