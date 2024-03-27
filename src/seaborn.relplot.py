import seaborn as sns
import matplotlib.pyplot as plt
import pandas



def rgb_to_hex(rgb: tuple = None):
    if rgb:
        return ''.join([str(hex(num)).replace('0x', '').zfill(2) for num in rgb])
# 输入数据

# 设置颜色代码
color1 ='#d4eded'
    #'#'+rgb_to_hex(rgb=(246,235,020))
#"#038355" # 孔雀绿
color2 = "#1f5681" # 向日黄
# 设置字体
font = {'family' : 'Times New Roman',
        'size'   : 12}
plt.rc('font', **font)
#data = sns.load_dataset('tips', cache=True, data_home=None)
data=pandas.read_csv('D:\score1.csv')
sns.set_style("whitegrid") # 设置背景样式
sns.relplot(
    x=None, y=None,   #x, y：data中的变量名 输入数据的变量；数据必须为数值型。
    hue=None,  #将会产生具有不同颜色的元素的变量进行分组。这些变量可以是类别变量或者数值型变量
    size=None,  #用粗细表现出分组的不同。可以是分组或数字(10, 100)
    style=None, #cue 虚线 stim实线 也可以是分组
    data=data,  #DataFrame
    row=None, col=None,  #col列分组 row行分组
    col_wrap=None,  #int这个变量设置可以将多列包装以多行的形式展现(有时太多列展现，不便利)，但不可以将多行以多列的形式展现。
    row_order=None,col_order=None,   #以此顺序组织网格的行和/或列，否则顺序将从数据对象中推断
    palette=None,  #["b", "r"] 列表格式 对不同分组设定不同颜色
    hue_order=None,  #列表 指定hue变量层级出现的顺序 否则会根据数据确定
    hue_norm=None, #元组或者 Normalize 对象
    sizes=None,  #列表、字典或者元组 当使用sizes时，用于确定如何选择尺寸。此变量可以一直是尺寸值的列表或者size变量的字典映射。
                #当size为数值型时，此变量也可以是指定最小和最大尺寸的元组，这样可以将其他值标准化到这个范围
    size_order=None,  #列表  指定size变量层次的表现顺序，不指定则会通过数据确定。当size变量为数值型时与此无关
    size_norm=None,  #元组或者 Normalize 对象   当size变量为数值型时，用于数据单元的 scaling plot 对象的标准化
    legend='brief',  #“brief”, “full”, 或者 False,
                    #用于决定如何绘制坐标轴。如果参数值为“brief”, 数值型的hue以及size变量将会被用等间隔采样值表示。
                    #如果参数值为“full”, 每组都会在坐标轴中被记录。如果参数值为“false”, 不会添加坐标轴数据，也不会绘制坐标轴。
    kind='line', #可选项为(scatter 散点图 及line 曲线图).
    height=5,  #每个 生成图 的高度
    aspect=1, #每个 生成图 的长宽比
)

# 添加标题和标签
plt.title("Title", fontweight='bold', fontsize=14)
plt.xlabel("X Label", fontsize=12)
plt.ylabel("Y Label", fontsize=12)

# 添加图例
plt.legend(loc='upper left', frameon=True, fontsize=10)

# 设置刻度字体和范围
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.xlim(0, 100)
plt.ylim(0, 200)

# 设置坐标轴样式
for spine in plt.gca().spines.values():
    spine.set_edgecolor("#CCCCCC")
    spine.set_linewidth(1.5)

plt.savefig('lineplot.png', dpi=300, bbox_inches='tight')
# 显示图像
plt.show()
