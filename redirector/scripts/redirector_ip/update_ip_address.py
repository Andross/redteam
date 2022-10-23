# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:   
# https://aws.amazon.com/developers/getting-started/python/

import boto3, requests
import base64, json
import argparse
from botocore.exceptions import ClientError
from requests.auth import HTTPBasicAuth
from get_public_ip import get_public_ip

proxies = {
              "http"  : "http://192.168.42.120:8080",
              "https" : "http://192.168.42.120:8080"
            }


def get_secret():

    secret_name = "name-api"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret
    # Your code goes here. 

def update_domain_ip(domain, username):

    headers = {'Content-Type':'application/json'}

    api_key_json = json.loads(get_secret())
    api_key = api_key_json[next(iter(api_key_json))]
    r = requests.get('https://api.name.com/v4/domains/{domain}/records'.format(domain=domain), auth=HTTPBasicAuth(username, api_key))
    # print(r.json())
    public_ip = get_public_ip().strip('\n')
    print('Public IP is {0}'.format(public_ip))
    records_json = r.json()
    if records_json is not None:
        for record in records_json['records']:
            # print(record) 
            if(record['type'] == 'A'):
                print(record)
                host_or_fqdn,host_or_fqdn_value = get_host_or_fqdn(record) 
                data = {host_or_fqdn:host_or_fqdn_value,"type":"A","answer":public_ip,"ttl":300}
                print(data)
                update_resp = requests.put('https://api.name.com/v4/domains/{domain}/records/{record_id}'.format(domain=domain, record_id=record['id']), auth=HTTPBasicAuth(username, api_key), json=data, headers=headers)
                print(update_resp.content)

def get_host_or_fqdn(record):
    if 'host' in record:
        return 'host',record['host']
    elif 'fqdn' in record:
        return 'fqdn',record['fqdn']

def main():
    parser = argparse.ArgumentParser(description='A python script used to update the IP address for domains you own on name.com')
    parser.add_argument('-d','--domain', help='Description for foo argument', required=True)
    parser.add_argument('-u','--username', help='Description for bar argument', required=True)
    args = vars(parser.parse_args())
    update_domain_ip(args['domain'],args['username'])


if "__main__":
    main()