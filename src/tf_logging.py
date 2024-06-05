import requests
import json
import sys

from src.managers.configs import ConfigurationsManager

config_manager = ConfigurationsManager()

TENSORFUSE_ID = {
    "teamId": config_manager.config.secret.tf_team_id,
    "projectId":  config_manager.config.secret.tf_proj_id,
    "datasourceId": config_manager.config.secret.tf_ds_id,
}

def track_tensorfuse_log(log_data):
    data = {
        "completionProperties": log_data
    }
    data.update(TENSORFUSE_ID)
    data_json = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config_manager.config.secret.tf_key}'
    }
    url = 'https://api.tensorfuse.io/tensorfuse/datasource/log-completion/'
    try:
        response = requests.post(url, data=data_json, headers=headers)
        if response.status_code == 200:
            print("Successfully logged to TensorFuse.")
        else:
            print(f"Failed to log to TensorFuse: {response.status_code}")
    except Exception as e:
        print(f"Error logging to TensorFuse: {e}")