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

def drawPriceGraphics(prices: list[PriceInformation]) -> None:
    openPrices: list[float] = []
    closePrices: list[float] = []
    times: list = []

    for price in prices:
        openPrices.append(price.open)
        closePrices.append(price.close)
        times.append(price.time)

    plt.figure(figsize=(12, 6))

    plt.plot(times, openPrices, marker="o", linestyle="-", color="green", label="Open")
    plt.plot(times, closePrices, marker="o", linestyle="-", color="red", label="Close")
 
    plt.grid(True)

    plt.gcf().autofmt_xdate()

def showLegend():
    plt.legend(loc="best", fontsize=10, framealpha=1)

def show():
    plt.show()