# PyAlgoTrade
#
# Copyright 2011-2018 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: lw
"""


from pyalgotrade import commonHelpBylw






from apscheduler.schedulers.background import BackgroundScheduler

from pyalgotrade import config



def initABscheduler(host,tablename):
    sched = BackgroundScheduler()


    # # 使用sqlalchemy作业存储器
    url = 'mysql+pymysql://admin:admin@'+host+':3306/tradeprojectdata_lw?charset=utf8'


    sched.add_jobstore('sqlalchemy', url=url,tablename=tablename,engine_options={'pool_recycle':1800,'pool_pre_ping':True})
    sched.start()
    return  sched



class orderControlObj:
    """lw李文实现的，用来封下单的一些控制动作的，基于掘金的下单函数的.

    """

    def __init__(self,aNewTradeCalendar,tablename,host):

        self.symTradeTime=config.tradeTimeDict
        self.sched=initABscheduler(host,tablename)

        self.aNewTradeCalendar=aNewTradeCalendar

    #funargs是tuple 如果只有一个参数，那么要这种形式(1,)即不要掉了逗号
    def controlByOrderTime(self,datetimeStr,symbol):
        underlygingSym=commonHelpBylw.getMainContinContract(symbol)

        dateList=self.symTradeTime[underlygingSym]


        listLength=len(dateList)


        date_=datetimeStr[0:10]
        time_=datetimeStr[11:]
        for indx_ in range(listLength):
            currDateRange=dateList[indx_]

            if time_==currDateRange[1]:

                nextInx_=(indx_+1)%listLength
                nextTime_=dateList[nextInx_][0]

                if nextTime_<time_:  #说明到了下一日了

                    nextTDate=self.aNewTradeCalendar.tradingDaysOffset(date_,1)
                    nextDatetime=nextTDate+' '+nextTime_


                if nextTime_>time_:

                    nextDatetime = date_ + ' ' + nextTime_

                # self.sched.add_job(fun, 'date', run_date=nextDatetime,misfire_grace_time=60, args=funargs, kwargs=funkargs,
                #                   id=symbol + '-' + nextDatetime+'-'+action)
                return True,nextDatetime
        return False,0



    def addDelayOrderTask(self,nextDatetime,action,fun,funargs=None,funkargs=None):
        symbol=funkargs.get('symbol')
        self.sched.add_job(fun, 'date', run_date=nextDatetime,misfire_grace_time=180, args=funargs, kwargs=funkargs,
                          id=symbol + '-' + nextDatetime+'-'+action)
