import os
import boto3

from django.conf import settings

custom_credentials_path = ".aws/credentials"
custom_config_path = ".aws/config"

# Update the environment variables to point to the custom locations
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = custom_credentials_path
os.environ['AWS_CONFIG_FILE'] = custom_config_path

dynamodb = boto3.resource("dynamodb")
nutrition_intakes_dynamodb_table = dynamodb.Table("nutrition-intakes")
foods_dynamodb_table = dynamodb.Table("foods")
