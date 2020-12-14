import os, sys, shutil
from PIL import Image

def ask_id():
    print("id: ", end="")
    id = input()
    if len(id) == 8 and id.isdecimal():
        return id
    else:
        return ask_id()

def ask_page():
    print("page: ", end="")
    page = input()
    if page.isdecimal() or page.startswith("extra") and page[5:].isdecimal():
        return page
    else:
        return ask_page()

def process_unknown(dir):
    udir = os.path.join(dir, "unknowns")
    files = os.listdir(udir)
    files.sort()

    for f in files:
        path = os.path.join(udir, f)
        img = Image.open(path)
        img.show()
        id = ask_id()
        page = ask_page()
        ext = os.path.splitext(f)[1]
        new_path = os.path.join(dir, id, page + ext)
        shutil.move(path, new_path)

def main(argv):
    if len(argv) != 2:
        print("Usage: python3 unknown.py [dir]")
        return

    process_unknown(argv[1])

if __name__ == "__main__":
    main(sys.argv)
