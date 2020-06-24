import boto3
_ssm = boto3.client('ssm')

class Resolver(object):
    def __init__(self, name, **aliases):
        self.name = name
        self.aliases = aliases

    def __str__(self):
        return self.default

    def __getattr__(self, attr):
        from formant import logger
        attr = self.aliases.get(attr, attr)
        path = f'/aws/service/{self.name}/{attr}'

        logger.debug(f'Getting AMI image ID for {path}...')
        param = _ssm.get_parameter(Name=path)
        return param['Parameter']['Value']

amazon_linux = Resolver('ami-amazon-linux-latest',
    default='amzn2-ami-hvm-x86_64-ebs'
)
