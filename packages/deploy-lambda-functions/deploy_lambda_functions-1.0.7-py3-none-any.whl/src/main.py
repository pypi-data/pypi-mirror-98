import sys, argparse,os
from .configManager import load_config,get_variables
from .LambdaFunction import LambdaFunction
from .S3 import S3Bucket
from .Zip import Zip



def deploy(config):
    bucket_name = os.environ["LAMBDA_CODE_BUCKET"]
    function = LambdaFunction(config["FUNCTION_NAME"])
    if "LAMBDA_IMAGE" in config:
        function.deploy_image(config["LAMBDA_IMAGE"])
    else:
        code_zip = Zip(name=config["FUNCTION_NAME"],path=config["CODE_DIR"]).name
        code_bucket = S3Bucket(bucket_name)
        code_bucket.upload_file(code_zip)
        function.deploy_zip(bucket_name,code_zip)
   
    variables = get_variables(config)
    function.update_env_variables(variables)

    version = function.publish_version(config["VERSION"])["Version"]
    function.update_alias(alias="stable",description=config["VERSION"],version=version)

def parse_args():
    parser = argparse.ArgumentParser(description='Deploy lambda function')
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        help='config directory or file',
        required=True
    )
    return parser.parse_args()

def main():
    args = parse_args()
    config = load_config(args.config)
    deploy(config)