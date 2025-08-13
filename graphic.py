"""
Graphic handler with format - axe X - dates(timestamp values in s), axe Y - price(float value)
"""

import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib.ticker import FuncFormatter
from priceparser import PriceInformation

def setTitleName(string: str):
    plt.title(string)

def setXLabel(string: str):
    plt.xlabel(string)

def setYLabel(string: str):
    plt.ylabel(string)

def setDateFormat(format: str):
    dateFormat = mdates.DateFormatter(format)
    plt.gca().xaxis.set_major_formatter(dateFormat)

def setPriceFormat():
    formatFunct = lambda x, p: f'{x:,.2f}'.replace(',', ' ')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(formatFunct))

def drawPriceGraphics(prices: list[PriceInformation], showOpenPrices=True, showClosePrices=True) -> None:
    openPrices: list[float] = []
    closePrices: list[float] = []
    times: list = []

    for price in prices:
        openPrices.append(price.open)
        closePrices.append(price.close)
        times.append(price.time)

    plt.figure(figsize=(12, 6))

    if(showOpenPrices):
        plt.plot(times, openPrices, marker="o", linestyle="-", color="green", label="Open prices")
    if(showClosePrices):
        plt.plot(times, closePrices, marker="o", linestyle="-", color="red", label="Close prices")
 
    plt.grid(True)

    plt.gcf().autofmt_xdate()

def drawLiniearGraphic(x: list, y: list[float], color: str, name: str) -> None:
    """
    x[i] - datetime\n
    y[i] - float
    """
    plt.plot(x, y, color=color, linestyle="-", marker="o", label=name)

def showLegend():
    plt.legend(loc="best", fontsize=10, framealpha=1)

def show():
    plt.show()