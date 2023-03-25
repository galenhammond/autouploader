import os
import config

def main():
  
  
  if not os.path.exists("./user_files/scheduled"):
    try:
      os.mkdir("./user_files/scheduled")
    except FileExistsError:
      #log error
      pass
    
    upload_file_paths = get_upload_file_paths(config.ROOT_FOLDER_PATH)
    for file in uploa      
    
  return

def get_upload_file_paths(path: str) -> list[str]:
  if not path:
    return []
  return [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".mp3")]
  
  
  
  
  
  
  
  
if __name__ == "__main__":
  main()