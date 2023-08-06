import iondrive, timeit, ufoLib2

path = "master_ufo/NotoSerif-Regular.ufo"

def dowork(font):
    for g in font:
        a = g.getBounds(font.layers.defaultLayer)

def ufotest():
    dowork(ufoLib2.Font.open(path))

def iontest():
    dowork(iondrive.load(ufoLib2.objects,path))

print("ufolib2 time: %f" % timeit.timeit(ufotest, number = 10))
print("iondrive: %f" % timeit.timeit(iontest, number = 10))
