class rds:

    def __init__(self, rds_service):
        self.rds = rds_service

    def get_db_arn(self):
        response = self.rds.describe_db_instances()

        result = []
        arn = []
        for i in response['DBInstances']:
            arn.append(i['DBInstanceArn'])

        for j in arn:
            result.append(self.describe_rds(j))

        return result

    def describe_rds(self, db_arn):
        response = self.rds.describe_db_instances(
            Filters=[{
                'Name': 'db-instance-id',
                'Values': [db_arn]
            }]
        )


        db_instance = response['DBInstances'][0]

        arn = db_instance['DBInstanceIdentifier']
        db_name = db_instance['DBName']
        db_engine = db_instance['Engine']
        db_type = db_instance['DBInstanceClass']
        db_storage = db_instance['AllocatedStorage']
        db_id = db_instance['MasterUsername']
        db_pw = 'Manual needed'
        db_characterset = 'Manual needed'
        db_mulaz = db_instance['MultiAZ']
        db_public = db_instance['PubliclyAccessible']
        db_endpoint = db_instance['Endpoint']['Address']

        result = (arn, db_name, db_engine, db_type, db_storage, db_id, db_pw, db_characterset, db_mulaz, db_public, db_endpoint)

        return result
