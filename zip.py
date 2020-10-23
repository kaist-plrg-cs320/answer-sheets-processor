import zipfile, sys, shutil, os, glob
from multiprocessing import Pool

tmp_dir = ".zip.tmp"

def unzip(path):
    print(path)

    out = os.path.basename(os.path.splitext(path)[0])
    out_path = os.path.join(tmp_dir, out)
    zf = zipfile.ZipFile(path)
    zf.extractall(out_path)
    zf.close()

def processZIP(in_dir, out_dir):
    shutil.rmtree(tmp_dir, ignore_errors=True)
    os.mkdir(tmp_dir)
    files = [ \
        os.path.join(in_dir, f) \
        for f in os.listdir(in_dir) \
        if f.endswith("zip") \
    ]

    with Pool(8) as p:
        p.map(unzip, files)

    os.makedirs(out_dir, exist_ok=True)
    files = glob.glob(os.path.join(tmp_dir + "/**/*"), recursive=True)
    for i, f in enumerate(files):
        if not os.path.isdir(f):
            name = "%s-%s" % (i, os.path.basename(f))
            shutil.move(f, os.path.join(out_dir, name))

    shutil.rmtree(tmp_dir, ignore_errors=True)

def main(argv):
    if len(argv) != 3:
        print("Usage: python3 zip.py [in_dir] [out_dir]")
        return

    in_dir = argv[1]
    out_dir = argv[2]
    processZIP(in_dir, out_dir)

if __name__ == "__main__":
    main(sys.argv)
