import sys
from qr import processQR
from pdf import processPDF
from zip import processZIP

def main(argv):
    if len(argv) != 5:
        print("Usage: python3 exam.py [in_dir] [img_dir] [out_dir] [secret_file]")
        return

    in_dir = argv[1]
    img_dir = argv[2]
    out_dir = argv[3]
    secret_file = argv[4]

    print("Processing PDFs")
    processPDF(in_dir, img_dir)

    print("Processing ZIPs")
    processZIP(in_dir, img_dir)

    print("Processing QRs")
    processQR(img_dir, out_dir, secret_file)

if __name__ == "__main__":
    main(sys.argv)
