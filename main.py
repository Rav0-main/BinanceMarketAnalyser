from random import randint
from random import random
from average import getAverageLineCoefficient
import matplotlib.pyplot as plt

def createMarketGraphicWithFixedStep(minY: int, maxY: int, stepX: int) -> list[tuple[int, float]]:
    length: int = randint(100, 150)
    pastX: int = -stepX
    result: list[tuple[int, float]] = []
    
    x: int = 0
    y: float = 0.0

    for i in range(0, length):
        x = pastX + stepX
        y = randfloat(minY, maxY)

        result.append((x, y))

        pastX = x

    return result

def randfloat(minIntPart: int, maxIntPart: int) -> float:
    return round(float(randint(minIntPart, maxIntPart)) + random(), randint(0, 6))

stepX: int = 1
marketGraphic = createMarketGraphicWithFixedStep(170, 172, stepX)
avgK = getAverageLineCoefficient(marketGraphic)

marketX = list(map(lambda item: item[0], marketGraphic))
marketY = list(map(lambda item: item[1], marketGraphic))

xLeft = marketX[-1]
xRight = marketX[-1] + stepX

avgB = marketY[-1] - avgK * xLeft

yLeft = marketY[-1]
#yRight is next excepted Y value
yRight = avgK * xRight + avgB

#draw market
plt.plot(
    marketX, marketY,
    'b-',
    linewidth=3
)  

plt.scatter(
    marketX, marketY, 
    color='red', 
    edgecolor='black', 
    s=35,           
    linewidths=1.2,  
    zorder=3,
)

#draw avgline
colorType = "r-" if avgK < 0 else "g-"
plt.plot(
    [xLeft, xRight], [yLeft, yRight],
    colorType,
    linewidth=3
) 

plt.scatter(
    [xLeft, xRight], [yLeft, yRight], 
    color='black', 
    edgecolor='black', 
    s=15,           
    linewidths=1.5,  
    zorder=3,
)

plt.show()