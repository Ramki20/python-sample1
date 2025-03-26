import boto3
import logging
import argparse
import json
import os
import base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('aws_appconfig')

def get_aws_appconfig(application_name, configuration_profile, environment='default'):
    """
    Retrieve the latest configuration from AWS AppConfig using AppConfig Data API
    
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
        
        # Create AppConfig Data client (the new API)
        appconfig_data_client = boto3.client('appconfigdata')
        
        # Step 1: Start a configuration session
        session_response = appconfig_data_client.start_configuration_session(
            ApplicationIdentifier=application_name,
            EnvironmentIdentifier=environment,
            ConfigurationProfileIdentifier=configuration_profile
        )
        
        session_token = session_response['InitialConfigurationToken']
        logger.info("Configuration session started successfully")
        
        # Step 2: Get the latest configuration with the session token
        config_response = appconfig_data_client.get_latest_configuration(
            ConfigurationToken=session_token
        )
        
        # Get the configuration content
        content = config_response['Configuration'].read()
        next_token = config_response['NextPollConfigurationToken']
        
        # Parse content (assuming JSON format)
        if content:
            try:
                config_data = json.loads(content)
                # Log the configuration (with sensitive information masked if needed)
                logger.info("AWS AppConfig content retrieved successfully")
                logger.info("AWS AppConfig content:")
                logger.info(json.dumps(config_data, indent=2))
                return config_data
            except json.JSONDecodeError:
                # If not JSON, try to decode as string
                content_str = content.decode('utf-8')
                logger.info("AWS AppConfig raw content retrieved successfully")
                logger.info("Content (non-JSON):")
                logger.info(content_str)
                return {"raw_content": content_str}
        else:
            logger.info("No configuration content retrieved")
            return {}
        
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