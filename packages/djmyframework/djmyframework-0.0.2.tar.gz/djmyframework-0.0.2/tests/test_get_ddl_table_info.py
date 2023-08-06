# -*- coding: utf-8 -*-
# @Time    : 2021-02-25 11:21
# @Author  : xzr
# @File    : test_get_ddl_table_info
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :
from unittest import TestCase
from framework.utils import sql

class TestGet_ddl_table_info(TestCase):

    def test_get_ddl_table_info(self):
        sql_text='''-- https://ci.apache.org/projects/flink/flink-docs-release-1.12/zh/dev/table/sql/create.html
-- https://ci.apache.org/projects/flink/flink-docs-release-1.12/zh/dev/table/connectors/kafka.html
-- http://maxwells-daemon.io/dataformat/

DROP TABLE IF EXISTS base__maxwell_table;
CREATE TABLE base__maxwell_table (
  `database` STRING,
  `table` STRING ,
  `type` STRING,
   proctime AS PROCTIME() -- UTC 时间
) WITH (
  'connector' = 'kafka',  -- using kafka connector
  'topic' = '${marital=ylyh_cn,ylyh_cn|test_topic}',  -- kafka topic
  'properties.bootstrap.servers' = 'kafka1:9092,kafka2:9092,kafka3:9092',  -- kafka broker address
  'format' = 'json',  -- the data format is json
  'json.fail-on-missing-field' = 'false',
  'json.ignore-parse-errors' = 'true'
);



DROP TABLE IF EXISTS ods__log;
CREATE TABLE ods__log (
  `data` ROW<id BIGINT,server_id STRING,log_user STRING, f1 STRING,f2 STRING,log_time TIMESTAMP(3),log_channel STRING>, 
   `log_time` as IF(data.log_time is NULL,TO_TIMESTAMP('1970-01-01 00:00:00'),data.log_time),    --log_time 空的话使用 1970-01-01 00:00:00 代替,需要加时区
  `c1` as `data`.`f1`,
  `c2` as `data`.`f2`,
   WATERMARK FOR `log_time` AS TIMESTAMPADD(HOUR,-8,`log_time`) - INTERVAL '10' SECOND   -- log_time 空的话使用 1970-01-01 00:00:00 代替,需要加时区,
) WITH (
  'topic' = '${marital=ylyh_cn,ylyh_cn|test_topic}'  -- kafka topic
) LIKE base__maxwell_table;


DROP TABLE IF EXISTS ods__log_cn;
CREATE TABLE ods__log_cn
WITH (
  'topic' = 'ylyh_cn'  -- kafka topic
)
LIKE ods__log;

DROP TABLE IF EXISTS ods__log_test;
CREATE TABLE ods__log_test
WITH (
  'topic' = 'test_topic'  -- kafka topic
)
LIKE ods__log;


DROP TABLE IF EXISTS ods__pay_action;
CREATE TABLE ods__pay_action (
  `data` ROW(id BIGINT,server_id STRING,pay_user STRING, channel_key STRING,query_id STRING,post_time TIMESTAMP(3) , last_time TIMESTAMP(3),pay_status INT,pay_ip string,pay_type int,channel_id int,order_id string ,pay_amount double,post_amount double,pay_gold int ), 
   `old` ROW(pay_status INT),
   `log_time` as IF(data.post_time is NULL,TO_TIMESTAMP('1970-01-01 00:00:00'),data.post_time) , -- log_time 空的话使用 1970-01-01 00:00:00 代替,需要加时区,
  `pay_user` as `data`.`pay_user`,
  `channel_key` as `data`.`channel_key`,
  `server_id` as `data`.`server_id`,
  `pay_status` as COALESCE(`data`.`pay_status`,`old`.`pay_status`),
  `query_id` as `data`.`query_id`,
  `pay_amount` as `data`.`pay_amount`,
  `query_idpost_amount` as `data`.`post_amount`,
  `pay_gold` as `data`.`pay_gold`,
   WATERMARK FOR `log_time` AS TIMESTAMPADD(HOUR,-8,`log_time`) - INTERVAL '10' SECOND  -- 水印时间为event time并转为 utc
) WITH (
  'topic' = '${marital=ylyh_cn,ylyh_cn|test_topic}',  -- kafka topic
  'properties.group.id'='ods__pay_action'
) LIKE base__maxwell_table;


DROP TABLE IF EXISTS ods__player;
CREATE TABLE ods__player (
  `data` ROW(id BIGINT,
            player_id bigint,
            player_name string,
            user_type bigint,
            link_key string,
            create_time TIMESTAMP(3),
            login_time TIMESTAMP(3),
            last_time TIMESTAMP(3),
            last_ip string,
            last_key string,
            login_num bigint,
            vip_level bigint,
            status bigint,
            channel_id string,
            mobile_key string,
            other string,
            is_old bigint,
            os string,
            last_os string
            ), 
   `old` ROW(
            create_time TIMESTAMP(3),
            login_time TIMESTAMP(3),
            last_time TIMESTAMP(3)
            ),
   `create_time` as `data`.`create_time`,
   `login_time` as `data`.`login_time`,
   `last_time` as `data`.`last_time`,
   `log_time` as IF(data.last_time is NULL,TO_TIMESTAMP('1970-01-01 00:00:00'),data.last_time) , -- log_time 空的话使用 1970-01-01 00:00:00 代替,需要加时区,
   WATERMARK FOR `log_time` AS TIMESTAMPADD(HOUR,-8,`log_time`) - INTERVAL '10' SECOND  -- 水印时间为event time并转为 utc
) WITH (
  'topic' = '${marital=ylyh_cn,ylyh_cn|test_topic}',  -- kafka topic
  'properties.group.id'='ods__player'
) LIKE base__maxwell_table;'''
        table_infos =  sql.get_ddl_table_info(sql_text)
        self.assertTrue(table_infos.get('ods__log'))

