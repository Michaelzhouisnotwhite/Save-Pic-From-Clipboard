from PIL import Image, ImageGrab
import sys
import getopt
import os
import json
# os.chdir(os.path.dirname(__file__))


class SaveClipBoardPic:
    def __init__(self) -> None:
        if not os.path.exists("./settings.json"):
            sys.stdout("no file \"settings.json\", use -i to init")
            sys.exit(0)
        self.save_folder_path = ""
        self.file_dict = dict()

    def save(self, file_name):
        im = ImageGrab.grabclipboard()
        if isinstance(im, Image.Image):
            print("image:size:%s, mode: %s" % (im.size, im.mode))
            try:
                im.save(os.path.join(self.save_folder_path, file_name + self.file_dict["pic type"]))
            except FileNotFoundError as e:
                print(e.strerror)
                print("use -i to init folder or use --folder to set another folder")
                sys.exit(-1)
        elif im:
            for filename in im:
                try:
                    print("filename: %s" % filename)
                    im = Image.open(filename)
                except IOError:
                    pass  # ignore this file
                else:
                    print("ImageList: size : %s, mode: %s" % (im.size, im.mode))
                    print("Path: " + os.path.abspath(filename))
        else:
            print("no pic in clipboard.")

    def get_save_folder(self):
        self.save_folder_path = self.file_dict["save folder"]
        return self.save_folder_path

    def init_setting(self):
        self.file_dict = {"save folder": ".", "pic type": ".png"}
        with open("settings.json", "w") as f:
            json.dump(self.file_dict, f)

    def load_settings(self):
        with open("settings.json", "r") as f:
            self.file_dict = json.load(f)
        
        try:
            folder_name, file_type = self.file_dict["save folder"], self.file_dict["pic type"]
        except KeyError:
            print("there is errors in settings.json, use -i to init it again")
            sys.exit(-1)

    def change_folder(self, folder_name: str):
        self.file_dict["save folder"] = folder_name
        with open("settings.json", "w") as f:
            json.dump(self.file_dict, f)
            
    def change_type(self, tp: str):
        if tp not in [".jpg", ".png"]:
            print("Error: type only support \" .jpg\", \" .png\"")
            sys.exit(-1)
        self.file_dict["pic type"] = tp
        with open("settings.json", "w") as f:
            json.dump(self.file_dict, f)
    
    @staticmethod
    def help():
        print("help:")
        print(" -i init the settings")
        print(" -n the pic name(you don't need to enter the suffix like \".png\" it will use the \"pic type\" in the settings and add to the end of file name automatically)")
        print(" -h see this help list")
        print(" --folder change the saving folder")
        print(" --type change the pic save type")
        
    def run(self, argv):
        try:
            opts, args = getopt.getopt(argv, "hin:", ["name=", "help", "init", "folder=", "type="])
        except getopt.GetoptError:
            print("Use -h to see all args")
            sys.exit(-1)
        if opts == []:
            print("Use -h to see help")
            sys.exit(-1)
        for opt, arg in opts:
            if opt in ["-n", "--name"]:
                self.load_settings()
                self.get_save_folder()
                self.save(arg)
                
            elif opt in ["-i", "--init"]:
                self.init_setting()
            elif opt=="--folder":
                self.load_settings()
                self.change_folder(arg)
                
            elif opt == "--type":
                self.load_settings()
                self.change_type(arg)
            elif opt in ["--help", "-h"]:
                self.help()
                sys.exit(-1)
            elif opt is None:
                print("Use -h to see all args")
            else:
                print("Use -h to see all args")
                sys.exit(-1)


def get_name(argv):
    file_name = ""
    try:
        opts, args = getopt.getopt(argv, "hi:n:", ["name=", "help", "init="])
    except getopt.GetoptError:
        print("Use -n to Enter the pic name")
        sys.exit(-1)

    for opt, arg in opts:
        if opt in ["-n", "--name"]:
            file_name = arg
        else:
            print("Use -n to Enter the pic name")
            sys.exit(-1)
    if file_name == "":
        print("Use -n to Enter the pic name")
        sys.exit(-1)
    return file_name


if __name__ == "__main__":
    c = SaveClipBoardPic()
    c.run(sys.argv[1:])
