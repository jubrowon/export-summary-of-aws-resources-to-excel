class subnet:
    def __init__(self, ec2_service):
        self.ec2_service = ec2_service
        self.sub_name =''
        self.sub_id = ''
        self.sub_vpc = ''
        self.sub_cidr = ''
        self.route_table_id = ''
        self.route_name = ''
        self.route_table = ''

    # subnet_id is list type
    def describe_route(self, subnet_id):
        response = self.ec2_service.describe_route_tables(
            Filters=[{
                'Name': 'association.subnet-id',
                'Values': [subnet_id]
            }]
        )
        id = response['RouteTables'][0]['RouteTableId'] + ' | '
        name = ''
        for tag in response['RouteTables'][0]['Tags']:
            if tag['Key'] == 'Name':
                name = tag['Value']

        return id, name

    # vpc_id should be list type
    def describe_subnet(self, vpc_id):
        response = self.ec2_service.describe_subnets(
            Filters=[{
                'Name': 'vpc-id',
                'Values': vpc_id
            }]
        )

        result = []
        for vpc in vpc_id:
            for sub in response['Subnets']:
                if sub['VpcId'] == vpc:
                    for name in sub['Tags']:
                        if name['Key'] == 'Name':
                            self.sub_name = name['Value']
                    self.sub_id = sub['SubnetId']
                    self.sub_vpc = vpc
                    self.sub_cidr = sub['CidrBlock']
                    self.route_table_id, self.route_name = self.describe_route(self.sub_id)
                    self.route_table = self.route_table_id + self.route_name

                    result.append((self.sub_name, self.sub_id, self.sub_vpc, self.sub_cidr, self.route_table))

        return result