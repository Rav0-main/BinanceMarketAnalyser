def getAverageLineCoefficient(marketGraphic: list[tuple[int, float]]):
    answerK: float = (marketGraphic[1][1] - marketGraphic[0][1]) / (marketGraphic[1][0] - marketGraphic[0][0])
    
    pastPoint: tuple[int, float] = marketGraphic[1]
    
    for point in marketGraphic[2:]:
        k = (point[1] - pastPoint[1]) / (point[0] - pastPoint[0])
        answerK = (answerK + k) / 2
        pastPoint = point

    return answerK