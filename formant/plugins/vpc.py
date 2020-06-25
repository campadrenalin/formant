import boto3
ec2 = boto3.client('ec2')

class VPC(dict):
    def __getattr__(self, attr):
        return self[attr]

    def __str__(self):
        return self.VpcId

def get_vpcs(*filters):
    matches = ec2.describe_vpcs(Filters=filters)['Vpcs']
    for match in matches:
        yield VPC(match)

def get_vpc(*filters):
    return next(get_vpcs(*filters))

default = get_vpc({'Name':'isDefault', 'Values': ['true']})
