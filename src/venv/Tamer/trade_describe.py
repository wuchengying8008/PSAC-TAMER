# encoding:utf-8

import os
import pymysql
import pandas as pd
from dbfread import DBF
from sqlalchemy import create_engine


pd.set_option('display.max_rows', 30000)
pd.set_option('display.max_columns', 500)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


database_param = {
    'localhost': {
        'user': 'root',
        'password': 'Hczq123456!!',
        'host': '127.0.0.1',
        'port': 3306,
        'database': 'hc_web'
    },
    'hc_service': {
        'user': 'root',
        'password': 'Hczq123456!!',
        'host': '49.232.20.88',
        'port': 3306,
        'database': 'hc_web'
    }
}


def define_localhost_engine():
    engine_info = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (database_param['localhost']['user'],
                                                                   database_param['localhost']['password'],
                                                                   database_param['localhost']['host'],
                                                                   database_param['localhost']['port'],
                                                                   database_param['localhost']['database'])
    sql_engine = create_engine(engine_info)
    return sql_engine


def define_service_engine(service_name):
    engine_infor = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (database_param[service_name]['user'],
                                                                    database_param[service_name]['password'],
                                                                    database_param[service_name]['host'],
                                                                    database_param[service_name]['port'],
                                                                    database_param[service_name]['database'])
    sql_engine = create_engine(engine_infor)
    return sql_engine


