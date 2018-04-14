class nat:
    def __init__(self, ec2_service):
        self.ec2_service = ec2_service

    def describe_nats(self, vpc_id):
        response = self.ec2_service.describe_nat_gateways(
            Filters=[{
                'Name': 'vpc-id',
                'Values': [vpc_id]
            }]
        )

        nat_res = response['NatGateways'][0]
        result = []

        # get nat_id
        nat_id = nat_res['NatGatewayId']

        # get EIP
        nat_eip, nat_privte = [], []
        for ips in nat_res['NatGatewayAddresses']:
            nat_eip.append(ips['PublicIp'])
            nat_privte.append(ips['PrivateIp'])

        # get subnet id
        sub_id = nat_res['SubnetId']

        result.append((nat_id, nat_eip, nat_privte, vpc_id, sub_id))

        return result