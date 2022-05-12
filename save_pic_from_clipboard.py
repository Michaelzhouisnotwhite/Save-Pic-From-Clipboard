from PIL import Image, ImageGrab
import sys
import os
import json
import argparse
import settings
from utils import md5_hash


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", help="init the saving settings", required=False, action="store_true")
    parser.add_argument("-n", "--name", help="the saved pic name", required=False)
    parser.add_argument("-f", "--folder", help="the saved pic folder", required=False)
    parser.add_argument("--info", required=False, action="store_true", help="print settings")
    parser.add_argument("-t", "--type", required=False, help="set pic type", default='.png', choices=['.jpg', '.png'])
    return parser.parse_args()


class Config:
    class InitError(Exception):
        def __init__(self, *args) -> None:
            super().__init__(*args)

    CONFIG_INIT = {'id': 0,
                   "save folder": os.path.abspath('.'), "pic type": ".png",
                   "hash": md5_hash(os.path.abspath('.'))}

    def __init__(self) -> None:
        self.config_file_path = settings.CONFIG_FILE
        self.config_file = []
        self.config = self.CONFIG_INIT
        self.cur_config_idx = -1
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'w') as f:
                json.dump(self.config_file, f, indent=4, ensure_ascii=False)

        with open(self.config_file_path, 'r') as f:
            self.config_file = json.load(f)

    def get_cur_config(self, folder_name):
        hash_res = md5_hash(folder_name)

        for idx, config in enumerate(self.config_file):
            if config['hash'] == hash_res:
                self.cur_config_idx = idx
                self.config = config
                return True

        return False

    def change_type(self, tp: str):
        self.config['pic type'] = tp

    def change_save_path(self, path: str):
        if os.path.isabs(path):
            self.config['save folder'] = os.path.join(os.path.abspath('.'), path)
        else:
            self.config['save folder'] = path

    def delete_config(self, idx):
        for config in self.config_file:
            if idx == config['idx']:
                self.config_file.remove(config)
                break

    def save_cur_config(self):
        if len(self.config_file) > 0:
            if self.cur_config_idx == -1:
                self.config['id'] = self.config_file[-1]['id'] + 1
                self.config_file.append(self.config)
                self.cur_config_idx = len(self.config_file)  - 1
                
            else:
                self.config_file[self.cur_config_idx] = self.config

        else:
            self.config_file.append(self.config)
            self.cur_config_idx = 0

    def init(self):
        if self.cur_config_idx != -1:
            print("You have init this folder. Are you sure to init again? (Y/N)", end='')
            choice = str(input())
            if choice in ['Y', 'y']:
                self.config = self.CONFIG_INIT

            elif choice in ['N', 'n']:
                pass

            else:
                print("Wrong Choices")
                sys.exit(-1)

    def save_config(self):
        with open(self.config_file_path, 'w') as f:
            json.dump(self.config_file, f, indent=4, ensure_ascii=False)


class SaveClipBoardPic():
    def __init__(self, args) -> None:
        self.config = Config()

        self.cur_path = os.getcwd()
        if settings.DEBUG:
            print(os.getcwd())
            print(os.path.abspath('.'))
            print(md5_hash(self.cur_path))
        self.config.get_cur_config(self.cur_path)
        self.params = args
        self.check_parms()

    def check_parms(self):
        if (self.params.init):
            self.init_setting()

        if (self.params.folder):
            self.change_folder(os.path.abspath(self.params.folder.strip()))

        if (self.params.type):
            self.change_type(self.params.type.strip())

        if (self.params.name):
            self.save(self.params.name.strip())

        if (self.params.info):
            self.show_settings()

    def show_settings(self):
        print("saved folder path: ", self.config.config['save folder'])
        print("picture type: ", self.config.config['pic type'])

    def save(self, file_name):
        im = ImageGrab.grabclipboard()
        file_dict = self.config.config
        if isinstance(im, Image.Image):
            print("image:size:%s, mode: %s" % (im.size, im.mode))
            try:
                im.save(os.path.join(file_dict["save folder"], file_name + file_dict["pic type"]))
                print("pic is saved in path:\"{}\"".format(
                    os.path.join(file_dict["save folder"], file_name + file_dict["pic type"])))
            except FileNotFoundError as e:
                print(e.strerror)
                print("use -i to init folder or use --folder to set another folder")
                sys.exit(-1)
        else:
            print("no pic in clipboard.")
        
        self.config.save_cur_config()
        self.config.save_config()

    def init_setting(self):
        self.config.init()
        self.config.save_cur_config()
        self.config.save_config()

    def change_folder(self, folder_name: str):
        self.config.change_save_path(folder_name)
        self.config.save_cur_config()
        self.config.save_config()

    def change_type(self, tp: str):
        self.config.change_type(tp)
        self.config.save_cur_config()
        self.config.save_config()


if __name__ == "__main__":
    SaveClipBoardPic(args=get_args())
