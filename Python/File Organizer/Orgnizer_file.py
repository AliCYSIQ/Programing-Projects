from pathlib import Path
from datetime import datetime
import json



IGNORE_FILES = {"history_of_files", "config.json"}
## return all the  files in a folder
def files_in_Folder(Folder_path):
    return  [file for file in Path(Folder_path).iterdir() if file.is_file()]

folder = "/home/ali/s_downloads"

files = files_in_Folder(folder)

config_path = Path(folder) / "config.json"
if  config_path in files and config_path.stat().st_size > 0:
    with open(config_path,"r") as f:
         EXT_MAP = json.load(f)
    print(f"config.json exists , we will use it.\n\n {EXT_MAP}\n")
else:
    
    EXT_MAP = {
        ".txt": "Document",
        ".png": "Image",
        ".zip": "Archive",
        ".py": "Programing",
        ".mp4": "Video"
    }
    print(f"we don't see config.json or the file is empty, we will use  our defualt.\n \n{EXT_MAP}\n")

if len(files) == 0:
    print("The Folder Is Empty")
else:
    for file in files:
        if file.name in IGNORE_FILES:
            print(f"{file.name}: Ignoring system file...")
            continue
        ## name for the new folder
        folder_name = EXT_MAP.get(file.suffix.lower(),"other")
        ## path for the new folder
        
        folder_path = Path(folder) / folder_name
        
        folder_path.mkdir(parents=True,exist_ok=True)
        
        new_file = folder_path / file.name
        if new_file.exists():
            print(f"Skipping {new_file}, already exists.")
        else:
            
            file.rename(new_file)
            time = datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
            log_message = f"{time} Moved {file.name} To {folder_name}/\n"
            print(log_message,end="")
            with open("history_of_files","a") as log:
                log.write(log_message)
            