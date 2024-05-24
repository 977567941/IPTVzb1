#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools
import db
import time
import re
import os

class Iptv (object):

    def __init__ (self) :
        self.T = tools.Tools()
        self.DB = db.DataBase()

    def run(self) :
        self.T.logger("开始抓取", True)

        self.DB.chkTable()

        Base = base.Source()
        Base.getSource()

        Dotpy = dotpy.Source()
        Dotpy.getSource()

        listB = listb.Source()
        listB.getSource()

        self.outPut()
        self.outJson()

        self.T.logger("抓取完成")

    def outPut (self) :
        self.T.logger("正在生成m3u8文件")

        sql = """SELECT * FROM
            (SELECT * FROM %s WHERE online = 1 ORDER BY delay DESC) AS delay
            GROUP BY LOWER(delay.title)
            HAVING delay.title != '' and delay.title != 'CCTV-' AND delay.delay < 500
            ORDER BY level ASC, length(title) ASC, title ASC
            """ % (self.DB.table)
        result = self.DB.query(sql)

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)).replace('python', 'http'), 'tv.m3u'), 'w') as f:
            f.write("#EXTM3U\n")
            for item in result :
                className = '其他频道'
                if item[4] == 1 :
                    className = '中央频道'
                elif item[4] == 2 :
                    className = '地方频道'
                elif item[4] == 3 :
                    className = '地方频道'
                elif item[4] == 7 :
                    className = '广播频道'
                else :
                    className = '其他频道'

                f.write("#EXTINF:-1, group-title=\"%s\", %s\n" % (className, item[1]))
                f.write("%s\n" % (item[3]))



if __name__ == '__main__':
    obj = Iptv()
    obj.run()





