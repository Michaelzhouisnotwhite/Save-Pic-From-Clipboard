from PIL import Image, ImageGrab
import sys
import os
import json
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", help="init the saving settings", required=False, action="store_true")
    parser.add_argument("-n", "--name", help="the saved pic name", required=False)
    parser.add_argument("-f", "--folder", help="the saved pic folder", required=False)
    parser.add_argument("--info", required=False, action="store_true", help="print settings")
    parser.add_argument("--type", required=False, help="set pic type", default='.png', choices=['.jpg', '.png'])
    args = parser.parse_args()
    return args


class SaveClipBoardPic():

    def __init__(self, args) -> None:
        self.save_folder_path = ""
        self.file_dict = dict()
        self.setting_file_path = "save-pic-settings.json"
        self.params = args
        self.check_parms()

    def check_parms(self):
        if (self.params.init):
            self.init_setting()
        else:
            self.load_settings()

        if (self.params.folder):
            self.change_folder(os.path.abspath(self.params.folder.strip()))

        if (self.params.type):
            self.change_type(self.params.type.strip())

        if (self.params.name):
            self.save(self.params.name.strip())
            
        if (self.params.info):
            self.show_settings()
    
    def show_settings(self):
        print("saved folder path: ",self.file_dict['save folder'])
        print("picture type: ",self.file_dict['pic type'])
    
    def save(self, file_name):
        im = ImageGrab.grabclipboard()
        if isinstance(im, Image.Image):
            print("image:size:%s, mode: %s" % (im.size, im.mode))
            try:
                im.save(os.path.join(self.file_dict["save folder"], file_name + self.file_dict["pic type"]))
                print("pic is saved in path:\"{}\"".format(
                    os.path.join(self.file_dict["save folder"], file_name + self.file_dict["pic type"])))
            except FileNotFoundError as e:
                print(e.strerror)
                print("use -i to init folder or use --folder to set another folder")
                sys.exit(-1)
        else:
            print("no pic in clipboard.")

    def get_save_folder(self):
        self.save_folder_path = self.file_dict["save folder"]
        return self.save_folder_path

    def init_setting(self):
        self.file_dict = {"save folder": os.path.abspath('.'), "pic type": ".png"}
        with open(self.setting_file_path, "w") as f:
            json.dump(self.file_dict, f)

    def load_settings(self):
        try:
            with open(self.setting_file_path, "r") as f:
                self.file_dict = json.load(f)

        except FileNotFoundError:
            print("save-pic-settings.json is not founded")
            print("use -i to init it")
            sys.exit(-1)

        try:
            folder_name, file_type = self.file_dict["save folder"], self.file_dict["pic type"]
        except KeyError:
            print("there is errors in settings.json, use -i to init it again")
            sys.exit(-1)

        if (not os.path.exists(folder_name)):
            print("save folder is not found")
            sys.exit(-1)

    def change_folder(self, folder_name: str):
        self.file_dict["save folder"] = folder_name
        with open(self.setting_file_path, "w") as f:
            json.dump(self.file_dict, f)

        self.load_settings()

    def change_type(self, tp: str):
        self.file_dict["pic type"] = tp
        with open(self.setting_file_path, "w") as f:
            json.dump(self.file_dict, f)

        self.load_settings()


if __name__ == "__main__":
    SaveClipBoardPic(args=get_args())