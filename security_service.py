class security_groups:
    def __init__(self, ec2_service):
        self.ec2_service = ec2_service

    # name is vpc-id or group-id and value is vpc-id or group-id
    def describe_securities(self, name, value):
        response = self.ec2_service.describe_security_groups(
            Filters=[{
                'Name': name,
                'Values': [value]
            }]
        )

        return response['SecurityGroups']

    def descirbe_sg_ids(self, vpc_id):
        response = self.describe_securities('vpc-id', vpc_id)
        sg_group_ids = []
        for secid in response:
            for key, val in secid.items():
                if key == 'GroupId':
                    sg_group_ids.append(val)

        return sg_group_ids

    def get_ip_ranges(self, sg_id, group_name, ip_permitions):
        protocol = ''
        protocol_type = ''
        port_range = ''
        sources = ''
        descrip = ''
        result = []

        for permitions in ip_permitions:
            protocol = permitions['IpProtocol']
            if protocol == '-1':
                port_range, protocol = 'ALL', 'ALL'
                protocol_type = 'ALL Traffic'
            if protocol == 'tcp' and permitions['FromPort'] == 80:
                protocol_type = 'HTTP(80)'
                port_range = permitions['ToPort']
            if protocol == 'tcp' and permitions['FromPort'] == 22:
                protocol_type = 'SSH(22)'
                port_range = permitions['ToPort']
            if protocol == 'tcp' and permitions['FromPort'] != 22 and permitions['FromPort'] != 80:
                protocol_type = 'Custom TCP Rule(6)'
                port_range = permitions['ToPort']
            if protocol == 'tcp' and permitions['FromPort'] == 0:
                protocol_type = 'ALL TCP'
                port_range = 'ALL'
            if protocol == 'udp' and permitions['FromPort'] == 0:
                protocol_type = 'ALL UDP'
                port_range = 'ALL'
            if protocol == 'icmp':
                protocol_type = 'ALL ICMP - IPV4'
                port_range = 'ALL'

            if permitions['IpRanges'] != []:
                for j in permitions['IpRanges']:
                    if len(j) == 2:
                        sources = j['CidrIp']
                        descrip = j['Description']
                    if len(j) == 1:
                        sources = j['CidrIp']
                    if len(j) == 0:
                        sources = 'No source'
                    if protocol != '' and port_range != '' and sources != '' and descrip != '':
                        result.append((sg_id, group_name, protocol_type, protocol, port_range, sources, descrip))

            if permitions['UserIdGroupPairs'] != []:
                for i in permitions['UserIdGroupPairs']:
                    if len(i) == 3:
                        sources = i['GroupId']
                        descrip = i['Description']
                    if len(i) == 2:
                        sources = i['GroupId']
                        descrip = 'None'
                    if len(i) == 0:
                        sources = 'No source'
                    if protocol != '' and port_range != '' and sources != '' and descrip != '':
                        result.append((sg_id, group_name, protocol_type, protocol, port_range, sources, descrip))

        return result

    # sg_ids is list type
    def describe_ips(self, vpc_id):
        result = []
        group_name = ''
        get_permissions = None
        sg_ids = self.descirbe_sg_ids(vpc_id)

        for sg in sg_ids:
            sg_info = self.describe_securities('group-id', sg)
            for sg_list in sg_info:
                for gp_name, gp_val in sg_list.items():
                    if gp_name == 'GroupName':
                        group_name = gp_val
                    if gp_name == 'IpPermissions':
                        get_permissions = self.get_ip_ranges(sg, group_name, gp_val)

            result.append(get_permissions)

        return result