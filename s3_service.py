class s3s:
    def __init__(self, s3_service):
        self.s3_service = s3_service


    def describe_s3s(self):
        response = self.s3_service.list_buckets()

        result = []
        bucket_names = []
        bucket_name = ''
        bucket_location = ''
        use = 'Manual needed'
        user = 'Manual needed'
        auth = 'Manual needed'

        for bname in response['Buckets']:
            bucket_names.append(bname['Name'])

        for name in bucket_names:
            bucket_name = name
            buck_location = self.s3_service.get_bucket_location(Bucket=name)['LocationConstraint']
            result.append((bucket_name, buck_location, use, user, auth))

        return result