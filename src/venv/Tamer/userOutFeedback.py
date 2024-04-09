# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2022/7/16 21:56
# @author   :wucy
# @function : pywebio
import requests, json
import json
from pywebio.input import input, TEXT, FLOAT, input_update, input_control, textarea
from pywebio.output import put_text, put_tabs, put_table, put_file, put_code
from pywebio import start_server


def _get_user_feedback(sen_add,tag,sen_answer,user,dim):
    try:
        sent_intersection = list(set(list(ssen_adden_1)).intersection(set(list(sen_answer))))
        sent_union = list(set(list(sen_add)).union(set(list(sen_answer))))
        score_jaccard = round(float(len(sent_intersection) / len(sent_union)), 6)
        github_url = "https://XXX"
        data = json.dumps({'name':'test', 'description':'some test repo'}) 
        r = requests.post(github_url, data, auth=('user', user,sen_add,tag,sen_answer,dim))
        score_feedback=json.loads(r)
        return score_feedback["score"];
    except:
        score_jaccard = 0
        res = {"result": 'call failure'}
        data = {"code": 200, "data": res, "message": "failure"}
        print("=============failure=============")
    # put_text(data)
    return 0;


if __name__ == '__main__':
    start_server(_get_user_feedback, port=8832)






