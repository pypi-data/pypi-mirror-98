import ast
import json
import os
import unittest
from datetime import datetime
from decimal import Decimal

import boto3
from dotenv import load_dotenv

from data_api_mapper.appsync import AppsyncEvent, CamelSnakeConverter
from data_api_mapper.data_api import DataAPIClient, ParameterBuilder, GraphQLMapper, DictionaryMapper

load_dotenv()


def read_json_file(path):
    with open(path) as json_file:
        return json.load(json_file)


class TestDataAPI(unittest.TestCase):

    data_client = None

    @classmethod
    def setUpClass(cls):
        db_name = os.getenv('DB_NAME')
        db_cluster_arn = os.getenv('DB_CLUSTER_ARN')
        secret_arn = os.getenv('SECRET_ARN')
        rds_client = boto3.client('rds-data')
        data_client = DataAPIClient(rds_client, secret_arn, db_cluster_arn, db_name)
        initial_sql = """
            DROP TABLE IF EXISTS aurora_data_api_test;
            CREATE TABLE aurora_data_api_test (
                id SERIAL,
                a_name TEXT,
                doc JSONB DEFAULT '{}',
                num_numeric NUMERIC (10, 5) DEFAULT 0.0,
                num_float float,
                num_integer integer,
                ts TIMESTAMP WITH TIME ZONE,
                field_string_null TEXT NULL,
                field_long_null integer NULL,
                field_doc_null JSONB NULL,
                field_boolean BOOLEAN NULL,
                tz_notimezone TIMESTAMP
            );
            INSERT INTO aurora_data_api_test (a_name, doc, num_numeric, num_float, num_integer, ts, tz_notimezone)
            VALUES ('first row', '{"string_vale": "string1", "int_value": 1, "float_value": 1.11}', 1.12345, 1.11, 1, '1976-11-02 08:45:00 UTC', '2021-03-03 15:51:48.082288');
            VALUES ('second row', '{"string_vale": "string2", "int_value": 2, "float_value": 2.22}', 2.22, 2.22, 2, '1976-11-02 08:45:00 UTC', '2021-03-03 15:51:48.082288');
        """
        data_client.execute(sql=initial_sql, wrap_result=False)
        cls.data_client = data_client

    def test_types(self):
        parameters = ParameterBuilder().add("id", 1).build()
        result = self.data_client.execute("select * from aurora_data_api_test where id =:id", parameters)
        row = GraphQLMapper(result.metadata).map(result.records)[0]
        self.assertEqual(1, row['id'])
        self.assertEqual('2021-03-03T15:51:48.082288Z', row['tz_notimezone'])
        self.assertEqual('first row', row['a_name'])
        doc = row['doc']
        self.assertEqual('string1', doc['string_vale'])
        self.assertEqual(1, doc['int_value'])
        self.assertEqual(1.11, doc['float_value'])
        self.assertEqual(1.12345, row['num_numeric'])
        self.assertEqual(1.11, row['num_float'])
        self.assertEqual(1, row['num_integer'])

    def test_data_api_types(self):
        sql = "INSERT INTO aurora_data_api_test (a_name, doc, num_numeric, num_float, num_integer, ts, tz_notimezone, field_string_null, field_boolean, field_long_null, field_doc_null) values (:name, :doc, :num_float, 1.11,:num_integer, '1976-11-02 08:45:00 UTC', '2021-03-03 15:51:48.082288', :field_string_null, :field_boolean, :field_long_null, :field_json_null) RETURNING id"
        parameters = ParameterBuilder()\
            .add("name", 'prueba')\
            .add('field_string_null', None)\
            .add('doc', {'key':'as'})\
            .add('num_integer', 1) \
            .add('num_float', 1.123) \
            .add('field_boolean', True) \
            .add('field_long_null', None) \
            .add('field_json_null', None)\
            .build()
        result = self.data_client.execute(sql, parameters)
        result_map = GraphQLMapper(result.metadata).map(result.records)
        parameters = ParameterBuilder().add("id", result_map[0]['id']).build()
        result = self.data_client.execute("select * from aurora_data_api_test where id =:id", parameters)
        row = GraphQLMapper(result.metadata).map(result.records)[0]
        self.assertEqual('prueba', row['a_name'])
        self.assertEqual({'key':'as'}, row['doc'])
        self.assertEqual(1, row['num_integer'])
        self.assertEqual(True, row['field_boolean'])
        self.assertEqual(None, row['field_string_null'])
        self.assertEqual(None, row['field_long_null'])
        self.assertEqual(None, row['field_doc_null'])


    def test_transaction(self):
        transaction = self.data_client.begin_transaction()
        transaction.execute('''
            INSERT INTO aurora_data_api_test (id, a_name, doc, num_numeric, num_float, num_integer, ts, tz_notimezone) 
            VALUES (3, 'first row', '{"string_vale": "string1", "int_value": 1, "float_value": 1.11}', 1.12345, 1.11, 1, '1976-11-02 08:45:00 UTC', '2021-03-03 15:51:48.082288');
        ''')
        before_commit = self.data_client.execute("select * from aurora_data_api_test where id = 3")
        self.assertEqual(0, len(before_commit.records))
        transaction.commit()
        after_commit = self.data_client.execute("select * from aurora_data_api_test where id = 3")
        self.assertEqual(1, len(after_commit.records))


    @classmethod
    def tearDownClass(cls):
        cls.data_client.execute('DROP TABLE IF EXISTS aurora_data_api_test', wrap_result=False)


