import json
import logging
import argparse
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('json_reader')

def read_json_file(file_path):
    """
    Read and parse a JSON file
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict: Parsed JSON data
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
            
        logger.info(f"Reading JSON file: {file_path}")
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        logger.info("JSON content:")
        logger.info(json.dumps(data, indent=2))
        
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format: {e}")
        raise
    except Exception as e:
        logger.error(f"Error reading JSON file: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read and log JSON file contents')
    parser.add_argument('--file', type=str, required=True, help='Path to the JSON file')
    
    args = parser.parse_args()
    read_json_file(args.file)
