pipeline {
    agent any
    
    // Define parameters for the pipeline
    parameters {
        string(name: 'JSON_FILE_PATH', defaultValue: 'data/config.json', description: 'Path to the JSON file to read')
    }
    
    // Define environment variables
    environment {
        BRANCH_NAME = "${env.GIT_BRANCH ?: 'main'}".replaceFirst('origin/', '')
        ENV_NAME = "${BRANCH_NAME}" // Uses the branch name to determine environment
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
        
        stage('Install Python') {
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
    }
    
    post {
        success {
            echo "Successfully processed JSON file in ${ENV_NAME} environment"
        }
        failure {
            echo "Failed to process JSON file in ${ENV_NAME} environment"
        }
    }
}