class TestAppSynEvent(unittest.TestCase):
    def test_fields(self):
        event = AppsyncEvent(read_json_file('query.json'))
        self.assertEqual("Hola Mundo", event.name)
        self.assertEqual("holamundo@email.com", event.email)
        self.assertEqual("4169f39a-db3a-4058-a907-3aa6684de0b2", event.username)


class TestAppSync(unittest.TestCase):
    def test_not_convert_typename(self):
        event = [{'prueba_campo': '2021-03-03 15:51:48.082288', '__typename': 'TYPENAME', 'id_ok': 9771}]
        result = CamelSnakeConverter.dict_to_camel(event)
        self.assertEqual("TYPENAME", result[0]['__typename'])
        self.assertEqual("2021-03-03 15:51:48.082288", result[0]['pruebaCampo'])
        self.assertEqual(9771, result[0]['idOk'])


class TestParameterBuilder(unittest.TestCase):
    def test_parameter_builder(self):
        self.assertEqual('dast', ParameterBuilder().add('string', 'dast').build()[0]['value']['stringValue'])
        self.assertEqual(1, ParameterBuilder().add('long', 1).build()[0]['value']['longValue'])
        self.assertEqual(1.123, ParameterBuilder().add('double', 1.123).build()[0]['value']['doubleValue'])
        self.assertEqual(False, ParameterBuilder().add('boolean', False).build()[0]['value']['booleanValue'])
        parameter_json = ParameterBuilder().add('json', {'key':'as'}).build()[0]
        self.assertEqual('JSON', parameter_json['typeHint'])
        self.assertEqual({'key':'as'}, ast.literal_eval(parameter_json['value']['stringValue']))
        date_object = ParameterBuilder().add('date', datetime(2017, 6, 11, 10, 20, 30).date()).build()[0]
        self.assertEqual('DATE', date_object['typeHint'])
        self.assertEqual('2017-06-11', date_object['value']['stringValue'])
        datetime_object = ParameterBuilder().add('datetime', datetime(2017, 6, 11, 10, 20, 30, 100)).build()[0]
        self.assertEqual('TIMESTAMP', datetime_object['typeHint'])
        self.assertEqual('2017-06-11 10:20:30.000100', datetime_object['value']['stringValue'])
        decimal = ParameterBuilder().add('decimal', Decimal(1.123412123123213035569278872571885585784912109375)).build()[0]
        self.assertEqual('DECIMAL', decimal['typeHint'])
        self.assertEqual('1.123412123123213035569278872571885585784912109375', decimal['value']['stringValue'])

    def test_parameter_builder_with_exception_by_none(self):
        with self.assertRaises(Exception) as context:
            ParameterBuilder().add('string', None).build()[0]['value']['stringValue']

        self.assertEqual('The data type of the value does not match against any of the expected', str(context.exception))

    def test_parameter_builder_with_null(self):
        self.assertEqual('dast', ParameterBuilder().add_or_null('string', 'dast').build()[0]['value']['stringValue'])
        self.assertEqual(1, ParameterBuilder().add_or_null('long', 1).build()[0]['value']['longValue'])
        self.assertEqual(1.123, ParameterBuilder().add_or_null('double', 1.123).build()[0]['value']['doubleValue'])
        self.assertEqual(False, ParameterBuilder().add_or_null('boolean', False).build()[0]['value']['booleanValue'])
        parameter_json = ParameterBuilder().add_or_null('json', {'key':'as'}).build()[0]
        self.assertEqual('JSON', parameter_json['typeHint'])
        self.assertEqual({'key':'as'}, ast.literal_eval(parameter_json['value']['stringValue']))
        date_object = ParameterBuilder().add_or_null('date', datetime(2017, 6, 11, 10, 20, 30).date()).build()[0]
        self.assertEqual('DATE', date_object['typeHint'])
        self.assertEqual('2017-06-11', date_object['value']['stringValue'])
        datetime_object = ParameterBuilder().add_or_null('datetime', datetime(2017, 6, 11, 10, 20, 30)).build()[0]
        self.assertEqual('TIMESTAMP', datetime_object['typeHint'])
        self.assertEqual('2017-06-11 10:20:30', datetime_object['value']['stringValue'])
        decimal = ParameterBuilder().add_or_null('decimal', Decimal(1.123412123123213035569278872571885585784912109375)).build()[0]
        self.assertEqual('DECIMAL', decimal['typeHint'])
        self.assertEqual('1.123412123123213035569278872571885585784912109375', decimal['value']['stringValue'])
        self.assertEqual(True, ParameterBuilder().add_or_null('string', None).build()[0]['value']['isNull'])

    def test_add_dictionary(self):
        a_dict = {
            'a_string': 'hello',
            'an_int': 4
        }
        params = ParameterBuilder().add_dictionary(a_dict).build()
        self.assertEqual('a_string', params[0]['name'])
        self.assertEqual('hello', params[0]['value']['stringValue'])
        self.assertEqual('an_int', params[1]['name'])
        self.assertEqual(4, params[1]['value']['longValue'])

if __name__ == '__main__':
    unittest.main()
