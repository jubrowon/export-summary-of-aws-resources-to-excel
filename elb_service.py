class elb:
    def __init__(self, elb, elb2):
        self.elb = elb
        self.elb2 = elb2


    def describe_classic_listeners(self, elb_name):
        response = self.elb.describe_instance_health(LoadBalancerName=elb_name)

        return response['InstanceStates']

    def describe_not_classic_listeners(self, elb_arn):
        response = self.elb2.describe_listeners(LoadBalancerArn=elb_arn)

        return response['Listeners']

    def descrbie_classic_elb(self):
        response = self.elb.describe_load_balancers()

        elb_name = ''
        dns_name = ''
        port = ''
        az = ''
        instance_check = '_'
        host_count = ''
        health_check = ''
        result = []

        for elb in response['LoadBalancerDescriptions']:
            elb_name = elb['LoadBalancerName']
            dns_name = elb['DNSName']

            for i in elb['ListenerDescriptions']:
                port = '{0} forwarding to {1}'.format(i['Listener']['LoadBalancerPort'], i['Listener']['InstancePort'])

            for i in elb['AvailabilityZones']:
                az += i + ', '

            instance_check = self.describe_classic_listeners(elb_name)
            for i in instance_check:
                if i !=[]:
                    insid = i['InstanceId']
                    state = i['State']
                    host_count += '{0} is in {1}, '.format(insid, state)
                else:
                    host_count = 'No instances'

            health_check = elb['HealthCheck']

            result.append((elb_name, dns_name, port, az, host_count, health_check))

        return result

    def describe_not_classic_elb(self):
        response = self.elb2.describe_load_balancers()

        elb_name = ''
        elb_arn = ''
        dns_name = ''
        port = ''
        target = ''
        az = ''
        host_count = ''
        health_check = ''
        result = []

        for balancer in response['LoadBalancers']:
            elb_name = balancer['LoadBalancerName']
            elb_arn = balancer['LoadBalancerArn']
            dns_name = balancer['DNSName']
            az = balancer['AvailabilityZones'][0]['ZoneName']

            elb_listener = self.describe_not_classic_listeners(elb_arn)
            if elb_listener !=[]:
                for i in elb_listener:
                    ports = i['Port']
                    target = i['DefaultActions'][0]['TargetGroupArn'].split('/')[1]
                    port += '{0} forwarding to {1}, '.format(ports, target)
                host_count += '{} has been found as targets'.format(len(elb_listener))
            else:
                port = 'None'
                target = 'None'
                host_count = 'None'
            health_check = 'No exists'

            result.append((elb_name, elb_arn, dns_name, az, host_count, health_check))
        return result