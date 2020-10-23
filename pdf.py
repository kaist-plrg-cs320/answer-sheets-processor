import fitz, sys, os, shutil
from multiprocessing import Pool

def extract(path, out_dir):
    print(path)

    name = os.path.basename(os.path.splitext(path)[0])
    doc = fitz.open(path)

    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            if img[3] <= 200:
                continue
            xref = img[0]
            out = "%s-%s-%s.png" % (name, i, xref)
            out_path = os.path.join(out_dir, out)
            pix = fitz.Pixmap(doc, xref)
            png = pix if pix.n - pix.alpha < 4 else fitz.Pixmap(fitz.csRGB, pix)
            png.writePNG(out_path)

def main(argv):
    if len(argv) != 3:
        print("Usage: python3 pdf.py [in_dir] [out_dir]")
        return

    shutil.rmtree(out_dir, ignore_errors=True)
    os.mkdir(out_dir)

    in_dir = argv[1]
    out_dir = argv[2]
    files = [ \
        (os.path.join(in_dir, f), out_dir) \
        for f in os.listdir(in_dir) \
        if f.endswith("pdf") \
    ]

    with Pool(8) as p:
        p.map(extract, files)

if __name__ == "__main__":
    main(sys.argv)
