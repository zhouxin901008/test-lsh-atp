#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,os
import unittest
import requests
import json
import random
import time

sys.path.append('/home/work/test-env/jenkins/workspace/test-lsh-atp')
from xlutils.copy import copy
from base.Basic import Basic
from base.DB import DB
from base.TestCase import TestCase
from base.SendMail import SendMail

#reload(sys)
#sys.setdefaultencoding('utf-8')

class TestAtp(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAtp(self):
        # 操作excel
        testCase = TestCase()
        excel = testCase.getAtpTestCase("atpcase.xls")
        sheet = excel.sheets()[0]
        nrows = sheet.nrows
        wb = copy(excel)
        ws = wb.get_sheet(0)
        amount = 0

        for i in range(1,nrows):
            basic = Basic()
            host = basic.getAtpHost()
            headers = eval(basic.getAtpHeaders())
            url = sheet.cell(i,4).value
            data = sheet.cell(i,5).value
            if "sequence" in data :
                data = json.loads(data)
                data['sequence'] = random.randint(100000000, 999999999)
                if sheet.cell(i,2).value.encode("utf-8")  == 'sequence已存在':
                    data['sequence'] = '450639911'
                elif sheet.cell(i,2).value.encode("utf-8")  == 'sequence为空':
                    data['sequence'] = ""
                elif sheet.cell(i,2).value.encode("utf-8")  == '扣减DC10':
                    sequence = data['sequence']
                    #print sequence
                elif sheet.cell(i,2).value.encode("utf-8")  == '正确的还原':
                    data['sequence'] = sequence
                    #print data['sequence']
                elif sheet.cell(i,2).value.encode("utf-8")  == '已经还原过':
                    data['sequence'] = sequence
                    #print data['sequence']
                elif sheet.cell(i, 2).value.encode("utf-8") == '含有hold_id的还原':
                    # 链接数据库
                    atp = DB()
                    sql = "select SEQUENCE_ID as sequence ,HOLD_NO as hold_id from `lsh-atp1`.`SKU_HOLD` where hold_end_time = 1500000000 and status = '2' and ZONE_CODE = 1000 ORDER BY id desc limit 1;"
                    data = atp.atpQuery(sql)
                    for row in data:
                        #print row
                        data = row
                    data['channel'] = 1
                    #cursor.close()
                    #print json.dumps(data)
                elif sheet.cell(i, 2).value.encode("utf-8") == 'hold_id为空':
                    # 链接数据库
                    atp = DB()
                    sql = "select SEQUENCE_ID as sequence from `lsh-atp1`.`SKU_HOLD` where hold_end_time = 1500000000 and status = '2' and ZONE_CODE = 1000 ORDER BY id desc limit 1;"
                    data = atp.atpQuery(sql)
                    #cursor.execute(sql)
                    #data = cursor.fetchall()
                    for row in data:
                        #print row
                        data = row
                    data['hold_id'] = ""
                    data['channel'] = 1
                    #cursor.close()
                    #print json.dumps(data)
                ws.write(i,5,json.dumps(data))
                result = requests.post(host + url,headers = headers,data = json.dumps(data))
            elif sheet.cell(i, 2).value.encode("utf-8") == '创建出货规则':
                data = json.loads(data)
                data['item_id'] = random.randint(100000, 999999)
                #print data['item_id']
                ws.write(i, 5, json.dumps(data))
                try:
                    result = requests.post(host + url, headers = headers, data = json.dumps(data))
                except Exception, e:
                    print Exception, ":", e
            else:
                try:
                    result = requests.post(host + url, headers = headers, data = data)
                #r = json.dumps(result.text)
                #print r
                except Exception, e:
                    print Exception, ":", e
            responseTime = (result.elapsed.microseconds) / 1000
            ws.write(i,13,responseTime)
            status = sheet.cell(i,11).value
            if result.json()['status'] == status :
                print "第%d条用例pass"%i
                ws.write(i,12,'pass')
                amount+=1
            else:
                print "第%d条用例failure" %i
                ws.write(i, 12, result.json()['status'])
                ws.write(i,10,result.text)
            resultTime = time.strftime('%Y-%m-%d_%H:%M:%S')

        a = amount/float(i)
        ws.write(i,15,"%.2f"%a)
        print "case通过率为%.2f"%a
        wb.save('./atpTestCase/atpTestResult_' + resultTime + '.xls')
        sd = SendMail()
        sd.mail(resultTime)


if __name__ ==  '__main__':
    unittest.main()

    """"
    suite = unittest.TestSuite()
    suite.addTest(atp1("TestAtp"))

    filename = "./atpTestReport.html"
    fp = file(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title="testing result", description="trying")
    runner.run(suite)
    fp.close()
    os.system(filename)
    """