import pymysql
import pandas as pd
import pandas_market_calendars as mcal


def get_df_from_db(sql):
    db = pymysql.connect(
            host='192.168.8.167',  # 数据库主机名
            port=3306,               # 数据库端口号，默认为3306
            user='rzrqtest',             # 数据库用户名
            passwd='rzrqTest!@34',         # 数据库密码
            db='rzrq',               # 数据库名称
            charset='utf8'           # 字符编码
            )
    cursor = db.cursor()#使用cursor()方法获取用于执行SQL语句的游标
    cursor.execute(sql)# 执行SQL语句
    """
    使用fetchall函数以元组形式返回所有查询结果并打印出来
    fetchone()返回第一行，fetchmany(n)返回前n行
    游标执行一次后则定位在当前操作行，下一次操作从当前操作行开始
    """
    data = cursor.fetchall()

    #下面为将获取的数据转化为dataframe格式
    columnDes = cursor.description #获取连接对象的描述信息
    columnNames = [columnDes[i][0] for i in range(len(columnDes))] #获取列名
    df = pd.DataFrame([list(i) for i in data],columns=columnNames) #得到的data为二维元组，逐行取出，转化为列表，再转化为df
    
    """
    使用完成之后需关闭游标和数据库连接，减少资源占用,cursor.close(),db.close()
    db.commit()若对数据库进行了修改，需进行提交之后再关闭
    """
    cursor.close()
    db.close()

    #print("cursor.description中的内容：",columnDes)
    return df

# 定义一个函数来计算统计信息
def calculate_user_stats(user_data, s):
    user_stats = {
        'Mean': user_data[s].mean(),
        'Median': user_data[s].median(),
        'Std': user_data[s].std(),
        '75th Percentile': user_data[s].quantile(0.75),
        '25th Percentile': user_data[s].quantile(0.25)
        #'深圳':user_data['交易类别'].value_counts()['深圳']
        # '上海':
    }
    return pd.Series(user_stats)
        
    

def success(user_data):
    return user_data['转融通委托状态'].mean()


if __name__ == "__main__":

    sql1 = "SELECT * FROM borrowdeclaration21"
    sql2 = "SELECT * FROM borrowdeclaration23"
    sql3 = "SELECT * FROM rzrq.shareholderaccounthistory"

    df1 = get_df_from_db(sql1)
    df1 = df1[['交易日期', '转融通委托状态', '交易类别', '对方股东账户','证金合约编号']]
    df2 = get_df_from_db(sql2)
    df2 = df2[['交易日期', '转融通委托状态', '交易类别', '对方股东账户', '证金合约编号']]
    df3 = get_df_from_db(sql3)
    df3 = df3[['holder_number', 'lender']]
    df = pd.concat([df1, df2])
    df = df.rename(columns = {'对方股东账户':'holder_number'})
    df_merged = df.merge(df3[['holder_number', 'lender']], on='holder_number', how='left')


    df_qr = df_merged[(df_merged["转融通委托状态"] == '成交且调仓成功') | ((df_merged["转融通委托状态"] == '已确认') & (~df_merged["证金合约编号"].empty) & (df_merged["证金合约编号"] != None))]
    #df_qr['转融通委托状态'] = (df_qr['转融通委托状态'] == '成交且调仓成功') | ((df_qr['转融通委托状态'] == '已确认') & (~df_qr['证金合约编号'].isna()))
    #s = '转融通期限天数'

    '''
    # 创建交易所对象
    exchange = mcal.get_calendar(exchange_name)
    # 指定要查询的时间段
    start_date = '2021-01-01'
    end_date = '2023-12-31'
    
    # 获取指定时间段的交易日
    trading_days = exchange.valid_days(start_date=start_date, end_date=end_date)
    
    # 将交易日转换为 Pandas DataFrame
    trade_day = pd.DataFrame({'date': trading_days})
    
    # 将日期时间列从字符串转换为 Pandas 的日期时间格式
    trade_day['date'] = pd.to_datetime(trade_day['date'])
    '''

    # 将日期时间格式化为所需的字符串格式
    df_qr['交易日期'] = pd.to_datetime(df_qr['交易日期'])
    #df_qr[s] = df_qr[s].astype('float')
    #df_qr['转融通委托状态'] = df_qr['转融通委托状态'].astype('float')

    #result1 = df_qr[df_qr['交易日期'].isin(trade_day['date'])]
    #result2 = df_qr[~df_qr['交易日期'].isin(trade_day['date'])]
    user_type = ''

    # 按月分组并计算统计信息
    monthly_stats = df_qr.groupby([df_qr['lender'], df_qr['交易日期'].dt.to_period('M')]).apply(calculate_user_stats, s = user_type)
    print(monthly_stats)

    # 按年分组并计算统计信息
    yearly_stats = df_qr.groupby([df_qr['lender'], df_qr['交易日期'].dt.to_period('Y')]).apply(calculate_user_stats,  s = user_type)
    
    # 按星期分组并计算统计信息
    weekly_stats = df_qr.groupby([df_qr['lender'], df_qr['交易日期'].dt.to_period('W')]).apply(calculate_user_stats,  s = user_type)
    #print(user_grouped)

    df = monthly_stats.to_csv('D:/monthly_stats_numbers_cjv.csv',encoding="utf_8_sig")
    df = yearly_stats.to_csv('D:/yearly_stats_numbers_cjv.csv',encoding="utf_8_sig")
    df = weekly_stats.to_csv('D:/weekly_stats_numbers_cjv.csv',encoding="utf_8_sig")


'''
# 提取年、月和周信息
result1['Year'] = result1['交易日期'].dt.year
result1['Month'] = result1['交易日期'].dt.month
result1['Week'] = result1['交易日期'].dt.week

# 分组并计算成功交易率
grouped = result1.groupby(['lender', 'Week'])
result = grouped['转融通委托状态'].mean().reset_index()


#df = result.to_csv('D:/monthly_stats_numbers_cjv.csv',encoding="utf_8_sig")
#df = result.to_csv('D:/yearly_stats_numbers_cjv.csv',encoding="utf_8_sig")
df = result.to_csv('D:/weekly_stats_numbers_cjv.csv',encoding="utf_8_sig")

# 打印结果
print(result)

'''











