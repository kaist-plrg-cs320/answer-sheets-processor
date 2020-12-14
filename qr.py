from pyzbar.pyzbar import decode
from multiprocessing import Pool
from Crypto.Cipher import AES
import cv2, os, sys, base64, re, shutil

class Answer:
    def __init__(self, s):
        arr = s.split("-")
        self.year = arr[0]
        self.semester = arr[1]
        self.exam = arr[2]
        self.sid = arr[3]
        self.question = arr[4]

    def __str__(self):
        return "Answer(%s, %s)" % (self.sid, self.question)

def decrypt(encrypted, key):
    s = base64.b64decode(encrypted)
    cipher = AES.new(key, AES.MODE_CBC, key)
    return re.sub("[^a-zA-Z0-9\-]", "", cipher.decrypt(s).decode('utf-8'))

def decode_qr(path, key):
    try:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        adapted = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY, 101, 2)
        decoded = decode(adapted)
        answer = Answer(decrypt(decoded[0].data, key)) if decoded else None
    except:
        answer = None
    return path, answer

def process_qr(in_dir, out_dir, secret_file):
    f = open(secret_file)
    key = f.readline().strip()
    f.close()
    files = [(os.path.join(in_dir, f), key) for f in os.listdir(in_dir)]

    with Pool(8) as p:
        results = p.starmap(decode_qr, files)

    def answers_of(sid):
        return [ \
            (path, answer.question) \
            for (path, answer) in results \
            if answer and answer.sid == sid
        ]

    sids = [answer.sid for (_, answer) in results if answer]
    answers_dict = { sid: answers_of(sid) for sid in sids }

    os.makedirs(out_dir, exist_ok=True)
    for sid, answers in answers_dict.items():
        s_dir = os.path.join(out_dir, sid)
        os.makedirs(s_dir, exist_ok=True)
        for src, question in answers:
            ext = os.path.splitext(src)[1]
            dst = os.path.join(s_dir, question + ext)
            shutil.copyfile(src, dst)

    unknowns = [path for (path, answer) in results if not answer]
    u_dir = os.path.join(out_dir, "unknowns")
    os.makedirs(u_dir, exist_ok=True)
    for i, src in enumerate(unknowns):
        ext = os.path.splitext(src)[1]
        dst = os.path.join(u_dir, str(i) + ext)
        shutil.copyfile(src, dst)

def main(argv):
    if len(argv) != 4:
        print("Usage: python3 qr.py [in_dir] [out_dir] [secret_file]")
        return

    in_dir = argv[1]
    out_dir = argv[2]
    secret_file = argv[3]
    process_qr(in_dir, out_dir, secret_file)

if __name__ == "__main__":
    main(sys.argv)