class LenderDescribe:

    def __init__(self):
        # 导入路径
        self.basic_path = os.getcwd()
        self.trade_mark = {
            '5101': '非约定申报',  # 转融券借入非约定
            '5102': '约定申报',  # 转融券借入约定
            '5103': '约定申报',  # 转融券借入市场化约定
            '5132': '提前了结',  # 转融券借入提前了结
            '5121': '展期申报',  # 转融券借入展期
            '5123': '展期申报'  # 市场化转融券借入展期
        }
        self.trade_status = {
            '1': '撤单',  # 已撤单
            '2': '成功',  # 部分成交
            '3': '成功',  # 全部成交
            '4': '成功',  # 对手方已报
            '5': '失败',  # 对手方未报
            'A': '失败',  # 未成交
            '9': '废单'  # 废单
        }
        self.database = {'host': '49.232.20.88', 'user': 'root', 'password': 'Hczq123456!!'}
        self.static_trade_mark_list = ['约定申报', '展期申报', '提前了结']
        self.static_trade_status_list = ['成功', '失败']
        self.product_type = ['ETF', 'LOF', '主动']

    def his_lender(self):
        # 连接数据库
        conn = pymysql.connect(user=self.database['user'],
                               password=self.database['password'],
                               host=self.database['host'])
        cur = conn.cursor()
        # 历史股东账号
        sql = 'select holder_number,lender from hc_web.lend_number;'
        cur.execute(sql)
        df = pd.DataFrame([i for i in cur.fetchall()], columns=[i[0] for i in cur.description])
        df.drop_duplicates(subset=['holder_number'], keep='first', inplace=True)
        # 公募产品信息
        sql = 'select holder_number,ts_code,name,manager from hc_web.number_to_product;'
        cur.execute(sql)
        product_df = pd.DataFrame([i for i in cur.fetchall()], columns=[i[0] for i in cur.description])
        product_df.drop_duplicates(subset=['holder_number'], keep='first', inplace=True)
        # 合并产品
        df = pd.merge(left=df, right=product_df, on=['holder_number'], how='left', indicator=False)
        df.rename(columns={'holder_number': '对方股东账户', 'lender': '出借人', 'ts_code': '产品代码', 'name': '产品简称',
                           'manager': '基金经理'}, inplace=True)
        df.fillna(value='', inplace=True)
        return df

    def process_zrt_data(self):

        # 输入输出地址
        input_dbf_path = self.basic_path + '/daily_zrt_trade/dbf/'
        input_excel_path = self.basic_path + '/daily_zrt_trade/uf20/'

        # === 读取dbf文件
        all_df = pd.DataFrame()
        file_list = sorted(os.listdir(input_dbf_path))
        for f in file_list:
            record_date = str(f).split('.')[0]
            table = DBF(input_dbf_path + f)
            all_columns_list = []
            all_data_list = []
            for record in table:
                all_columns_list.append(record.keys())
                all_data_list.append(record.values())
            # 写入dataframe中
            df = pd.DataFrame(all_data_list, columns=all_columns_list[0])
            # 记录日期
            df['记录日期'] = record_date
            # 合并dataframe
            all_df = pd.concat([all_df, df], ignore_index=True)
        # 输出格式
        all_df = all_df[['记录日期', 'DDRQ', 'DDLX', 'ZQDM', 'CYRDDH', 'DDZT', 'WTSL', 'QXFL', 'QX']]
        # 重命名
        all_df.rename(columns={'DDRQ': '交易日期', 'DDLX': '业务标志', 'ZQDM': '证券代码', 'DDZT': '交易状态', 'CYRDDH': '申请编号',
                               'WTSL': '成交数量', 'QXFL': '成交费率', 'QX': '成交期限'},
                      inplace=True)
        # 进行区间统计
        group_all_df = all_df.groupby(['交易日期', '申请编号']).last()
        group_all_df['区间交易次数'] = all_df.groupby(['交易日期', '申请编号'])['证券代码'].count()
        group_all_df.reset_index(drop=False, inplace=True)

        # === 读取uf20借入委托数据
        all_entrust = pd.DataFrame()
        file_list = sorted(os.listdir(input_excel_path))
        for f in file_list:
            entrust_df = pd.read_excel(input_excel_path + f)
            all_entrust = pd.concat([all_entrust, entrust_df])
        # 输出格式
        all_entrust['证券代码'] = all_entrust['证券代码'].apply(lambda x: str(x).rjust(6, '0'))
        all_entrust = all_entrust[['交易日期', '对方股东账户', '证券代码', '申请编号']]

        # ===合并数据
        group_all_df[['交易日期', '证券代码', '申请编号']] = group_all_df[['交易日期', '证券代码', '申请编号']].astype('str')
        all_entrust[['交易日期', '证券代码', '申请编号']] = all_entrust[['交易日期', '证券代码', '申请编号']].astype('str')
        group_all_df = pd.merge(left=group_all_df, right=all_entrust, on=['交易日期', '证券代码', '申请编号'], how='outer', indicator=True)
        # 剔除掉不属于借入申报的类型(uf20导出的是借入委托的表格)
        group_all_df = group_all_df[group_all_df['_merge'] == 'both']
        del group_all_df['_merge']

        # === 数据处理
        # 业务标志
        group_all_df['业务标志'] = group_all_df['业务标志'].apply(lambda x: self.trade_mark[str(x)])
        # 交易状态
        group_all_df['交易状态'] = group_all_df['交易状态'].apply(lambda x: self.trade_status[str(x)])
        # 剔除不在统计范围内的业务类型
        not_in_static_trade_mark_list = [i for i in self.trade_mark.values() if i not in self.static_trade_mark_list]
        for i in not_in_static_trade_mark_list:
            group_all_df = group_all_df[group_all_df['业务标志'] != i]
        # 剔除不在统计范围内的成交类型
        not_in_static_trade_status_list = [i for i in self.trade_status.values() if i not in self.static_trade_status_list]
        for i in not_in_static_trade_status_list:
            group_all_df = group_all_df[group_all_df['业务标志'] != i]

        # === 读取出借人账号席位文件
        number_info = LenderDescribe().his_lender()
        # 合并
        group_all_df = pd.merge(left=group_all_df, right=number_info, on=['对方股东账户'], how='left', indicator=True)
        group_all_df = group_all_df[group_all_df['_merge'] == 'both']
        del group_all_df['_merge']

        # === 若出借人是基金公司，则会有产品，可以根据产品判断主动还是被动
        def judge_product(x):
            if str(x).endswith('ETF'):
                return 'ETF'
            elif str(x).endswith('A'):
                return 'LOF'
            else:
                return '主动'
        group_all_df['产品类型'] = group_all_df['产品简称'].apply(lambda x: judge_product(x))

        # === 反馈信息
        return group_all_df

    def analyse_zrt_data(self):

        # === 读取转融通交易文件
        df = LenderDescribe().process_zrt_data()
        df['交易月份'] = df['交易日期'].apply(lambda x: str(x)[4: 6])

        # ====== 按照出借人维度分类统计业务类型
        type_list = self.static_trade_mark_list

        # === 交易概览
        group_df = pd.DataFrame()
        group_df['交易次数'] = df.groupby(['出借人'])['区间交易次数'].sum()
        for t in type_list:
            group_df['其中:' + t] = df[df['业务标志'] == t].groupby(['出借人'])['区间交易次数'].sum()
        group_df.fillna(value=0.0, inplace=True)

        # === 交易明细统计
        group_detail_df = pd.DataFrame()
        for i in type_list:
            # 单表
            single_group_df = pd.DataFrame()
            # 类型
            single_group_df['业务类型'] = i
            # 申报笔数
            single_group_df['申报'] = df[df['业务标志'] == i].groupby(['出借人'])['区间交易次数'].sum()
            single_group_df['成交'] = df[(df['业务标志'] == i) & (df['交易状态'] == '成功')].groupby(['出借人'])['区间交易次数'].sum()
            single_group_df['成交'].fillna(value=0.0, inplace=True)
            single_group_df['成功率'] = round(single_group_df['成交'] / single_group_df['申报'], 4)
            # 具体产品类型
            for j in self.product_type:
                single_group_df[j + '-申报'] = df[(df['业务标志'] == i) & (df['产品类型'] == j)].groupby(['出借人'])['区间交易次数'].sum()
                single_group_df[j + '-成交'] = df[(df['业务标志'] == i) & (df['产品类型'] == j) & (df['交易状态'] == '成功')].groupby(['出借人'])['区间交易次数'].sum()
                single_group_df[j + '-成交'].fillna(value=0.0, inplace=True)
                single_group_df[j + '-成功率'] = round(single_group_df[j + '-成交'] / single_group_df[j + '-申报'], 4)
            # 补全信息
            single_group_df['业务类型'].fillna(value=i, inplace=True)
            single_group_df.fillna(value='-', inplace=True)
            # 合并
            group_detail_df = pd.concat([group_detail_df, single_group_df])

        # === 按照公募及产品维度统计展期成功率
        # === 展期统计
        product_extension_df = pd.DataFrame()
        # 股东账号集合
        product_extension_df['股东账号'] = df.groupby(['出借人', '产品代码', '产品简称'])['对方股东账户'].apply(lambda x: '|'.join(set(x)))
        # 展期申报-笔数
        product_extension_df['展期-申报'] = df[df['业务标志'] == '展期申报'].groupby(['出借人', '产品代码', '产品简称'])['区间交易次数'].sum()
        # 展期成交-笔数
        product_extension_df['展期-成交'] = df[(df['业务标志'] == '展期申报') & (df['交易状态'] == '成功')].groupby(['出借人', '产品代码', '产品简称'])['区间交易次数'].sum()
        product_extension_df['展期-成交'].fillna(value=0.0, inplace=True)
        # 成功率-笔数(展期的成功率主观感受为笔，而非市值；此外同一笔合约多次报展期，失败也是考虑在内的)
        product_extension_df['展期成功率'] = round(product_extension_df['展期-成交'] / product_extension_df['展期-申报'], 4)
        product_extension_df.fillna(value='-', inplace=True)

        # === 失败借入及失败展期的月份分布
        # 按照月份统计失败及成功的数量及总占比
        group_month_df = pd.DataFrame()
        for i in type_list:
            group_month_df[i + '-申报'] = df[df['业务标志'] == i].groupby(['出借人', '交易月份'])['区间交易次数'].sum()
            group_month_df[i + '-失败'] = df[(df['业务标志'] == i) & (df['交易状态'] == '失败')].groupby(['出借人', '交易月份'])['区间交易次数'].sum()
            group_month_df[i + '-失败'].fillna(value=0.0, inplace=True)  # 分子可以补全为0
            group_month_df[i + '-失败率'] = round(group_month_df[i + '-失败'] / group_month_df[i + '-申报'], 4)
        group_month_df.fillna(value='-', inplace=True)

        # # ==== 输出及打印
        # writer = pd.ExcelWriter('公募基金交易指标统计-{}.xlsx'.format(lender.replace(' ', '').split('-')[1]))
        # group_df.to_excel(writer, '交易概览')
        # group_detail_df.to_excel(writer, '交易明细')
        # product_extension_df.to_excel(writer, '产品展期申报')
        # group_month_df.to_excel(writer, '交易月份统计')
        # writer.close()

        # 返回信息
        return {'overall': group_df, 'detail': group_detail_df, 'product_detail': product_extension_df, 'month_detail': group_month_df}

    def tagging_lender(self, input_analyse_zrt_data):
        pass


