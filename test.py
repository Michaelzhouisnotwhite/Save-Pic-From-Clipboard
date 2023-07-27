from save_pic_from_clipboard import SaveClipBoardPic, parser_init


def test():
    SaveClipBoardPic(args=parser_init().parse_args([]))
    
    
if __name__ == "__main__":
    test()
