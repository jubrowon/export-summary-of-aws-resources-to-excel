class direct_connect:
    def __init__(self, directconnect_service):
        self.dx = directconnect_service

    def describe_peer_ip(self, connection_id):
        response = self.dx.describe_virtual_inerfaces(
            connectionId=connection_id
        )

        vgw = ''
        yourip = ''
        amazonip = ''

        if len(response) !=2:
            for i in response['virtualInterfaces']:
                vgw = i['virtualGatewayId']
                yourip = i['customerAddress']
                amazonip = i['amazonAddress']

        return vgw, yourip, amazonip

    def describe_dx(self):
        response = self.dx.describe_connections()

        connection_id = 'Not found'
        connection_name = 'Not found'
        connection_info = 'Not found'
        vgw = 'Not found'
        yourip = 'Not found'
        amazonip = 'Not found'
        result = []
        if len(response) != 2 :
            for i in response['connections']:
                connection_name = i['connectionName']
                connection_id = i['connections']
                vgw, yourip, amazonip = self.describe_peer_ip(connection_id)
                connection_info = 'region: {}, location: {}, bandwidth: {}, lagId: {}'.format(i['region'], i['location'], i['bandwidth'], i['lagId'])

            result.append((connection_name, connection_id, connection_info))
        else:
            result.append((connection_name, connection_id, connection_info, vgw, yourip, amazonip))

        return result