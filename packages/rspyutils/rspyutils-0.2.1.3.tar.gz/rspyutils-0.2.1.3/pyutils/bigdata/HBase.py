# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on MAY 21, 2018
@author: zlh
"""
# 以下两个模块可以通过 pip install thrift 安装获得
import pprint

from sqlalchemy.dialects.mysql.base import colspecs
from sqlalchemy.dialects.postgresql.base import colspecs
from thrift.protocol import TBinaryProtocol
from thrift.transport import THttpClient

# 下面的模块通过 thrift --gen py hbase.thrift 来生成
from pyutils.bigdata.hbases.thrift2.hbase import THBaseService
from pyutils.bigdata.hbases.thrift2.hbase.ttypes import (TColumn, TColumnFamilyDescriptor,
                                                         TColumnValue, TGet,
                                                         TNamespaceDescriptor, TPut, TScan,
                                                         TTableDescriptor, TTableName)

# # 下面的模块通过 thrift --gen py hbase.thrift 来生成
# from hbases.thrift2.hbase import THBaseService
# from hbases.thrift2.hbase.ttypes import (TColumn, TColumnFamilyDescriptor,
#                                                          TColumnValue, TGet,
#                                                          TNamespaceDescriptor, TPut, TScan,
#                                                          TTableDescriptor, TTableName)


class HBaseCli(object):

    def __init__(self, url, headers=None):
        """
        create connection to hive server2
        headers = {}
        # 用户名
        headers["ACCESSKEYID"] = "root";
        # 密码
        headers["ACCESSSIGNATURE"] = "root"
        """
        try:
            # 连接地址
            # url = "http://ld-bp17y8n3j6f45p944-proxy-hbaseue.hbaseue.rds.aliyuncs.com:30020"
            self.transport = THttpClient.THttpClient(url)
            self.transport.setCustomHeaders(headers)
            protocol = TBinaryProtocol.TBinaryProtocolAccelerated(
                self.transport)
            self.client = THBaseService.Client(protocol)
        except Exception as e:
            raise e

    def createNamespace(self, ns):
        """ 创建命名空间

        Args:
            ns (string): 命名空间名称
        """
        self.transport.open()
        self.client.createNamespace(TNamespaceDescriptor(name=ns))
        self.transport.close()

    def checkNamespace(self, ns):
        """ 检测是否创建了命名空间

        Args:
            ns (string): 命名空间名称

        Returns:
            bool: 是否存在
        """
        self.transport.open()
        Descriptors = self.client.listNamespaceDescriptors()
        self.transport.close()

        for Descriptor in Descriptors:
            if Descriptor.name == ns:
                return True

        return False

    def createTable(self, ns, qualifier, family):
        """ 创建表，必须要先创建namespace

            最好手动创建表：create 'namespace:tablename' , {NAME => 'info', VERSIONS => 1}
            VERSIONS: 控制数据存储版本个数

        Args:
            ns (string): 命名空间名称
            qualifier (string): 表名
            family (string): 列簇名
        """
        self.transport.open()
        tableName = TTableName(ns=ns, qualifier=qualifier)
        self.client.createTable(TTableDescriptor(tableName=tableName, columns=[
            TColumnFamilyDescriptor(name=family)
        ]), None)
        self.transport.close()

    def checkTable(self, ns, qualifier):
        self.transport.open()
        tableName = TTableName(ns=ns, qualifier=qualifier)
        flg = self.client.tableExists(tableName)
        self.transport.close()

        return flg

    def single_insert(self, ns, tableName, family, **kwargs):
        """ 单行插入

        Args:
            ns ([type]): [description]
            tableName ([type]): [description]
            family ([type]): [description]
            kwargs : {"row_key":row_key,"data":{"k1":"v1","k2":"v2","k3":"v3"}}
        Raises:
            Exception: [description]

        Returns:
            [type]: [description]
        """
        self.transport.open()
        tableInbytes = "{ns}:{tableName}".format(
            ns=ns, tableName=tableName).encode("utf8")
        row_key = kwargs.get("row_key", "")
        if not row_key:
            raise Exception("row_key not exit exception")
        data = kwargs.get("data", {})
        self.client.put(table=tableInbytes, tput=TPut(row="{}".format(row_key).encode("utf8"), columnValues=[
            TColumnValue(family="{}".format(family).encode("utf8"), qualifier="{}".format(k).encode("utf8"),
                         value="{}".format(v).encode("utf8")) for k, v in data.items()]))

        self.transport.close()

    def bulk_insert(self, ns, tableName, family, kwargs_list):
        """ 批量插入

        Args:
            ns ([type]): [description]
            qualifier ([type]): [description]
            family ([type]): [description]
            kwargs_list:[{"row_key":row_key,"data":{"k1":"v1","k2":"v2","k3":"v3"}}]
        """
        self.transport.open()
        tableInbytes = "{ns}:{tableName}".format(
            ns=ns, tableName=tableName).encode("utf8")
        puts = [TPut(row="{}".format(v.get("row_key")).encode("utf-8"), columnValues=[
            TColumnValue(family="{}".format(family).encode("utf-8"), qualifier="{}".format(k).encode("utf-8"),
                         value="{}".format(v2).encode("utf-8")) for k, v2 in v.get('data', {}).items()]) for v in kwargs_list]
        self.client.putMultiple(table=tableInbytes, tputs=puts)
        self.transport.close()

    @staticmethod
    def _decode_from_result(result):
        def get_key(family, qualifier):
            return "{}:{}".format(family, qualifier)

        return {get_key(x.family.decode('utf-8'), x.qualifier.decode('utf-8')): x.value.decode('utf-8') for x in result}

    @staticmethod
    def _decode_from_results(result):
        def get_key(family, qualifier):
            return "{}:{}".format(family, qualifier)

        return [{get_key(xx.family.decode('utf-8'), xx.qualifier.decode('utf-8')): xx.value.decode('utf-8') for xx in
                 x.columnValues} for x in result]

    def get(self, ns, tableName, row):
        """ 单行查询数据

        Args:
            ns ([type]): [description]
            tableName ([type]): [description]
            row ([type]): [description]

        Returns:
            [type]: [description]
        """
        self.transport.open()
        tableInbytes = "{ns}:{tableName}".format(
            ns=ns, tableName=tableName).encode("utf8")
        result = self.client.get(tableInbytes, TGet(row=row.encode("utf8")))
        self.transport.close()
        return self._decode_from_result(result.columnValues)

    def getCols(self, ns, tableName, row, cols):
        """ 单行查询数据, 指定列名

        Args:
            ns ([type]): [description]
            tableName ([type]): [description]
            row ([type]): [description]
            col ([type]): [description]

        Returns:
            [type]: [description]
        """
        self.transport.open()
        tableInbytes = "{ns}:{tableName}".format(
            ns=ns, tableName=tableName).encode("utf8")
        result = self.client.get(tableInbytes, TGet(
            row=row.encode("utf8"), columns=cols))
        self.transport.close()
        return self._decode_from_result(result.columnValues)

    def getMultiple(self, ns, tableName, rows):
        """ 批量单行查询

        Args:
            ns ([type]): [description]
            tableName ([type]): [description]
            rows ([type]): [description]

        Returns:
            [type]: [description]
        """
        self.transport.open()
        tableInbytes = "{ns}:{tableName}".format(
            ns=ns, tableName=tableName).encode("utf8")
        gets = [TGet(row=row.encode("utf8")) for row in rows]
        results = self.client.getMultiple(tableInbytes, gets)
        self.transport.close()
        return self._decode_from_results(results)

    def getMultipleCols(self, ns, tableName, rows, cols):
        """ 批量单行查询, 指定列名

        Args:
            ns ([type]): [description]
            tableName ([type]): [description]
            rows ([type]): [description]
            col ([type]): [description]

        Returns:
            [type]: [description]
        """
        self.transport.open()
        tableInbytes = "{ns}:{tableName}".format(
            ns=ns, tableName=tableName).encode("utf8")
        gets = [TGet(row=row.encode("utf8"), columns=cols) for row in rows]
        results = self.client.getMultiple(tableInbytes, gets)
        self.transport.close()
        return self._decode_from_results(results)

    def scan(self, ns, tableName, family=None, cols=None, startRow=None, stopRow=None, filterString=None, caching=20, limit=None):
        """ 扫描表

        Args:
            ns ([type]): [description]
            tableName ([type]): [description]
            family ([type], optional): [description]. Defaults to None.
            cols ([type], optional): [description]. Defaults to None.
            startRow ([type], optional): [description]. Defaults to None.
            stopRow ([type], optional): [description]. Defaults to None.
            caching (int, optional): [description]. Defaults to 20.
            limit ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        self.transport.open()
        tableInbytes = "{ns}:{tableName}".format(
            ns=ns, tableName=tableName).encode("utf8")

        scan_dict = {}
        if family is not None and cols is not None:
            columnsInbytes = []
            for columnName in cols:
                columnsInbytes.append(TColumn(family=family.encode(
                    "utf-8"), qualifier=columnName.encode("utf-8")))
            scan_dict["columns"] = columnsInbytes

        if startRow is not None:
            startRow = startRow.encode("utf8")
            scan_dict["startRow"] = startRow

        if stopRow is not None:
            stopRow = stopRow.encode("utf8")
            scan_dict["stopRow"] = stopRow

        if filterString is not None:
            filterString = filterString.encode("utf8")
            scan_dict["filterString"] = filterString

        scan = TScan(**scan_dict)

        # 扫描的结果
        results = []

        # 此函数可以找到比当前row大的最小row，方法是在当前row后加入一个0x00的byte
        # 从比当前row大的最小row开始scan，可以保证中间不会漏扫描数据
        def createClosestRowAfter(row):
            array = bytearray(row)
            array.append(0x00)
            return bytes(array)

        while True:
            lastResult = None
            # getScannerResults会自动完成open,close 等scanner操作，HBase增强版必须使用此方法进行范围扫描
            currentResults = self.client.getScannerResults(
                tableInbytes, scan, caching)
            for result in currentResults:
                results.append(result)
                lastResult = result
            # 如果一行都没有扫描出来，说明扫描已经结束，我们已经获得startRow和stopRow之间所有的result
            if lastResult is None:
                break
            # 如果此次扫描是有结果的，我们必须构造一个比当前最后一个result的行大的最小row，继续进行扫描，以便返回所有结果
            else:
                nextStartRow = createClosestRowAfter(lastResult.row)
                scan_dict["startRow"] = nextStartRow
                scan = TScan(**scan_dict)
                # scan = TScan(startRow=nextStartRow, columns=columnsInbytes)

            if limit is not None:
                if len(results) >= limit:
                    break

        self.transport.close()
        return results


