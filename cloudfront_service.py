class cloudfront:

    def __init__(self, cloudfront_service):
        self.cf = cloudfront_service

    def describe_cfs(self):
        response = self.cf.list_distributions()

        result = []
        ids = ''
        cf_domain = ''
        cf_origin = ''
        cf_cname = ''
        etc = ''

        for id in response['DistributionList']['Items']:
            ids = id['Id']
            cf_domain = id['DomainName']
            cf_origin = id['Origins']
            if len(id['Aliases']) != 1:
                cf_cname = id['Aliases']['Items']
            else:
                cf_cname = 'None'

            result.append((ids, cf_domain, cf_origin, cf_cname, etc))

        return result


