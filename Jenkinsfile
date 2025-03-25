pipeline {
    agent any
    
    // Define parameters for the pipeline
    parameters {
        string(name: 'JSON_FILE_PATH', defaultValue: 'data/config.json', description: 'Path to the JSON file to read')
    }
    
    // Define environment variables
    environment {
        ENV_NAME = "${BRANCH_NAME}" // Uses the branch name to determine environment
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Check out the code from Bitbucket
                checkout scm
                
                // Display current branch info
                bat "echo 'Current branch: ${BRANCH_NAME}'"
                bat "echo 'Environment: ${ENV_NAME}'"
            }
        }
        
        stage('Setup Python') {
            steps {
                // Setup Python environment
                bat '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                '''
            }
        }
        
        stage('Read JSON') {
            steps {
                // Activate virtual environment and run the Python script
                bat '''
                    . venv/bin/activate
                    python read_json.py --file ${JSON_FILE_PATH}
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
        always {
            // Clean up
            bat 'if exist venv rmdir /s /q venv'
        }
    }
}
