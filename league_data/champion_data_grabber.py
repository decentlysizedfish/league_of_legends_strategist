#this program will load the locally saved champion data and compare it to the latest version,
#if they are not the same it will update the local data with the latest version,
#and archive the old data

#important functions from this class:
#get_champion_all_data() function will return the entire champion data from a json file as dictionary

#this is the only file that interacts with the api and files, so it will be heavy on exception handling

class ChampionDataGrabber:
    #loads the currently saved champion data from the json file saved locally
    #then makes a request to the api to get the latest version of the champion data
    #if they are not the same it will update the local data with the latest version,
    #and archive the old data - the archiving will be handled in the is_up_to_date() function
    def __init__(self):
        pass
    
    #returns a dictionary of the locally saved champion list (main one to be used to avoid excess api calls)
    #loads straight from dir
    def _get_local_champion_data(self) -> dict:
        pass
    #trurns the latest champion data from the api as a dictionary (should only be called once to verify data is up to date)
    #loads straight from api
    def _get_latest_champion_data(self) -> dict:
        pass
    
    #returns the version of the passed champion data dictionary
    def _version_check(self, data:dict) -> str:
        pass

    #only called if version is out of date. 
    #this will take the old data, save it to a new file with the version number as the prefix before "champion_data.json"
    #this will be saved in seperate nested folder called "archived_data"
    def _archive_old_data(self, old_data:dict):
        pass








