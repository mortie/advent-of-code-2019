import sys

width = 25
height = 6

with open("input") as f:
    image = [int(x) for x in f.read().strip()]

layerSize = width * height
layerCount = int(len(image) / layerSize)
layers = [image[i*layerSize:(i+1)*layerSize] for i in range(layerCount)]

sys.stdout.write("\033[2J")
for layer in reversed(layers):
    rows = [layer[i*width:(i+1)*width] for i in range(int(layerSize / height))]
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            sys.stdout.write(f"\033[{y + 1};{x + 1}H")
            if ch == 0:
                sys.stdout.write(" ")
            elif ch == 1:
                sys.stdout.write("█")
print()
