import sys, os, shutil
from pdf2image import convert_from_path
from multiprocessing import Pool

def extract(path, out_dir):
    print(path)

    name = os.path.basename(os.path.splitext(path)[0])
    images = convert_from_path(path)

    for i, img in enumerate(images):
        out = "%s-%s-%s.jpg" % (name, i)
        out_path = os.path.join(out_dir, out)
        image.save(out_path, "JPEG")

def process_pdf(in_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    files = [ \
        (os.path.join(in_dir, f), out_dir) \
        for f in os.listdir(in_dir) \
        if f.endswith("pdf") \
    ]

    with Pool(8) as p:
        p.starmap(extract, files)

def main(argv):
    if len(argv) != 3:
        print("Usage: python3 pdf.py [in_dir] [out_dir]")
        return

    in_dir = argv[1]
    out_dir = argv[2]
    process_pdf(in_dir, out_dir)

if __name__ == "__main__":
    main(sys.argv)
