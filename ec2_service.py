class ec2:
    def __init__(self, ec2_service):
        self.ec2_service = ec2_service

    def describe_ec2s(self, name, value):
        response = self.ec2_service.describe_instances(
            Filters=[{
                'Name': name,
                'Values': [value]
            }]
        )
        return response['Reservations']

    def get_instance_ids(self, vpc_id):
        instances = []
        ec2s_info = []

        ec2 = self.describe_ec2s('vpc-id', vpc_id)

        for num in range(0, len(ec2)):
            instances.append(ec2[num]['Instances'][0]['InstanceId'])

        for ec2s in instances:
            ec2s_info.append(self.get_one_instance_info(ec2s))

        return ec2s_info

    def describe_amis(self, image_id):
        response = self.ec2_service.describe_images(
            Filters=[{
                'Name': 'image-id',
                'Values': [image_id]
            }]
        )

        result = response['Images']
        if result == []:
            result = 'manual needed'
        else:
            result = response['Images'][0]['Name']

        return result


    def get_one_instance_info(self, instance_id):
        instance_name = ''
        ec2_type = ''
        az = ''
        key_pair = ''
        sg_name = ''
        iam_role = ''
        eip = ''
        pip = ''
        id = 'manual needed'
        pw = 'manual needed'
        ebs = ''
        os = ''
        etc = ''
        result = []

        instance = self.describe_ec2s('instance-id', instance_id)
        ins = instance[0]['Instances'][0]  # one_instnace_info is list type

        for name in ins['Tags']:
            if name['Key'] == 'Name':
                instance_name = name['Value']

        ec2_type = ins['InstanceType']
        az = ins['Placement']['AvailabilityZone']
        key_pair = ins['KeyName']

        for sg in ins['SecurityGroups']:
            sg_name += sg['GroupName'] + ', '

        elements_list = []
        for key, val in ins.items():
            elements_list.append(key)
        if elements_list.count('IamInstanceProfile') == 1:
            iam_role = ins['IamInstanceProfile']['Arn'].split('/').pop()
        else:
            iam_role = 'None'

        if elements_list.count('PublicIpAddress') == 1:
            eip = ins['PublicIpAddress']
        else:
            eip = 'None'

        pip = ins['PrivateIpAddress']

        for bl in ins['BlockDeviceMappings']:
            ebs += bl['DeviceName'] + ', ' + bl['Ebs']['VolumeId'] + ' | '

        os = self.describe_amis(ins['ImageId'])

        return (instance_name, instance_id, ec2_type, az, key_pair, sg_name, iam_role, eip, pip, id, pw, ebs, os, etc)