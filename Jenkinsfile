pipeline {
    agent {
        docker {
            image 'python:3.12'  // Use Python Docker image
            args '-v ${WORKSPACE}:/workspace' // Mount workspace for better performance
            reuseNode true // Run on the same node as the Jenkins agent
        }
    }
    
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
        
        stage('Read JSON') {
            steps {
                // No need for venv in Docker - Python is already set up
                sh "python read_json.py --file ${params.JSON_FILE_PATH}"
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