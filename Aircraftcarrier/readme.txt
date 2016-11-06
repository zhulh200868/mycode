"""
jid=20161106175058618648
mysql> select * from t_exec_mapping where jid = '20161106175058618648';
+----------------------+-------------------------------------------------------------+---------------------------+------+------------------------+
| jid                  | ip_list                                                     | command                   | no   | task_id                |
+----------------------+-------------------------------------------------------------+---------------------------+------+------------------------+
| 20161106175058618648 | 172.16.167.106,172.16.167.113,172.16.167.111,172.16.167.126 | hadoop_util.refreshfsnode |    1 | 14781429778088199_10_1 |
+----------------------+-------------------------------------------------------------+---------------------------+------+------------------------+
1 row in set (0.00 sec)

mysql> select * from t_exec_jid_detail where jid = '20161106175058618648';
+-------+----------------------+----------------+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------+
| id    | jid                  | ip             | result | detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | donetime            |
+-------+----------------------+----------------+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------+
| 10430 | 20161106175058618648 | 172.16.167.106 | true   | Refresh nodes successful for BJYZ-Aircraftcarrier-167106.hadoop.jd.local/172.16.167.106:8020
Refresh nodes successful for BJYF-Aircraftcarrier-167113.hadoop.jd.local/172.16.167.113:8020
[2016-11-06T17:51:00.246+08:00] [INFO] security.whitelist.WhiteListConfigConstant.refreshDataNode(WhiteListRpcClient.java 591) [main] : BJYZ-Aircraftcarrier-167106.hadoop.jd.local White List Service is Closed
[2016-11-06T17:51:00.379+08:00] [INFO] security.whitelist.WhiteListConfigConstant.refreshDataNode(WhiteListRpcClient.java 591) [main] : BJYF-Aircraftcarrier-167113.hadoop.jd.local White List Service is Closed      | 2016-11-06 17:51:06 |
| 10432 | 20161106175058618648 | 172.16.167.111 | true   | Refresh nodes successful for BJHC4-Aircraftcarrier-167126.hadoop.jd.local/172.16.167.126:8020
Refresh nodes successful for BJHC4-Aircraftcarrier-167111.hadoop.jd.local/172.16.167.111:8020
[2016-11-06T17:51:00.265+08:00] [INFO] security.whitelist.WhiteListConfigConstant.refreshDataNode(WhiteListRpcClient.java 591) [main] : BJHC4-Aircraftcarrier-167111.hadoop.jd.local White List Service is Closed
[2016-11-06T17:51:00.399+08:00] [INFO] security.whitelist.WhiteListConfigConstant.refreshDataNode(WhiteListRpcClient.java 591) [main] : BJHC4-Aircraftcarrier-167126.hadoop.jd.local White List Service is Closed  | 2016-11-06 17:51:06 |
| 10433 | 20161106175058618648 | 172.16.167.113 | true   | Refresh nodes successful for BJYZ-Aircraftcarrier-167106.hadoop.jd.local/172.16.167.106:8020
Refresh nodes successful for BJYF-Aircraftcarrier-167113.hadoop.jd.local/172.16.167.113:8020
[2016-11-06T17:51:00.211+08:00] [INFO] security.whitelist.WhiteListConfigConstant.refreshDataNode(WhiteListRpcClient.java 591) [main] : BJYF-Aircraftcarrier-167113.hadoop.jd.local White List Service is Closed
[2016-11-06T17:51:00.343+08:00] [INFO] security.whitelist.WhiteListConfigConstant.refreshDataNode(WhiteListRpcClient.java 591) [main] : BJYZ-Aircraftcarrier-167106.hadoop.jd.local White List Service is Closed      | 2016-11-06 17:51:06 |
| 10431 | 20161106175058618648 | 172.16.167.126 | true   | Refresh nodes successful for BJHC4-Aircraftcarrier-167126.hadoop.jd.local/172.16.167.126:8020
Refresh nodes successful for BJHC4-Aircraftcarrier-167111.hadoop.jd.local/172.16.167.111:8020
[2016-11-06T17:51:00.259+08:00] [INFO] security.whitelist.WhiteListConfigConstant.refreshDataNode(WhiteListRpcClient.java 591) [main] : BJHC4-Aircraftcarrier-167126.hadoop.jd.local White List Service is Closed
[2016-11-06T17:51:00.392+08:00] [INFO] security.whitelist.WhiteListConfigConstant.refreshDataNode(WhiteListRpcClient.java 591) [main] : BJHC4-Aircraftcarrier-167111.hadoop.jd.local White List Service is Closed  | 2016-11-06 17:51:06 |
+-------+----------------------+----------------+--------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------+
4 rows in set (0.00 sec)

mysql> select * from t_exec_log where task_id = '14781429778088199_10_1';
+------+------------------------+
| id   | task_id                |
+------+------------------------+
| 2044 | 14781429778088199_10_1 |
+------+------------------------+
1 row in set (0.00 sec)

mysql> select * from t_exec_error_log where task_id = '14781429778088199_10_1';
Empty set (0.01 sec)
"""