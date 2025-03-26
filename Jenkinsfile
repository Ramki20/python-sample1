pipeline {
    agent any
    
    // Define parameters for the pipeline
    parameters {
        string(name: 'JSON_FILE_PATH', defaultValue: 'data/config.json', description: 'Path to the JSON file to read')
        string(name: 'AWS_APPCONFIG_APP', defaultValue: 'app0001', description: 'AWS AppConfig application name')
        string(name: 'AWS_APPCONFIG_PROFILE', defaultValue: 'olacon1', description: 'AWS AppConfig configuration profile')
        string(name: 'AWS_APPCONFIG_ENV', defaultValue: 'default', description: 'AWS AppConfig environment')
    }
    
    // Define environment variables
    environment {
        BRANCH_NAME = "${env.GIT_BRANCH ?: 'main'}".replaceFirst('origin/', '')
        ENV_NAME = "${BRANCH_NAME}" // Uses the branch name to determine environment
        AWS_REGION = "us-east-1" // Default AWS region, can be overridden
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Check out the code from Bitbucket
                checkout scm
                
                // Display current branch info
                sh "echo 'Current branch: ${BRANCH_NAME}'"
                sh "echo 'Environment: ${ENV_NAME}'"
            }
        }
        
        stage('Install Python and Dependencies') {
            steps {
                // Attempt to install Python directly
                sh '''
                    # Update package lists
                    apt-get update -y || true
                    
                    # Install Python 3 and pip
                    apt-get install -y python3 python3-pip || true
                    
                    # If that fails due to permissions, try with sudo
                    if ! command -v python3 &> /dev/null; then
                        sudo apt-get update -y || true
                        sudo apt-get install -y python3 python3-pip || true
                    fi
                    
                    # Check if Python was successfully installed
                    python3 --version || echo "Failed to install Python3"
                    
                    # Install AWS SDK for Python (boto3)
                    python3 -m pip install boto3 || sudo python3 -m pip install boto3
                '''
            }
        }
        
        stage('Read JSON') {
            steps {
                // Run Python script with appropriate command
                sh '''
                    if command -v python3 &> /dev/null; then
                        python3 read_json.py --file ${JSON_FILE_PATH}
                    elif command -v python &> /dev/null; then
                        python read_json.py --file ${JSON_FILE_PATH}
                    else
                        echo "ERROR: No Python interpreter found."
                        echo "Please install Python in your Jenkins environment."
                        exit 1
                    fi
                '''
            }
        }
        
        stage('Get AWS AppConfig') {
            steps {
                // Configure AWS credentials
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
                                  credentialsId: 'aws-credentials',
                                  accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
                                  secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    
                    // Set AWS region
                    withEnv(["AWS_DEFAULT_REGION=${AWS_REGION}"]) {
                        
                        // Run Python script to retrieve AWS AppConfig
                        sh '''
                            echo "Retrieving AWS AppConfig for application: ${AWS_APPCONFIG_APP}, profile: ${AWS_APPCONFIG_PROFILE}"
                            
                            if command -v python3 &> /dev/null; then
                                python3 get_aws_appconfig.py --app ${AWS_APPCONFIG_APP} --profile ${AWS_APPCONFIG_PROFILE} --env ${AWS_APPCONFIG_ENV}
                            elif command -v python &> /dev/null; then
                                python get_aws_appconfig.py --app ${AWS_APPCONFIG_APP} --profile ${AWS_APPCONFIG_PROFILE} --env ${AWS_APPCONFIG_ENV}
                            else
                                echo "ERROR: No Python interpreter found."
                                exit 1
                            fi
                        '''
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo "Successfully processed JSON file and AWS AppConfig in ${ENV_NAME} environment"
        }
        failure {
            echo "Failed to process JSON file or AWS AppConfig in ${ENV_NAME} environment"
        }
    }
}