pipeline {
    agent any
    
    // Define parameters for the pipeline
    parameters {
        string(name: 'JSON_FILE_PATH', defaultValue: 'data/config.json', description: 'Path to the JSON file to read')
        string(name: 'AWS_APPCONFIG_APP', defaultValue: 'app0001', description: 'AWS AppConfig application name')
        string(name: 'AWS_APPCONFIG_PROFILE', defaultValue: 'olacon1', description: 'AWS AppConfig configuration profile')
        string(name: 'AWS_APPCONFIG_ENV', defaultValue: 'devl', description: 'AWS AppConfig environment')
    }
    
    // Define environment variables
    environment {
        BRANCH_NAME = "${env.GIT_BRANCH ?: 'main'}".replaceFirst('origin/', '')
        ENV_NAME = "${BRANCH_NAME}" // Uses the branch name to determine environment
        AWS_REGION = "us-east-1" // Default AWS region, can be overridden
        VENV_PATH = "${WORKSPACE}/venv"
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
        
        stage('Setup Python Environment') {
            steps {
                // Ensure python3-full and python3-venv are installed
                sh '''
                    echo "Checking Python installation..."
                    python3 --version
                    
                    # Install python3-full and python3-venv (if possible)
                    apt-get update -y && apt-get install -y python3-full python3-venv || true
                    
                    # Create a virtual environment
                    echo "Creating virtual environment at ${VENV_PATH}"
                    python3 -m venv ${VENV_PATH}
                    
                    # Activate virtual environment and install dependencies
                    . ${VENV_PATH}/bin/activate
                    pip install --upgrade pip
                    pip install boto3
                    
                    # Verify installations
                    pip list | grep boto3
                '''
            }
        }
        
        stage('Read JSON') {
            steps {
                // Run Python script with appropriate command
                sh '''
                    # Activate virtual environment
                    . ${VENV_PATH}/bin/activate
                    
                    # Run the script
                    python read_json.py --file ${JSON_FILE_PATH}
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
                            
                            # Activate virtual environment
                            . ${VENV_PATH}/bin/activate
                            
                            # Run the script
                            python get_aws_appconfig.py --app ${AWS_APPCONFIG_APP} --profile ${AWS_APPCONFIG_PROFILE} --env ${AWS_APPCONFIG_ENV}
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
        always {
            // Clean up (optional)
            echo "Job completed. Virtual environment can be found at: ${VENV_PATH}"
        }
    }
}