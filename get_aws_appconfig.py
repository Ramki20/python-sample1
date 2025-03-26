import boto3
import logging
import argparse
import json
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('aws_appconfig')

def get_aws_appconfig(application_name, configuration_profile, environment='default'):
    """
    Retrieve the latest configuration from AWS AppConfig
    
    Args:
        application_name (str): AWS AppConfig application name
        configuration_profile (str): AWS AppConfig configuration profile
        environment (str): AWS AppConfig environment name (default: 'default')
        
    Returns:
        dict: Retrieved configuration data
    """
    try:
        logger.info(f"Retrieving AWS AppConfig for application: {application_name}, "
                    f"profile: {configuration_profile}, environment: {environment}")
        
        # Create AppConfig client
        appconfig_client = boto3.client('appconfig')
        
        # Get latest configuration version
        config_response = appconfig_client.get_configuration(
            Application=application_name,
            Environment=environment,
            Configuration=configuration_profile,
            ClientId='jenkins-pipeline'  # Unique identifier for the client
        )
        
        # Extract content
        content = config_response['Content'].read()
        logger.info("AWS AppConfig content retrieved successfully")
        
        # Parse content (assuming JSON format)
        config_data = json.loads(content)
        
        # Log the configuration (with sensitive information masked if needed)
        logger.info("AWS AppConfig content:")
        logger.info(json.dumps(config_data, indent=2))
        
        return config_data
        
    except Exception as e:
        logger.error(f"Error retrieving AWS AppConfig: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve and log AWS AppConfig')
    parser.add_argument('--app', type=str, required=True, help='AWS AppConfig application name')
    parser.add_argument('--profile', type=str, required=True, help='AWS AppConfig configuration profile')
    parser.add_argument('--env', type=str, default='default', help='AWS AppConfig environment name')
    
    args = parser.parse_args()
    get_aws_appconfig(args.app, args.profile, args.env)