#this program will load the locally saved champion data and compare it to the latest version,
#if they are not the same it will update the local data with the latest version,
#and archive the old data

#important functions from this class:
#get_champion_all_data() function will return the entire champion data from a json file as dictionary

#this is the only file that interacts with the api and files, so it will be heavy on exception handling
import json #for json file handling
import requests #for api calls
import os #for file handling
import dotenv #for environment variable handling #loads the environment variables from the .env file
class ChampionDataGrabber:
    dotenv.load_dotenv() #loads the environment variables from the .env file

    #add .env variables for later easier access
    CHAMPION_URL_PRE = os.getenv("CHAMPION_URL_PRE")
    CHAMPION_URL_POST = os.getenv("CHAMPION_URL_POST")
    LOCAL_CHAMPION_DATA_PATH = os.getenv("LOCAL_CHAMPION_DATA_PATH")
    ARCHIVE_CHAMPION_DATA_PATH = os.getenv("ARCHIVE_CHAMPION_DATA_PATH")
    ARCHIVE_CHAMPION_DATA_PATH_FILE_NAME = os.getenv("ARCHIVE_CHAMPION_DATA_PATH_FILE_NAME")
    VERSION_CHECK_URL = os.getenv("VERSION_CHECK_URL")

    
    
    #loads the currently saved champion data from the json file saved locally
    #then makes a request to the api to get the latest version of the champion data
    #if they are not the same it will update the local data with the latest version,
    #and archive the old data
    def __init__(self):
        self.champion_data = self._get_local_champion_data()
        if not self.champion_data:
            print("Failed to get champion data. Using empty data.")
            self.champion_data = {}
        #checks if versions are the same
        if self._version_check_local(self.champion_data) != self._version_check_api():
            print("version mismatch, archiving old data")
            self._archive_old_data(self.champion_data)
            self.champion_data = self._get_latest_champion_data()
        else:
            print("version match, no need to update")
        self._save_champion_data(self.champion_data)


    #all the following functions are private and should only be called by the class <

    #returns a dictionary of the locally saved champion list (main one to be used to avoid excess api calls)
    #loads straight from dir
    def _get_local_champion_data(self) -> dict:
        try:
            with open(self.LOCAL_CHAMPION_DATA_PATH, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Local file not found. Fetching data from API.")
            return self._get_latest_champion_data()

    #trurns the latest champion data from the api as a dictionary (should only be called if out of date)
    #loads straight from api
    def _get_latest_champion_data(self) -> dict:
        try:
            response = requests.get(self.CHAMPION_URL_PRE + str(self._version_check_api()) + self.CHAMPION_URL_POST)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return {}  # Return an empty dict
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}  # Return an empty dict

    #get real current version
    #returns the version of the passed champion data dictionary
    def _version_check_local(self, data:dict) -> str:
        return data["version"] 
        
    #usues a seperate call to the api to get the latest version number
    def _version_check_api(self) -> str:
        try:
            response = requests.get(self.VERSION_CHECK_URL)
            response.raise_for_status()
            return response.json()[0]  # Assuming the first item is the latest version
        except Exception as e:
            print(f"Error checking API version: {e}")
            return "0.0.0"  # Return a default version

    #only called if version is out of date. 
    #this will take the old data, save it to a new file with the version number as the prefix before "champion_data.json"
    #this will be saved in seperate nested folder called "archived_data"
    def _archive_old_data(self, old_data:dict):
        try:
            version_to_archive = self._version_check_local(old_data)
            path_to_archive = os.path.join(self.ARCHIVE_CHAMPION_DATA_PATH, f"{version_to_archive}{self.ARCHIVE_CHAMPION_DATA_PATH_FILE_NAME}")
            
            # Ensure the archive directory exists
            os.makedirs(os.path.dirname(path_to_archive), exist_ok=True)
            
            with open(path_to_archive, "w") as file:
                json.dump(old_data, file)
            print(f"Successfully archived data to {path_to_archive}")
        except IOError as e:
            print(f"Error archiving old data: {e}")
        except Exception as e:
            print(f"Unexpected error while archiving old data: {e}")

    def _save_champion_data(self, data: dict):
        with open(self.LOCAL_CHAMPION_DATA_PATH, "w") as file:
            json.dump(data, file)


    #end of private functions >

    #these functions are public and should be called to gather useful information about each character
    #first function will return a champions full stats as a dictionary
    def get_champion_full_stats(self, champion_name:str) -> dict:
        return self.champion_data["data"][champion_name]
    
    def get_champion_tags(self, champ: dict) -> dict:
        return champ["tags"]

test = ChampionDataGrabber()
test.get_champion_full_stats("Aatrox")
print(test.get_champion_stats_by_tag(test.get_champion_full_stats("Aatrox")))

