import sys, shutil
from qr import process_qr
from pdf import process_pdf
from zip import process_zip
from unknown import process_unknown
from extra import process_extra

def main(argv):
    if len(argv) != 5:
        print("Usage: python3 exam.py [in_dir] [img_dir] [out_dir] [secret_file]")
        return

    in_dir = argv[1]
    img_dir = argv[2]
    out_dir = argv[3]
    secret_file = argv[4]

    print("Processing PDFs")
    process_pdf(in_dir, img_dir)

    print("Processing ZIPs")
    process_zip(in_dir, img_dir)

    print("Processing QRs")
    process_qr(img_dir, out_dir, secret_file)

    print("Processing unknown files")
    shutil.copytree(out_dir, out_dir + ".bk1")
    process_unknown(out_dir)

    print("Processing extra files")
    shutil.copytree(out_dir, out_dir + ".bk2")
    process_extra(out_dir)

if __name__ == "__main__":
    main(sys.argv)
