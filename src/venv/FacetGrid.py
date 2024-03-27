import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
tips = pd.read_csv(r"tips.csv")
axes = sns.scatterplot(x="total_bill",y="tip",data=tips)
#利用Axes对象的函数设置一些属性
axes.set_xticks(range(0,60,5))

#g1 = sns.FacetGrid(tips)
#g1.map(plt.scatter,"total_bill","tip")


#fig,[ax1,ax2] = plt.subplots(1,2,figsize=(20,5))

#sns.scatterplot(x="total_bill",y="tip",data=tips,ax=ax1)

#sns.barplot(x="day",y="total_bill",data=tips,ax=ax2)


##sns.scatterplot(x=tips['total_bill'],y='tip',data=tips)

#g1 = sns.FacetGrid(tips)
#g1.map(plt.scatter,"total_bill","tip")


#g2 = sns.FacetGrid(tips,col="day",col_wrap=2)
#g2.map(plt.scatter,"total_bill","tip")

#g2 = sns.FacetGrid(tips,col="day",hue="time")
#g2.map(plt.scatter,"total_bill","tip")

#g2.add_legend()



#
g = sns.FacetGrid(tips,col="day",row="time")
g.map(sns.regplot,"total_bill","tip")

#g.set_titles(template="{row_var}/{row_name}")

g.set_titles(template="{col_var}/{col_name}title")

plt.show()
