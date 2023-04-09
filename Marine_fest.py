from io import TextIOWrapper
from msilib.schema import Class, File
from os import path, walk
from sys import argv, exit
from argparse import ArgumentParser


def header():
  print("  __  __            _              ______        _ ")  
  print(" |  \/  |          (_)            |  ____|      | |  ")
  print(" | \  / | __ _ _ __ _ _ __   ___  | |__ ___  ___| |_  ")
  print(" | |\/| |/ _` | '__| | '_ \ / _ \ |  __/ _ \/ __| __| ")
  print(" | |  | | (_| | |  | | | | |  __/ | | |  __/\__ \ |_  ")
  print(" |_|  |_|\__,_|_|  |_|_| |_|\___| |_|  \___||___/\__| ")
  print("                             ______                  ")
  print("                            |______|                 ")
  print("")

class M_Entry:
    '''
    Class Name: M_Entry
    Attributes:
      - name | Name of the animation
      - butt_min | Minimum butthurt level
      - butt_max | Maximum butthurt level
      - level_min | Minimum level
      - level_max | Maximum level
    
    '''
    def __init__(self, name):
        self.name = name
        self.butt_min = 0
        self.butt_max = 14
        self.level_min = 1
        self.level_max = 3
        self.weight = 3
        print("\n=========================================")
        print("Lets set-up " + self.name)
        print("=========================================")
        self.set_butt_min()
        self.set_butt_max()
        self.set_level_min()
        self.set_level_max()
        self.set_weight()
        print("=========================================\n")
    
    def set_butt_min(self):
        loop=True
        while(loop):
            try:
                val = int(input("Minimum butthurt required[0-14]: "))
                if val < 0 or val > 14:
                    raise ValueError
            except ValueError:
                print("...uh, let's try that again. Remember, 0-14...")
                continue
            print("Setting butt_min to " + str(val))
            self.butt_min = int(val)
            loop=False
    
    def set_butt_max(self):
        loop=True
        while(loop):
            try:
                val = int(input("Maximum butthurt required["+str(self.butt_min)+"-14]: "))
                if val < self.butt_min or val > 14:
                    raise ValueError
            except ValueError:
                print("...uh, let's try that again. Remember, "+str(self.butt_min)+"-14...")
                continue
            print("Setting butt_max to " + str(val))
            self.butt_max = int(val)
            loop=False
    
    def set_level_min(self):
        loop=True
        while(loop):
            try:
                val = int(input("Minimum level required[1-3]: "))
                if val < 1 or val > 3:
                    raise ValueError
            except ValueError:
                print("...uh, let's try that again. Remember, 1-3...")
                continue
            print("Setting level_min to " + str(val))
            self.level_min = int(val)
            loop=False

    def set_level_max(self):
        loop=True
        while(loop):
            try:
                val = int(input("Maximum level required["+str(self.level_min)+"-3]: "))
                if val < self.level_min or val > 3:
                    raise ValueError
            except ValueError:
                print("...uh, let's try that again. Remember, "+str(self.level_min)+"-3...")
                continue
            print("Setting level_max to " + str(val))
            self.level_max = int(val)
            loop=False

    def set_weight(self):
        loop=True
        while(loop):
            try:
                val = int(input("Animation Weight[Higher = More like to be chosen]: "))
            except ValueError:
                print("...uh, let's try that again. Remember, gotta be a integer...")
                continue
            print("Setting weight to " + str(val))
            self.weight = int(val)
            loop=False

    def get_name(self):
        return self.name

    def get_butt_min(self):
        return self.butt_min
    
    def get_butt_max(self):
        return self.butt_max
    
    def get_level_min(self):
        return self.level_min
    
    def get_level_max(self):
        return self.level_max

    def get_weight(self):
        return self.weight
    
    def export_text(self, file: TextIOWrapper):

        print("Exporting " + self.name)
        lines = {
            'Name' : self.name, 
            'Min butthurt' : self.butt_min, 
            'Max butthurt' : self.butt_max, 
            'Min level' : self.level_min, 
            'Max level' : self.level_max,
            'Weight' : self.weight
            }
        file.write("\n")
        file.write("\n".join([k+": " +str(v) for k,v in lines.items()]))
        file.write("\n")





def retrieve_Dir_Names(directory: str):
    '''
    Function name: retrieve_Dir_Names
    Args:
      - directory(String) - literal string of path to directory where animations are, usually assets\dolphin\external

    This function returns all directory names in the provided directory, as these correspond to manifest entry names.
    If no directories are found, a FileNotFoundError is raised.
    '''
    dirs = [filename for filename in next(walk(directory))[1] if not filename[0] == '.']
    if len(dirs) == 0:
        print("No directories were found. Are you sure you gave the right place?")
        raise FileNotFoundError
    return dirs

def compare_Animations(directories: list[str], existing_Entries: list[str]):
    '''
    Function name: compare_Animations
    Args: 
      - directories(List[String]) - List containing Strings of directory names in assets\dolphin\external
      - existing_Entried(List[String]) - List containing Strings of names for entries in existing manifest.txt

    This function simply returns a list of directories that are not already in the manifest file, unless existing_Entries is empty, then it just returns directories back...
    '''
    if len(existing_Entries) == 0:
        return directories
    manifest_List = [name for name in directories if name not in existing_Entries]
    return manifest_List

def read_existing(manifest_dir: str):
    '''
    Function name: read_existing
    Args: 
      - manifest_dir(String) - Literal String of path to dir containing manifest.txt, usually assets\dolphin\external

    This function checks for an existing manifest.txt. If it exists, the names of existing entries are collected into a list and returned.
    '''
    manifest_File = manifest_dir + r'\manifest.txt'
    existing_Entry = []
    print("\nChecking for existing manifest.txt")
    if not path.isfile(manifest_File):
        print("\nNo manifest.txt exists here, creating it for you <3...")
        with open(manifest_File, 'a') as f:
            f.write("\n".join(["Filetype: Flipper Animation Manifest","Version: 1",""]))
            f.close()
        return existing_Entry
    with open(manifest_File,"r") as m:
        for line in m:
            if line.strip() == "":
                continue
            line_key = line.split(":")[0]
            line_val = line.split(":")[1].strip()
            if line_key == "Name":
                existing_Entry.append(line_val)
        m.close()
    return existing_Entry

def main(args):
    header()
    prs = ArgumentParser(description='Creates Version 1 manifest.txt for flipper firmware animations.')
    prs.add_argument('-d', '--dir', nargs='?', metavar='<PATH>', help="Path to the directory containing all the animations you wish to use", default='.\\')
    args = prs.parse_args()
    root_Working_Dir = args.dir

    try:
        dir_List = retrieve_Dir_Names(root_Working_Dir)
        existing = read_existing(root_Working_Dir)
        checked = compare_Animations(dir_List, existing)
        if len(checked) == 0:
            print("There's no animations to add.")
            exit(0)
        manifest_arr = [M_Entry(name) for name in checked]
        with open(root_Working_Dir+ r'\manifest.txt', 'a') as f:
            for entry in manifest_arr:
                entry.export_text(f)
            f.close()
        print("Manifest created!")
    except FileNotFoundError:
        exit(1)

if __name__ == "__main__":
    main(argv)