if __name__ == '__main__':

    # 定义数据库
    localhost_db = define_localhost_engine()
    service_db = define_service_engine('hc_service')

    # === 遍历获取画像
    output_dict = LenderDescribe().analyse_zrt_data()

    # === 交易总表重命名
    overall_df = output_dict['overall']
    overall_df.reset_index(drop=False, inplace=True)
    overall_df.rename(columns={'出借人': 'lender', '交易次数': 'trade_times', '其中:约定申报': 'borrow_times',
                               '其中:展期申报': 'extension_times', '其中:提前了结': 'finish_times'}, inplace=True)

    # === 交易明细表重命名
    detail_df = output_dict['detail']
    detail_df.reset_index(drop=False, inplace=True)
    detail_df.rename(columns={'出借人': 'lender', '业务类型': 'business_type', '申报': 'declare', '成交': 'deal', '成功率': 'success_rate',
                              'ETF-申报': 'etf_declare', 'ETF-成交': 'etf_deal', 'ETF-成功率': 'etf_success_rate',
                              'LOF-申报': 'lof_declare', 'LOF-成交': 'lof_deal', 'LOF-成功率': 'lof_success_rate',
                              '主动-申报': 'act_declare', '主动-成交': 'act_deal', '主动-成功率': 'act_success_rate', 'index': 'lender'}, inplace=True)

    # === 产品明细表重命名
    product_detail_df = output_dict['product_detail']
    product_detail_df.reset_index(drop=False, inplace=True)
    product_detail_df.rename(columns={'出借人': 'lender', '产品代码': 'ts_code', '产品简称': 'name', '股东账号': 'holder_number',
                                      '展期-申报': 'extension_declare', '展期-成交': 'extension_deal', '展期成功率': 'extension_success_rate'}, inplace=True)

    # === 月份明细表重命名
    month_detail_df = output_dict['month_detail']
    month_detail_df.reset_index(drop=False, inplace=True)
    month_detail_df.rename(columns={'出借人': 'lender', '交易月份': 'month',
                                    '约定申报-申报': 'borrow_declare', '约定申报-失败': 'borrow_fail', '约定申报-失败率': 'borrow_fail_rate',
                                    '展期申报-申报': 'extension_declare', '展期申报-失败': 'extension_fail', '展期申报-失败率': 'extension_fail_rate',
                                    '提前了结-申报': 'finish_declare', '提前了结-失败': 'finish_fail', '提前了结-失败率': 'finish_fail_rate'}, inplace=True)

    for engine in [service_db, localhost_db]:
        overall_df.to_sql(name='lender_overall_trade_portrait', con=engine, if_exists='replace', index=False)
        detail_df.to_sql(name='lender_detail_trade_portrait', con=engine, if_exists='replace', index=False)
        product_detail_df.to_sql(name='lender_product_trade_portrait', con=engine, if_exists='replace', index=False)
        month_detail_df.to_sql(name='lender_month_portrait', con=engine, if_exists='replace', index=False)

