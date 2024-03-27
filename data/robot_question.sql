/*
Navicat MySQL Data Transfer

Source Server         : 47.98.233.4
Source Server Version : 100214
Source Host           : 47.98.233.4:3307
Source Database       : gaas

Target Server Type    : MYSQL
Target Server Version : 100214
File Encoding         : 65001

Date: 2020-02-10 17:13:12
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for robot_question
-- ----------------------------
DROP TABLE IF EXISTS `robot_question`;
CREATE TABLE `robot_question` (
  `id` int(10) unsigned zerofill NOT NULL COMMENT '主键id',
  `ques_title` varchar(255) DEFAULT NULL,
  `ques_short` varchar(255) DEFAULT '' COMMENT '同义词',
  `ques_type` varchar(255) DEFAULT NULL,
  `answ_refid` varchar(255) DEFAULT NULL COMMENT '问题相关问题',
  `is_reply` varchar(255) DEFAULT NULL COMMENT '是否有答案',
  `key_words` varchar(255) DEFAULT NULL COMMENT '关键词',
  `cata_id` int(11) DEFAULT NULL COMMENT '目录id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of robot_question
-- ----------------------------
INSERT INTO `robot_question` VALUES ('0000000001', '创业板的企业如果连续亏损会被加st吗', '创业板企业连续亏损会被加st', '1', '1,2,3', '1', '创业板,亏损,ST', '10020002');
INSERT INTO `robot_question` VALUES ('0000000002', '潜客录入', '我要增加客户', '3', null, '1', '新增,客户', '10010004');
INSERT INTO `robot_question` VALUES ('0000000003', '工作日历', '今天要做什么', '3', null, '1', '工作,日历', '10010004');
INSERT INTO `robot_question` VALUES ('0000000004', '服务记录', '打开服务记录', '3', null, '1', '服务,记录', '10010004');
INSERT INTO `robot_question` VALUES ('0000000005', '财经早餐', '我想看财经早餐/早报', '3', null, '1', '财经,早餐,早报', '10010004');
INSERT INTO `robot_question` VALUES ('0000000006', '新闻资讯', '今天有什么新闻', '3', null, '1', '新闻,资讯', '10010004');
INSERT INTO `robot_question` VALUES ('0000000007', '客户互动', '哪些客户比较活跃', '3', null, '1', '客户,互动,活跃', '10010004');
INSERT INTO `robot_question` VALUES ('0000000008', '建议书', '想看看建议书', '3', null, '1', '建议书', '10010004');
INSERT INTO `robot_question` VALUES ('0000000009', '最新产品', '最新上架了什么产品', '3', null, '1', '新,产品', '10010004');
INSERT INTO `robot_question` VALUES ('0000000010', '我的自选', '我的自选', '3', null, '1', '自选,产品', '10010004');
INSERT INTO `robot_question` VALUES ('0000000011', '公募基金', '公募产品', '3', null, '1', '公募,基金,产品', '10010004');
INSERT INTO `robot_question` VALUES ('0000000012', '产品超市', '有哪些产品在卖', '3', null, '1', '产品,卖,超市', '10010004');
INSERT INTO `robot_question` VALUES ('0000000013', '推荐产品', '有什么产品推荐吗', '3', null, '1', '推荐,产品', '10010004');
INSERT INTO `robot_question` VALUES ('0000000014', '精选组合', '有什么组合推荐', '3', '', '1', '精选,组合,推荐', '10010004');
INSERT INTO `robot_question` VALUES ('0000000015', '投资规划', '投资规划', '3', null, '1', '投资,规划', '10010004');
INSERT INTO `robot_question` VALUES ('0000000016', '我的客户', '我想看全部客户', '3', null, '1', '客户', '10010004');
INSERT INTO `robot_question` VALUES ('0000000017', '今日总结', '我的工作任务', '3', null, '1', '任务,总结,工作,四步工作法', '10010004');
INSERT INTO `robot_question` VALUES ('0000000018', '倾听', '倾听', '3', null, '1', '倾听', '10010004');
INSERT INTO `robot_question` VALUES ('0000000019', '建议', '我想要看建议', '3', null, '1', '建议', '10010004');
INSERT INTO `robot_question` VALUES ('0000000020', '实施', '我想要看实施任务', '3', null, '1', '实施', '10010004');
INSERT INTO `robot_question` VALUES ('0000000021', '跟踪', '我想要看跟踪任务', '3', '', '1', '跟踪', '10010004');
INSERT INTO `robot_question` VALUES ('0000000022', '精美海报', '最新海报', '3', null, '1', '海报', '10010004');
INSERT INTO `robot_question` VALUES ('0000000023', '预约查询', '预约查询', '3', null, '1', '预约,查询', '10010004');
INSERT INTO `robot_question` VALUES ('0000000024', '到账查询', '我想查询到账情况', '3', null, '1', '到账,查询', '10010004');
INSERT INTO `robot_question` VALUES ('0000000025', '业绩确认', '我的业绩确认情况如何', '3', null, '1', '业绩,确认', '10010004');
INSERT INTO `robot_question` VALUES ('0000000026', '合同录入', '我想查看合同', '3', null, '1', '合同', '10010004');
INSERT INTO `robot_question` VALUES ('0000000027', '精品课堂', '我要学习', '3', null, '1', '学习，课程', '10010004');
INSERT INTO `robot_question` VALUES ('0000000028', '精准营销', '我想看精准营销', '3', null, '1', '精准营销', '10010004');
INSERT INTO `robot_question` VALUES ('0000000029', '客群贡献', '我想看客群贡献', '3', null, '1', '客群,贡献', '10010004');
INSERT INTO `robot_question` VALUES ('0000000030', '资金运用', '我想看资金运用情况', '3', null, '1', '资金运,用', '10010004');
INSERT INTO `robot_question` VALUES ('0000000031', '销售漏斗', '我想看销售漏斗/销售情况', '3', null, '1', '销售,漏斗', '10010004');
INSERT INTO `robot_question` VALUES ('0000000032', '智能KYC', '我要查公司信息', '3', null, '1', '查询,公司,情况', '10010004');
INSERT INTO `robot_question` VALUES ('0000000100', '以前开过基金账户，还需要重新开户么？', '开过基金账户，需要重新开户么', '1', null, '1', '基金,账户,已经,重新,开户', '10010001');
INSERT INTO `robot_question` VALUES ('0000000101', '我的银行卡在别处已有账户了，能在再开户吗？会有冲突吗？', '银行卡在别处已有账户了，能在再开户吗？会有冲突吗？', '1', null, '1', '银行卡,再,开户,冲突', '10010001');
INSERT INTO `robot_question` VALUES ('0000000102', '开户多久之后能得到确认？', '开户多久之后能得到确认', '1', null, '1', '开户,久,确认', '10010001');
INSERT INTO `robot_question` VALUES ('0000000103', '我一直没有收到绑定手机的短信验证码？', '没有收到绑定手机的短信验证码', '1', null, '1', '短信,验证码', '10010001');
INSERT INTO `robot_question` VALUES ('0000000104', '信用卡、存折可以开户吗？', '信用卡、存折可以开户吗', '1', null, '1', '信用卡,存折卡,开户', '10010001');
INSERT INTO `robot_question` VALUES ('0000000105', '一个账号可以挂多张银行卡么？', '一个账号可以挂多张银行卡么？', '1', null, '1', '多,银行卡', '10010001');
INSERT INTO `robot_question` VALUES ('0000000106', '什么是预留信息？', '什么是预留信息？', '1', null, '1', '预留信息', '10010001');
INSERT INTO `robot_question` VALUES ('0000000107', '设置预留信息有什么用？', '设置预留信息有什么用？', '1', null, '1', '预留信息,用', '10010001');
INSERT INTO `robot_question` VALUES ('0000000108', '如何设置交易密码？', '如何设置交易密码？', '1', null, '1', '设置,交易,密码', '10010001');
INSERT INTO `robot_question` VALUES ('0000000109', '绑定银行卡必须和开户人一致么？', '绑定银行卡必须和开户人一致么？', '1', null, '1', '银行卡,开户人,本人', '10010001');
INSERT INTO `robot_question` VALUES ('0000000110', '申购多长时间可以确认?', '申购多长时间可以确认?', '1', null, '1', '申购,久,时间,确认', '10010003');
INSERT INTO `robot_question` VALUES ('0000000111', '申购操作有时间限制么', '申购操作有时间限制么', '1', null, '1', '申购,时间,限制', '10010003');
INSERT INTO `robot_question` VALUES ('0000000112', '申购基金，按哪一天的净值计算份额？', '申购基金，按哪一天的净值计算份额？', '1', null, '1', '申购,净值,份额,计算,天', '10010003');
INSERT INTO `robot_question` VALUES ('0000000113', '申购操作有金额限制么？', '申购操作有金额限制么？', '1', null, '1', '申购,金额,限制', '10010003');
INSERT INTO `robot_question` VALUES ('0000000114', '申购基金之后什么时候开始享受基金的收益？', '申购基金之后什么时候开始享受基金的收益？', '1', null, '1', '基金,收益,久,时间', '10010003');
INSERT INTO `robot_question` VALUES ('0000000115', '申购能够撤销么？', '申购能够撤销么？', '1', null, '1', '申购,撤销', '10010003');
INSERT INTO `robot_question` VALUES ('0000000116', '申购撤销后钱多久返回银行账户?', '申购撤销后钱多久返回银行账户?', '1', null, '1', '申购,撤销,钱,返', '10010003');
INSERT INTO `robot_question` VALUES ('0000000117', '为什么才申购的基金当天不能赎回？', '为什么才申购的基金当天不能赎回？', '1', null, '1', '申购,赎回', '10010003');
INSERT INTO `robot_question` VALUES ('0000000118', '赎回多长时间可以确认?', '赎回多长时间可以确认?', '1', null, '1', '赎回,确认', '10000001');
INSERT INTO `robot_question` VALUES ('0000000119', '赎回操作有时间限制么？', '赎回操作有时间限制么？', '1', null, '1', '赎回,限制,久,时间', '10000001');
INSERT INTO `robot_question` VALUES ('0000000120', '赎回操作有金额限制么？', '赎回操作有金额限制么？', '1', null, '1', '赎回,限制,钱,时间', '10000001');
INSERT INTO `robot_question` VALUES ('0000000121', '赎回能够撤销么？', '赎回能够撤销么？', '1', null, '1', '赎回,撤销', '10000001');
INSERT INTO `robot_question` VALUES ('0000000122', '赎回后，钱多久返回账户？', '赎回后，钱多久返回账户？', '1', null, '1', '赎回,钱,返', '10000001');
INSERT INTO `robot_question` VALUES ('0000000123', '货币基金全额赎回时，未分配收益部分如何处理？', '货币基金全额赎回时，未分配收益部分如何处理？', '1', null, '1', '全部,赎回,未分配收益', '10000001');
INSERT INTO `robot_question` VALUES ('0000000124', '基金有几种分红方式？', '基金有几种分红方式？', '1', null, '1', '分红,方式', '10010002');
INSERT INTO `robot_question` VALUES ('0000000125', '基金分红方式可以选择么？', '基金分红方式可以选择么？', '1', null, '1', '分红,选择', '10010002');
INSERT INTO `robot_question` VALUES ('0000000126', '修改分红方式后多长时间生效？', '修改分红方式后多长时间生效？', '1', null, '1', '修改,分红,生效', '10010002');
INSERT INTO `robot_question` VALUES ('0000000127', '明天是权益登记日，现在修改分红方式还来得及吗？', '明天是权益登记日，现在修改分红方式还来得及吗？', '1', null, '1', '权益登记日,修改,分红', '10010002');
INSERT INTO `robot_question` VALUES ('0000000128', '什么时候持有基金才能享受基金分红？', '什么时候持有基金才能享受基金分红？', '1', null, '1', '久,时间,分红', '10010002');
INSERT INTO `robot_question` VALUES ('0000000129', '什么是红利再投资？', '什么是红利再投资？', '1', null, '1', '红利再投', '10010002');
INSERT INTO `robot_question` VALUES ('0000000130', '红利再投资有什么优点？', '红利再投资有什么优点？', '1', null, '1', '红利再投,特点', '10010002');
INSERT INTO `robot_question` VALUES ('0000000131', '选择红利再投资方式是以哪一天的净值计算分红份额的?', '选择红利再投资方式是以哪一天的净值计算分红份额的?', '1', null, '1', '红利再投,算', '10010002');
INSERT INTO `robot_question` VALUES ('0000000132', '选择红利再投资方式何时可以赎回?', '选择红利再投资方式何时可以赎回?', '1', null, '1', '红利再投,赎回', '10010002');
INSERT INTO `robot_question` VALUES ('0000000133', '系统提示我输入交易密码，这个密码是银行卡的密码还是基金账户的密码？', '系统提示我输入交易密码，这个密码是银行卡的密码还是基金账户的密码？', '1', null, '1', '交易密码', '10010004');
INSERT INTO `robot_question` VALUES ('0000000134', '我输入交易密码之后，我的交易能够保证安全吗？', '我输入交易密码之后，我的交易能够保证安全吗？', '1', null, '1', '交易密码,安全', '10010004');
INSERT INTO `robot_question` VALUES ('0000000135', '为什么会出现申请时间与所属交易日不在同一天的现象？', '为什么会出现申请时间与所属交易日不在同一天的现象？', '1', null, '1', '申请,时间,日期,交易日', '10010004');
INSERT INTO `robot_question` VALUES ('0000000136', '我提交交易申请之后还要去基金公司或者银行进行确认吗？', '我提交交易申请之后还要去基金公司或者银行进行确认吗？', '1', null, '1', '交易,申请,确认', '10010004');
INSERT INTO `robot_question` VALUES ('0000000137', '什么是基金的本质', '什么是基金的本质', '1', null, '1', '基金,本质', '10020001');
INSERT INTO `robot_question` VALUES ('0000000138', '谁是基金的参与者', '谁是基金的参与者', '1', null, '1', '基金,参与者', '10020001');
INSERT INTO `robot_question` VALUES ('0000000139', '基金与股票有什么不同', '基金与股票有什么不同', '1', null, '1', '基金,股票', '10020001');
INSERT INTO `robot_question` VALUES ('0000000140', '基金与债券有什么不同', '基金与债券有什么不同', '1', null, '1', '基金,债券', '10020002');
INSERT INTO `robot_question` VALUES ('0000000141', '基金与银行存款有什么不同', '基金与银行存款有什么不同', '1', null, '1', '基金,存款,银行', '10020002');
INSERT INTO `robot_question` VALUES ('0000000142', '基金适合短线炒作还是长期投资？', '基金适合短线炒作还是长期投资？', '1', null, '1', '基金,短线,长', '10020002');
INSERT INTO `robot_question` VALUES ('0000000143', '选股票基金还是债券基金？', '选股票基金还是债券基金？', '1', null, '1', '股票基金,债券基金', '10020002');
INSERT INTO `robot_question` VALUES ('0000000144', '选一家基金还是多家基金？', '选一家基金还是多家基金？', '1', null, '1', '一,多,基金,1', '10020002');
INSERT INTO `robot_question` VALUES ('0000000145', '如何评价基金绩效？', '如何评价基金绩效？', '1', null, '1', '基金,评价,绩效', '10020002');
INSERT INTO `robot_question` VALUES ('0000000146', '如何确定自己的风险承受能力', '如何确定自己的风险承受能力', '1', null, '1', '风险,承受', '10020005');
INSERT INTO `robot_question` VALUES ('0000000147', '投资基金的主要风险有哪些', '投资基金的主要风险有哪些', '1', null, '1', '基金,风险', '10020005');
INSERT INTO `robot_question` VALUES ('0000000148', '开放式基金投资收益来源有哪些', '开放式基金投资收益来源有哪些', '1', null, '1', '开放式基金,收益', '10020005');
INSERT INTO `robot_question` VALUES ('0000000149', '个人投资开放式基金收益来源有哪些', '个人投资开放式基金收益来源有哪些', '1', null, '1', '开放式基金,个人', '10020005');
INSERT INTO `robot_question` VALUES ('0000000150', '为什么基金净值会出现异常波动', '为什么基金净值会出现异常波动', '1', null, '1', '净值,波动', '10020005');
INSERT INTO `robot_question` VALUES ('0000000151', '基金投资方式有哪些', '基金投资方式有哪些', '1', null, '1', '基金,投资方式', '10020005');
INSERT INTO `robot_question` VALUES ('0000000152', '如何防范基金投资风险', '如何防范基金投资风险', '1', '', '1', '基金,风险', '10020005');
INSERT INTO `robot_question` VALUES ('0000000153', '基金分类有哪些', '基金分类有哪些', '1', null, '1', '基金,类', '10020005');
INSERT INTO `robot_question` VALUES ('0000000154', '封闭式基金', '封闭式基金', '1', null, '1', '封闭式,基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000155', '开放式基金', '开放式基金', '1', null, '1', '开放式,基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000156', '契约型基金', '契约型基金', '1', null, '1', '契约型,基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000157', '公司型基金', '公司型基金', '1', null, '1', '公司型,基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000158', '股票型基金', '股票型基金', '1', null, '1', '股票型,基金,股票基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000159', '债券型基金', '债券型基金', '1', null, '1', '债券型,基金,债券基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000160', '货币市场基金', '货币市场基金', '1', null, '1', '货币市场基金,货币,基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000161', '混合基金', '混合基金', '1', null, '1', '混合基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000162', '增长型基金', '增长型基金', '1', null, '1', '增长型基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000163', '收入型基金', '收入型基金', '1', null, '1', '收入型基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000164', '平衡型基金', '平衡型基金', '1', null, '1', '平衡型基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000165', '主动型基金', '主动型基金', '1', null, '1', '主动型基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000166', '被动型基金', '被动型基金', '1', null, '1', '被动型基金,指数型', '10020005');
INSERT INTO `robot_question` VALUES ('0000000167', '公募基金', '公募基金', '1', null, '1', '公募基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000168', '私募基金', '私募基金', '1', null, '1', '私募基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000169', '在岸基金', '在岸基金', '1', null, '1', '在岸基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000170', '离岸基金', '离岸基金', '1', null, '1', '离岸基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000171', '系列基金', '系列基金', '1', null, '1', '系列基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000172', '基金中的基金', '基金中的基金', '1', null, '1', '基金中的基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000173', '保本基金', '保本基金', '1', null, '1', '保本基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000174', '交易型开放式指数基金（ETF）与ETF联接基金', '交易型开放式指数基金（ETF）与ETF联接基金', '1', null, '1', '交易型开放式指数基金,ETF', '10020005');
INSERT INTO `robot_question` VALUES ('0000000175', '上市开放型基金', '上市开放型基金', '1', null, '1', '上市开放型基金,EOF', '10020005');
INSERT INTO `robot_question` VALUES ('0000000176', 'QDII基金', 'QDII基金', '1', null, '1', 'QDII基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000177', '分级基金', '分级基金', '1', null, '1', '分级基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000178', '契约型基金与公司型基金的区别', '契约型基金与公司型基金的区别', '1', null, '1', '公司型基金,契约型基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000179', '认购和申购的区别', '认购和申购的区别', '1', null, '1', '认购,申购', '10020005');
INSERT INTO `robot_question` VALUES ('0000000180', '基金净值', '基金净值', '1', null, '1', '基金,净值', '10020005');
INSERT INTO `robot_question` VALUES ('0000000181', '累计净值', '单位累计净值', '1', null, '1', '累计,净值', '10020005');
INSERT INTO `robot_question` VALUES ('0000000182', '万份收益', '万份基金单位收益', '1', null, '1', '万份,收益', '10020005');
INSERT INTO `robot_question` VALUES ('0000000183', '七日年化收益率', '七日年化收益率', '1', null, '1', '七日年化收益率', '10020005');
INSERT INTO `robot_question` VALUES ('0000000184', '参考市值', '参考市值', '1', null, '1', '参考市值', '10020005');
INSERT INTO `robot_question` VALUES ('0000000185', '基金开放日', '基金开放日', '1', null, '1', '基金,开放日', '10020005');
INSERT INTO `robot_question` VALUES ('0000000186', 'T日', 'T日', '1', null, '1', 'T日', '10020005');
INSERT INTO `robot_question` VALUES ('0000000187', '未知价原则', '未知价法', '1', null, '1', '未知价', '10020005');
INSERT INTO `robot_question` VALUES ('0000000188', '基金认购', '基金认购', '1', null, '1', '认购', '10020005');
INSERT INTO `robot_question` VALUES ('0000000189', '封闭建仓期', '封闭建仓期', '1', null, '1', '封闭', '10020005');
INSERT INTO `robot_question` VALUES ('0000000190', '基金转换及基金转换好处', '基金转换及基金转换好处', '1', null, '1', '基金转换', '10020005');
INSERT INTO `robot_question` VALUES ('0000000191', '转托管', '转托管', '1', null, '1', '转托管', '10020005');
INSERT INTO `robot_question` VALUES ('0000000192', '基金定投', '懒人理财', '1', null, '1', '定投', '10020005');
INSERT INTO `robot_question` VALUES ('0000000193', '非交易过户', '非交易过户', '1', null, '1', '非交易过户', '10020005');
INSERT INTO `robot_question` VALUES ('0000000194', '分级基金的特点', '结构型基金', '1', null, '1', '结构型基金,分级基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000195', '什么叫巨额赎回', '什么叫巨额赎回', '1', '', '1', '巨额赎回', '10020005');
INSERT INTO `robot_question` VALUES ('0000000196', '为什么基金暂停交易', '为什么基金暂停交易', '1', null, '1', '基金,暂停交易', '10020005');
INSERT INTO `robot_question` VALUES ('0000000197', '什么是强增(强减)', '什么是强增(强减)', '1', null, '1', '强增,强减', '10020005');
INSERT INTO `robot_question` VALUES ('0000000198', '保本基金真的保本吗', '保本基金真的保本吗', '1', null, '1', '保本,基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000199', '什么是债券型基金的杠杆比例', '什么是债券型基金的杠杆比例', '1', null, '1', '杠杆', '10020005');
INSERT INTO `robot_question` VALUES ('0000000200', '开支比率', '开支比率', '1', null, '1', '开支比率', '10020005');
INSERT INTO `robot_question` VALUES ('0000000201', '中港互认基金', '中港互认基金', '1', null, '1', '互认,基金', '10020005');
INSERT INTO `robot_question` VALUES ('0000000202', '什么是分位排名', '什么是分位排名', '1', null, '1', '分位,排名', '10020005');
INSERT INTO `robot_question` VALUES ('0000000203', '什么是基金场外转场内', '什么是基金场外转场内', '1', null, '1', '场外,转,场内', '10020005');
INSERT INTO `robot_question` VALUES ('0000000204', '什么是惩罚性赎回费', '什么是惩罚性赎回费', '1', null, '1', '惩罚性赎回', '10020005');
INSERT INTO `robot_question` VALUES ('0000000205', '什么是强制赎回', '什么是强制赎回', '1', null, '1', '强制赎回', '10020006');
INSERT INTO `robot_question` VALUES ('0000000206', '基金A类、B类、C类的区别', '基金A类、B类、C类的区别', '1', null, '1', '基金A类、B类、C类', '10020006');
INSERT INTO `robot_question` VALUES ('0000000207', '定开债基金是什么', '定开债基金是什么', '1', null, '1', '定开债', '10020006');
INSERT INTO `robot_question` VALUES ('0000000208', '定开债基金有哪些优势', '定开债基金有哪些优势', '1', null, '1', '定开债,基金,优势', '10020006');
INSERT INTO `robot_question` VALUES ('0000000209', '定开债基的特点', '定开债基的特点', '1', null, '1', '定开债,特点', '10020006');
INSERT INTO `robot_question` VALUES ('0000000210', '什么是养老目标基金？', '什么是养老目标基金？', '1', null, '1', '养老,基金', '10020006');
INSERT INTO `robot_question` VALUES ('0000000211', '什么是养老目标日期基金？', '什么是养老目标日期基金？', '1', null, '1', '养老,日期,基金', '10020006');
INSERT INTO `robot_question` VALUES ('0000000212', '什么是养老目标风险基金？', '什么是养老目标风险基金？', '1', null, '1', '养老,目标,风险,基金', '10020006');
INSERT INTO `robot_question` VALUES ('0000000213', '什么是个税递延？', '什么是个税递延？', '1', '', '1', '个税,递延', '10020006');
INSERT INTO `robot_question` VALUES ('0000000214', '养老账户如何进行资金领取及个税扣缴？', '养老账户如何进行资金领取及个税扣缴？', '1', null, '1', '养老,账户,领取,个税', '10020006');
INSERT INTO `robot_question` VALUES ('0000000215', '什么是S基金', '什么是S基金', '1', null, '1', 'S基金', '10020003');
