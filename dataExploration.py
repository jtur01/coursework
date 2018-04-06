import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# load the dataframe
df = pd.read_csv("train.csv")

columnsToAgg = ['weekday', 'hour', 'region', 'city', 'adexchange', 'creative', 'keypage', 'advertiser']

# Summary statistics
print("Train set summary statistics")
print("Total Clicks: " + str(df['click'].sum()))
print("Total Impressions: " + str(len(df)))
print("CTR: " + str(df['click'].sum()/len(df)*100) + "%")

print("Total Cost: " + str(df['payprice'].sum()/1000))
print("Avg Cost per Impression: " + str(df['payprice'].sum()/1000/len(df)))
print("Avg Cost per Thousand Impressions (CPM): " + str(df['payprice'].sum()/len(df)))
print("Avg Cost per Click: " + str(df['payprice'].sum()/1000/df['click'].sum()))

# Function for getting CTR according to any feature
def ctrPerFeature(feature):
    featureClicks = df.groupby(feature)['click'].sum().reset_index()
    aggImps = df.groupby(feature)['click'].agg('count').reset_index()

    featureClicks['CTR'] = ""
    for index, row in featureClicks.iterrows():
        ctr = (row['click'] / aggImps['click'][index]) * 100
        featureClicks.loc[index, 'CTR'] = ctr

    return featureClicks

def graphFeature(feature):
    featureCtr = ctrPerFeature(feature)
    sns.barplot(x=feature, y='CTR', data=featureCtr, color="navy")
    plt.show()

# show average ctr by feature, select as needed
graphFeature('weekday')
graphFeature('hour')
graphFeature('region')
graphFeature('city')
graphFeature('adexchange')
graphFeature('creative')
graphFeature('slotheight')
graphFeature('slotwidth')
graphFeature('slotprice')
graphFeature('advertiser')
graphFeature('slotvisibility')
graphFeature('slotformat')

val = pd.read_csv("validation.csv")
# Summary statistics
print("\nValidation set summary statistics")
print("Total Clicks: " + str(val['click'].sum()))
print("Total Impressions: " + str(len(val)))
print("CTR: " + str(val['click'].sum()/len(val)*100) + "%")

print("Total Cost: " + str(val['payprice'].sum()/1000))
print("Avg Cost per Impression: " + str(val['payprice'].sum()/1000/len(val)))
print("Avg Cost per Thousand Impressions (CPM): " + str(df['payprice'].sum()/len(val)))
print("Avg Cost per Click: " + str(val['payprice'].sum()/1000/val['click'].sum()))

featureCtr = ctrPerFeature('weekday')
sns.barplot(x='weekday', y='CTR', data=featureCtr, color="navy")
# plt.savefig("weekday.png")
plt.show()

featureCtr = ctrPerFeature('region')
sns.barplot(x='region', y='CTR', data=featureCtr, color="green")
plt.xticks(rotation=90)
# plt.savefig("region.png")
plt.show()

featureCtr = ctrPerFeature('hour')
sns.barplot(x='hour', y='CTR', data=featureCtr, color="orange")
# plt.savefig("hour.png")
plt.show()

# Advertiser data
def ctrPerFeature(feature):
    featureClicks = df.groupby(feature)['cost'].sum().reset_index()
    aggImps = df.groupby(feature)['click'].agg('count').reset_index()
    cost = df.groupby(feature)['payprice'].agg('sum').reset_index
    avgBid = df.groupby(feature)['bidprice'].agg('mean').reset_index()
    avgPay = df.groupby(feature)['payprice'].agg('mean').reset_index()

    featureClicks['CTR'] = ""
    for index, row in featureClicks.iterrows():
        ctr = (row['click'] / aggImps['click'][index]) * 100
        featureClicks.loc[index, 'CTR'] = ctr

    print(cost)
    print(featureClicks)
    print(aggImps)
    print(avgBid)
    print(avgPay)

ctrPerFeature('advertiser')


# Click vs pay-price
sns.stripplot(df['click'], df['payprice'], jitter=True, size=2)
# plt.savefig("clickPay.png")
plt.show()