from pathlib import Path

root_path = Path.home() / '.ssh'

def get_key(kind='rsa'):
    assert kind in ('rsa', 'dsa')
    path = root_path / f'id_{kind}.pub'
    try:
        with open(path, 'r') as f:
            return f.read()
    except:
        return None

rsa_key = get_key('rsa')
dsa_key = get_key('dsa')
any_key = rsa_key or dsa_key

def ec2_keypair(name, kind='rsa'):
    import boto3
    from formant import logger
    ec2 = boto3.client('ec2')

    def key_exists(name):
        logger.debug(f'Checking if keypair {name} exists...')
        try:
            ec2.describe_key_pairs(KeyNames=[name])
            logger.debug('Keypair found')
            return True
        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == 'InvalidKeyPair.NotFound':
                logger.debug('Keypair not found')
                return False
            raise err

    if key_exists(name):
        logger.debug(f'Keypair {name} already exists, no further action needed.')
        return name

    logger.info(f'Creating keypair {name}...')
    response = ec2.import_key_pair(
        KeyName = name,
        PublicKeyMaterial = get_key(kind),
    )
    logger.debug(f'Done! Imported key pair {response["KeyName"]} with fingerprint {response["KeyFingerprint"]}.')
    return response['KeyName']
