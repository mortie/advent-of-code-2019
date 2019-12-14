import sys

width = 25
height = 6

with open("input") as f:
    image = [int(x) for x in f.read().strip()]

layerCount = int(len(image) / (width * height))

fewestZeroLayer = None
fewestZeroCount = 0
for i in range(layerCount):
    start = i * width * height
    layer = image[start:start+width*height]
    zeroCount = layer.count(0)
    if fewestZeroLayer is None or zeroCount < fewestZeroCount:
        fewestZeroLayer = layer
        fewestZeroCount = zeroCount

print(fewestZeroLayer, fewestZeroCount)
print(fewestZeroLayer.count(1) * fewestZeroLayer.count(2))