if __name__ == "__main__":
    client = HBaseCli(url="http://ld-bp17y8n3j6f45p944-proxy-hbaseue.hbaseue.rds.aliyuncs.com:9190",
                      headers={"ACCESSKEYID": "root", "ACCESSSIGNATURE": "root"})

    # 检测和创建命名空间
    namespace = "recommend_xxxx_test"
    if client.checkNamespace(namespace) is False:
        print("命名空间未创建，创建...")
        client.createNamespace(namespace)
    else:
        print("已创建命名空间:", namespace)

    # 检测和创建表名
    tableName = "xxxx"
    family = "info"
    if client.checkTable(ns=namespace, qualifier=tableName) is False:
        print("表未创建，创建...")
        client.createTable(ns=namespace, qualifier=tableName, family=family)
    else:
        print("已创建表:", namespace)

    # 数据插入:插入单条数据
    kwargs = {
        "row_key": "2",
        "data": {
            "type": 2,
            "page_id": "-Elías-PCB-161219993935151",
            "home_id": "161219993935151",
            "obj_name": "(<-) Elías - PCB",
            "img_url": "http://spider-silicon.3935151.jpg",
            "c_url": "https://www.facebook.com/-Elías-PCB-161219993935151/?ref=br_rs",
            "company_url": "http://www.eliaspcb.com"
        }
    }
    client.single_insert(ns=namespace, tableName=tableName,
                         family=family, **kwargs)

    # 数据插入:批量插入数据
    kwargs_list = [
        {
            "row_key": "3",
            "data": {
                "type": 2,
                "page_id": "-Hair-Accessories--416385828419351",
                "home_id": "416385828419351",
                "obj_name": "~{ Hair Accessories }~",
                "img_url": "http://spider-ccessories--416385828419351.jpg",
                "c_url": "https://www.facebook.com/-Hair-Accessories--416385828419351/?ref=br_rs",
                "company_url": ""
            }
        },
        {
            "row_key": "4",
            "data": {
                "type": 2,
                "page_id": "-Joc-Lyn-Bicycle-Parts--386837101395047",
                "home_id": "386837101395047",
                "obj_name": "-Joc-Lyn-Bicycle-Parts",
                "img_url": "",
                "c_url": "https://www.facebook.com/-Joc-Lyn-Bicycle-Parts--386837101395047/?ref=br_rs",
                "company_url": ""
            }
        }
    ]
    client.bulk_insert(ns=namespace, tableName=tableName,
                       family=family, kwargs_list=kwargs_list)

    # 获取单个数据或指定列名
    print(client.get(ns=namespace, tableName=tableName, row="2"))
    print(client.getCols(ns=namespace, tableName=tableName, row="3",
                         cols=[TColumn(family="info", qualifier="home_id"),
                               TColumn(family="info", qualifier="img_url")]))
    print("#############")

    # 获取多个数据或指定列名
    print(client.getMultiple(ns=namespace,
                             tableName=tableName, rows=["2", "4"]))
    print(client.getMultipleCols(ns=namespace, tableName=tableName, rows=["2", "4"],
                                 cols=[TColumn(family="info", qualifier="obj_name"),
                                       TColumn(family="info", qualifier="page_id")]))

    print("#############")

    result = client.scan(ns=namespace, tableName=tableName,
                         limit=110, caching=11)   # limit为caching的倍数
    print(len(result))
    print(result)

    result = client.scan(ns=namespace, tableName=tableName, family="info", cols=["home_id", "c_url"],
                         limit=110, caching=11)   # limit为caching的倍数
    print(len(result))
    print(result)

    for rowInfo in result:
        print("+++++")
        print(rowInfo)
        print("ROW_KEY:", rowInfo.row)
        print(rowInfo.columnValues)
        for columnValue in rowInfo.columnValues:
            print(columnValue.qualifier, ":", columnValue.value)
            print(columnValue.qualifier.decode("utf-8"),
                  ":", columnValue.value.decode("utf-8"))

    print("555555555555555")
    result = client.scan(ns=namespace, tableName=tableName, family="info", cols=["home_id", "c_url"],
                         filterString="SingleColumnValueFilter('info','home_id',=,'binary:386837101395047')",
                         limit=110, caching=11)   # limit为caching的倍数
    print(len(result))
    print(result)
