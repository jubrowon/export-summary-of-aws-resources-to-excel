import boto3
import time, datetime


def describe_logs_files(rds):
    d_now = datetime.datetime.now()
    d_yesterday = d_now.replace(day=d_now.day-1)
    d_to_posix = int(time.mktime(d_yesterday.timetuple()))

    response = rds.describe_db_log_files(
        DBInstanceIdentifier='mz-test-ora',  # push-oracle-instance
        FileLastWritten=d_to_posix

    )

    return response['DescribeDBLogFiles']  # return list type

def download_logs_file(rds, log_file):
    token = '0'
    response = rds.download_db_log_file_portion(
        DBInstanceIdentifier='mz-test-ora',
        LogFileName=log_file,
        Marker=token
    )

    log_files_data = response['LogFileData']
    while response['AdditionalDataPending']:
        token = response['Marker']
        log_files_data += response['LogFileData']

        response = rds.download_db_log_file_portion(
            DBInstanceIdentifier='mz-test-ora',
            LogFileName=log_file,
            Marker=token
        )
    result_log_file = str.encode(log_files_data)
    return log_file, result_log_file


def lambda_handler(event, context):
    print('Hello')

    rds = boto3.client('rds', region_name='ap-south-1')
    s3 = boto3.client('s3', region_name='ap-south-1')
    dnow = datetime.datetime.now()
    dstr = dnow.strftime('%Y-%m-%d %H:%M:%S')
    print(describe_logs_files(rds))

    log_file_list = describe_logs_files(rds)
    logfilename = None
    downloads = None

    for i in log_file_list:
        logfilename, downloads = download_logs_file(rds, i['LogFileName'])
        s3.put_object(Bucket='logfiledata-test-juwon', Key='AWSRdsLogs/{}/'.format(dstr)+logfilename, Body=downloads)


if __name__ == '__main__':
    event, context = [], []
    lambda_handler(event, context)