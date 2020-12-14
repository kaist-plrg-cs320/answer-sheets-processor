import os, sys, shutil
from PIL import Image

def ask_qnums():
    print("qnum(s): ", end="")
    qnums = input()
    qnums = [n.strip() for n in qnums.split(",")]
    return [n for n in qnums if n.isdecimal()]

def combine_images(images):
    widths, heights = zip(*(img.size for img in images))
    width = sum(widths)
    height = max(heights)
    
    image = Image.new("RGB", (width, height))
    
    offset = 0
    for img in images:
        image.paste(img, (offset, 0))
        offset += img.size[0]
    
    return image

def process_extra(dir):
    dirs = [
        os.path.join(dir, d) \
        for d in os.listdir(dir) \
        if len(d) == 8 and d.isdecimal()
    ]
    for d in dirs:
        files = os.listdir(d)
        extras = [
            os.path.join(d, f) \
            for f in files \
            if f.startswith("extra")
        ]
        extras.sort()
        for f in extras:
            img = Image.open(f)
            os.remove(f)
            img.show()
            for n in ask_qnums():
                cand = [f for f in files if f.startswith(n + ".")]
                new_path = os.path.join(d, n + ".jpg")
                if cand:
                    f0 = os.path.join(d, cand[0])
                    img0 = Image.open(f0)
                    os.remove(f0)
                    new_img = combine_images([img0, img])
                    new_img.save(new_path, "JPEG")
                else:
                    img.save(new_path, "JPEG")

def main(argv):
    if len(argv) != 2:
        print("Usage: python3 extra.py [dir]")
        return

    process_extra(argv[1])

if __name__ == "__main__":
    main(sys.argv)
