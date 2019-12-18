import re
import os
import math

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
    count = component.qty // recipe.output.qty
    if not component.qty % recipe.output.qty == 0: count += 1

    # Update our inputs accordingly
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

maxore = 1000000000000
min = 0
max = 1

# Find the max
while True:
    inv = {}
    min = max
    max *= 2
    reqs = manufacture(Component("FUEL", max), inv, recipes)
    if reqs["ORE"].qty > maxore:
        break
print(f"Found a min/max: {min}/{max}")

# Now that we have a min/max, we can binary search
curr = (max + min) // 2
while True:
    reqs = manufacture(Component("FUEL", curr), inv, recipes)
    if reqs["ORE"].qty > maxore:
        max = curr
    else:
        min = curr
        if max == min + 1:
            break
    curr = (max + min) // 2

# Now, 'min' is the smallest value which requires <=maxore
inv = {}
reqs = manufacture(Component("FUEL", min), inv, recipes)
print("Need", reqs, "to create", min, "fuel.")
