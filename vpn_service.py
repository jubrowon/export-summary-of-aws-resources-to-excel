class vpn:
    def __init__(self, ec2_service):
        self.ec2_service = ec2_service

    # vpc_id is list type
    def describe_vpn_gates(self, vpc_id):
        response = self.ec2_service.describe_vpn_gateways(
            Filters=[{
                'Name': 'attachment.vpc-id',
                'Values': [vpc_id]
            }]
        )

        result = []
        # get vpn gateway id
        vpn_gate_id = response['VpnGateways'][0]['VpnGatewayId']

        # get amazon side asn
        amazonesideasn = response['VpnGateways'][0]['AmazonSideAsn']

        customer_ip = 'Manual needed'
        etc = 'Manual needed'
        vpn_name, customer_gate_id, vpn_connection_id, static_routes, tunnel1, tunnel2 = self.describe_vpn_connect(vpn_gate_id)

        result.append((vpn_name, customer_gate_id, vpn_connection_id, customer_ip, amazonesideasn, tunnel1, tunnel2, static_routes, etc))
        return result

    def describe_vpn_connect(self, vpn_gateway_id):
        vpn_name = ''
        static_route = []
        tunnels = []

        response = self.ec2_service.describe_vpn_connections(
            Filters=[{
                'Name':'vpn-gateway-id',
                'Values': [vpn_gateway_id]
            }]
        )

        vpn_con = response['VpnConnections'][0]

        # get vpn connection id
        vpn_connection_id = vpn_con['VpnConnectionId']

        # get name
        for tag in vpn_con['Tags']:
            if tag['Key'] == 'Name':
                vpn_name = tag['Value']

        # get gateway id
        customer_gate_id = vpn_con['CustomerGatewayId']

        # get static_routes
        for route in vpn_con['Routes']:
            static_route.append(route['DestinationCidrBlock'])

        # get tunnel ip
        for tunnel in vpn_con['VgwTelemetry']:
            tunnels.append(tunnel['OutsideIpAddress'])

        return vpn_name, customer_gate_id, vpn_connection_id, static_route, tunnels[0], tunnels[1]
