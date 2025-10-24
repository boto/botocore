import boto3

boto3.set_stream_logger('')


rds_client = boto3.client('rds-data')

sql = '''
select array[123::int4, null::int4, 456::int4];
'''

recs = rds_client.execute_statement(
    secretArn='arn:aws:secretsmanager:us-east-1:135633386280:secret:rds!cluster-9237ce19-931d-48a6-9130-c1f7e4930a27-ZLZKOT',
    resourceArn='arn:aws:rds:us-east-1:135633386280:cluster:data-api-test',
    database='postgres',
    sql=sql,
)

print(f'{recs}')


# TODO: Working below for comparison

# import boto3
# boto3.set_stream_logger('')
#
# rds_client = boto3.client('rds-data')
#
# sql = 'select array[123::int4, 789::int4, 456::int4];'
#
# recs = rds_client.execute_statement(
#     secretArn = 'arn:aws:secretsmanager:us-east-1:135633386280:secret:rds!cluster-9237ce19-931d-48a6-9130-c1f7e4930a27-ZLZKOT',
#     resourceArn = 'arn:aws:rds:us-east-1:135633386280:cluster:data-api-test',
#     database = 'postgres',
#     sql = sql
# )
#
# print(f'{recs}')
