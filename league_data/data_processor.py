import json
import os
from datetime import datetime
import requests
from dotenv import load_dotenv
load_dotenv()
#gets most recent champion data from riot ap
class Data_processor:
    #loads champion data from file or riot api into champion_data
    #if the champion data is out of date, it will update it, as well ar archive the old version and add the new version as current
    def __init__(self):
        self.champion_data = self._load_champion_data_from_file()
        current_version = self._current_version_from_riot()
        if current_version != self.champion_data.get("version"):
            #archive the current champion data
            self._archive_current_champion_data(current_version) 

            #self.champion_data = self.get_current_champion_data_from_riot()
            #self.save_champion_data(current_version)
            #self.save_current_champion_data()

    #loads champion data from file
    def _load_champion_data_from_file(self) -> dict:
        path_to_champion_data = os.getenv("PATH_TO_CHAMPION_DATA")
        if not path_to_champion_data:
            raise ValueError("PATH_TO_CHAMPION_DATA environment variable is not set")
        
        file_path = os.path.join(path_to_champion_data, "current_champion_data.json")
        
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return {}
        except PermissionError:
            print(f"Permission denied when trying to read: {file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")
            return {}
        except Exception as e:
            print(f"Unexpected error when reading file {file_path}: {e}")
            return {}

    #gets most recent champion data from riot api
    def _get_current_champion_data_from_riot(self) -> dict:
        response = requests.get(os.getenv("CHAMPION_URL_PRE") 
                                + self._current_version_from_riot() 
                                + os.getenv("CHAMPION_URL_POST"))
        return response.json()

    #gets the current version of the champion data from the riot api
    def _current_version_from_riot(self) -> str:
        #checks if the version of the champion data is up to date with the saved files
        version_url = os.getenv("VERSION_URL")
        if not version_url:
            raise ValueError("VERSION_URL environment variable is not set")
        response = requests.get(version_url)
        return response.json()[0]
    
    def get_champion_data(self) -> dict:
        # Access the entire champion data dictionary
        return self.champion_data

    def get_champion_names(self) -> list:
        # Get a list of all champion names
        return list(self.champion_data['data'].keys())

    def get_champion_info(self, champion_name: str) -> dict:
        # Get information for a specific champion
        return self.champion_data['data'].get(champion_name)

    def get_champion_stat(self, champion_name: str, stat: str) -> float:
        # Get a specific stat for a champion
        return self.champion_data['data'][champion_name]['stats'].get(stat)

    def _save_champion_data(self, version):
        path_to_champion_data = str("current") + os.getenv("PATH_TO_CHAMPION_DATA")
        if not path_to_champion_data:
            raise ValueError("[added prefix] PATH_TO_CHAMPION_DATA environment variable is not set")
        
        #if not os.path.exists(path_to_champion_data):
        #    os.makedirs(path_to_champion_data, exist_ok=True)
        
        filename = str("current") + os.getenv("PATH_TO_CHAMPION_DATA")
        full_path = os.path.join(path_to_champion_data, filename)
        
        try:
            with open(full_path, "w") as file:
                json.dump(self.champion_data, file)
        except IOError as e:
            print(f"Error writing to file {full_path}: {e}")

    #returns true if the archive was successful, false otherwise
    def _archive_current_champion_data(self, current_version) -> bool:
        new_archive_path = str(current_version) + os.getenv("PATH_TO_CHAMPION_DATA")
        archive_dir = os.path.join(os.path.dirname(__file__), "archived_data")
        os.makedirs(archive_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_filename = f"champion_data_{current_version}_{timestamp}.json"
        archive_path = os.path.join(archive_dir, archive_filename)
        
        try:
            with open(archive_path, "w") as file:
                json.dump(self.champion_data, file)
            return True
        except IOError as e:
            print(f"Error writing to file {archive_path}: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error when archiving champion data: {e}")
            return False

    def save_current_champion_data(self, version):
        new_archive_path = os.path.join(os.getenv("PATH_TO_CHAMPION_DATA"), "current_champion_data.json")
        try:
            with open(new_archive_path, "w") as file:
                json.dump(self.champion_data, file)
        except IOError as e:
            print(f"Error writing to file {new_archive_path}: {e}")
        except Exception as e:
            print(f"Unexpected error when archiving champion data: {e}")
        
test = Data_processor()