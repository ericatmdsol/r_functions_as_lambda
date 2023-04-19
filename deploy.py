import os
import hydra
import boto3
from omegaconf import DictConfig, OmegaConf

def get_lambda():
    client = boto3.client('sts')
    arn = "arn:aws:iam::833923177614:role/DataScience-Engineering"
    response = client.assume_role(RoleArn=arn, RoleSessionName="boto3")
    response = response['Credentials']

    # Create a lambda session
    lambda_resource=boto3.client('lambda',
        aws_access_key_id=response['AccessKeyId'],
        aws_secret_access_key=response['SecretAccessKey'],
        aws_session_token=response['SessionToken'])
    return lambda_resource

@hydra.main(version_base=None, config_path=".", config_name="config")
def main(cfg : DictConfig) -> None:
    docker_build = f"""docker build . --network=host -t {cfg['docker_img']}"""
    docker_login_remote = f"""aws ecr get-login-password --region us-east-1 --profile okta-orangeds | docker login --username AWS --password-stdin {cfg['ecr_address']}"""
    docker_set_remote = f"""docker tag {cfg['docker_img']} {cfg['ecr_address']}/{cfg['lambda_name']}"""
    docker_push = f"""docker push {cfg['ecr_address']}/{cfg['lambda_name']}"""

    ecr_steps = [docker_build, docker_login_remote, docker_set_remote, docker_push]
    list(map(lambda x: os.system(x), ecr_steps))
    create_lambda = f"""aws lambda create-function --function-name {cfg['lambda_name']} --package-type Image --code ImageUri={cfg['ecr_address']}/{cfg['docker_img']}"""
    create_lambda +=  f""" --role {cfg['role']} --profile okta-orangeds --memory-size {cfg['memory']}"""

    update_lambda = f"""aws lambda update-function-code --function-name {cfg['lambda_name']} --image-uri {cfg['ecr_address']}/{cfg['docker_img']} --profile okta-orangeds"""
    client = get_lambda()
    try:
        client.get_function(FunctionName=cfg['lambda_name'])
        print(update_lambda)
        os.system(update_lambda)
    except Exception as e:
        os.system(create_lambda)
        

if __name__ == "__main__":
    main()
    
