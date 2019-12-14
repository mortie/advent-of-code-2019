import re

class Component:
    def __init__(self, name, qty):
        self.name = name
        self.qty = qty

    def __repr__(self):
        return f"{self.qty} {self.name}"

    def clone(self):
        return Component(self.name, self.qty)

class Recipe:
    def __init__(self, inputs, output):
        self.inputs = [input.clone() for input in inputs]
        self.output = output.clone()

    def __repr__(self):
        return f"{self.inputs} => {self.output}"

    def clone(self):
        return Recipe(self.inputs, self.output)

component_rx = re.compile(r"(\d+) (\w+)")
def parse_component(s):
    match = component_rx.search(s)
    groups = match.groups()
    return Component(groups[1], int(groups[0]))

recipes = {}
with open("input") as f:
    for line in f:
        inputstr, output = line.split("=>")
        inputs = inputstr.split(", ")

        outcomp = parse_component(output)
        incomps = [parse_component(input) for input in inputs]
        recipes[outcomp.name] = Recipe(incomps, outcomp)

def manufacture(component, inventory, recipes, depth = 0):
    # See if we got anything in our inventory we can use
    if component.name in inventory:
        if inventory[component.name].qty >= component.qty:
            inventory[component.name].qty -= component.qty
            return {}
        else:
            component.qty -= inventory[component.name].qty
            inventory[component.name].qty = 0

    # If there's no recipe to make what we need, there's nothing we can do
    if not component.name in recipes:
        return { component.name: component }

    # Now, we need to make the necessary components
    recipe = recipes[component.name].clone()
    neededtotal = {}

    # We may need to make multiples of the thing
    count = 1
    while recipe.output.qty * count < component.qty:
        count += 1
    for input in recipe.inputs:
        input.qty *= count
    recipe.output.qty *= count

    for recinput in recipe.inputs:
        needed = manufacture(recinput, inventory, recipes, depth + 1)

        # Merge in the needed with our total
        for key in needed:
            if key in neededtotal:
                neededtotal[key].qty += needed[key].qty
            else:
                neededtotal[key] = needed[key].clone()

    # We may have a bunch more of stuff now
    if component.name not in inventory:
        inventory[component.name] = recipe.output.clone()
        inventory[component.name].qty -= component.qty
    else:
        inventory[component.name].qty += recipe.output.qty - component.qty

    return neededtotal

inv = {}
reqs = manufacture(Component("FUEL", 1), inv, recipes)
print("Needs", reqs)
print("Left over:", list(inv.values()))
