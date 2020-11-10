import sys, os, shutil
from multiprocessing import Pool
from pdf2image import convert_from_path
from PIL import Image

def to_jpg(in_file, out_dir):
    name, ext = os.path.splitext(in_file)
    sid = os.path.basename(name).split("-")[1]
    out_file = os.path.join(out_dir, f"{sid}.jpg")

    if ext == ".pdf":
        images = convert_from_path(in_file)

        widths, heights = zip(*(img.size for img in images))
        width = max(widths)
        height = sum(heights)
        
        image = Image.new("RGB", (width, height))
        
        offset = 0
        for img in images:
            image.paste(img, (0, offset))
            offset += img.size[1]
        
        image.save(out_file, "JPEG")
    else:
        shutil.copyfile(in_file, out_file)

def main(argv):
    if len(argv) != 3:
        print("Usage: python3 quiz.py [in_dir] [out_dir]")
        return

    in_dir = argv[1]
    out_dir = argv[2]

    os.makedirs(out_dir, exist_ok=True)
    files = [ \
        (os.path.join(in_dir, f), out_dir) \
        for f in os.listdir(in_dir) \
    ]

    with Pool(8) as p:
        p.starmap(to_jpg, files)

if __name__ == "__main__":
    main(sys.argv)
