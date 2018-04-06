import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def graphResults(xLab, y1Lab, y2Lab, frame, save=False):
    fig, ax1 = plt.subplots()
    ax1.plot(frame[xLab], frame[y1Lab], 'b-')
    ax1.set_xlabel(xLab)
    ax1.set_ylabel(y1Lab, color='b')
    ax1.tick_params('y', colors='b')
    ax2 = ax1.twinx()
    ax2.plot(frame[xLab], frame[y2Lab], 'g-')
    ax2.set_ylabel(y2Lab, color='g')
    ax2.tick_params('y', colors='g')
    fig.tight_layout()
    if save == True:
        plt.savefig(str(xLab)+ str(y1Lab) + "Graph.png")
    plt.show()

clickDf = pd.read_csv("validation_predictions.csv")
payDf = pd.read_csv("Paypredictions.csv")
validation = pd.read_csv("validation.csv")

clickList = clickDf['predictions'].tolist()
payList = payDf['Payprediction'].tolist()

payClickRatio = []
for index in range(0, len(clickList)):
    ratio = clickList[index]/payList[index]
    payClickRatio.append(ratio)

validation['payclick'] = payClickRatio

clickList = validation['click'].tolist()
payList = validation['payprice'].tolist()
ratioList = validation['payclick'].tolist()

# Put click and payprice into a list for ease of use later
clickCostList = []
for index in range(0, len(clickList)):
    click = clickList[index]
    pay = payList[index]
    ratio = ratioList[index]
    tempTuple = (click, pay, ratio)
    clickCostList.append(tempTuple)

# pCTR-payprice ratio
ratioList = [] # NB: was 0.0005 below
for cutOff in np.arange(0.001, 0.02, 0.0001):
    print(cutOff)
    impressions = 0
    clicks = 0
    totalPrice = 0
    bidPrice = 300
    for clickPayRatio in clickCostList:
        if clickPayRatio[2] >= cutOff:
            if bidPrice > clickPayRatio[1]:
                # Check if we have reached the budget, if so break the loop
                if totalPrice+(clickPayRatio[1]/1000) <= 6250:
                    impressions = impressions + 1
                    totalPrice = totalPrice + (clickPayRatio[1]/1000)
                    clicks = clicks + clickPayRatio[0]
                else:
                    continue
    if clicks == 0:
        CTR = 0
        CPC = 0
    else:
        CTR = clicks/impressions*100
        CPC = totalPrice/clicks

    if impressions == 0:
        CPM = 0
    else:
        CPM = totalPrice/impressions*1000

    ratioList.append([str(cutOff), impressions, clicks, CTR, totalPrice, CPM, CPC])

constantDataB = pd.DataFrame(ratioList, columns=['ratio', 'impressions', 'clicks', 'CTR', 'totalPrice', 'CPM', 'CPC'],
                             dtype='float')

graphResults('ratio', 'clicks', 'CTR', constantDataB)
graphResults('ratio', 'clicks', 'totalPrice', constantDataB)


constantDataB.sort_values('clicks', ascending=False, inplace=True)
print("Top 5 by clicks:")
print(constantDataB.head(n=5))