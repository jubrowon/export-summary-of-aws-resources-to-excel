class vpc:

    def __init__(self, ec2_service):
        self.ec2_service = ec2_service
        self.cidr = ''
        self.vpcid = ''
        self.vpc_name = ''
        self.flow_logs = ''
        self.flow = ''

    def describe_flowlogs(self, vpc_id):
        response = self.ec2_service.describe_flow_logs(
            Filters=[{
                'Name':'flow-log-id',
                'Values': [vpc_id]
            }]
        )

        return response['FlowLogs']

    # tag_val is list type, tag_val = []
    def desecribe_vpc(self, tag_val):
        response = self.ec2_service.describe_vpcs(
            Filters=[{
                'Name': 'tag-value',
                'Values': tag_val
            }]
        )

        vpc_info = []
        if 1 <= len(response['Vpcs']):
            for i in range(0, len(response['Vpcs'])):
                self.vpc_name = tag_val[i]
                self.cidr = response['Vpcs'][i]['CidrBlock']
                self.vpcid = response['Vpcs'][i]['VpcId']
                flow = self.describe_flowlogs(self.vpcid)
                if flow ==[]:
                    self.flowlog = 'No flow log found'
                else:
                    self.flowlog = flow[0]['FlowLogId']

                vpc_info.append((self.vpc_name, self.cidr, self.vpcid, self.flowlog))
        
        return vpc_info