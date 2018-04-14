class route:
    def __init__(self, ec2_service):
        self.ec2_service = ec2_service
        self.route_table_id = ''
        self.route_name = ''
        self.main = ''

    # subent_id is list type
    def describe_route(self, subnet_id):
        response = self.ec2_service.describe_route_tables(
            Filters=[{
                'Name': 'association.subnet-id',
                'Values': subnet_id
            }]
        )

        result = []

        for route in response['RouteTables']:
            for tag in route['Tags']:
                if tag['Key'] == 'Name':
                    self.route_name = tag['Value']
            self.route_table_id = route['Associations'][0]['RouteTableId']

            if route['Associations'][0]['Main'] == True:
                self.main = 'Yes'
            else:
                self.main = 'No'

            result.append((self.route_name, self.route_table_id, self.main))

        return result