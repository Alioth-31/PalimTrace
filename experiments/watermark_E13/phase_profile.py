"""Recompute the E13 4x4 phase-orbit statistics from source images.
The recorded study used jpeg-js/UPNG.js decoders; Pillow may differ slightly.
"""
import argparse, csv, hashlib, io, json, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent


def energy(a, b, c, d):
    return ((a-b+c-d)/2)**2 + ((a+b-c-d)/2)**2 + ((a-b-c+d)/2)**2


def profile(img):
    h, w = img.shape
    if h % 4 or w % 4:
        raise ValueError('Require dimensions divisible by four')
    result = []
    for dy in range(4):
        for dx in range(4):
            a = np.roll(img, (-dy, -dx), axis=(0, 1))
            m, e = [], []
            for by in range(2):
                for bx in range(2):
                    q = a[2*by::4, 2*bx::4]
                    r = a[2*by::4, 2*bx+1::4]
                    s = a[2*by+1::4, 2*bx::4]
                    t = a[2*by+1::4, 2*bx+1::4]
                    m.append((q+r+s+t)/4)
                    e.append(energy(q,r,s,t))
            x = np.log1p(energy(*m)); y = np.log1p(sum(e)/4)
            bins = np.clip(np.floor(sum(m)/256), 0, 3).astype(int)
            cov = vx = vy = 0.
            for k in range(4):
                xx, yy = x[bins == k], y[bins == k]
                if xx.size:
                    xx, yy = xx-xx.mean(), yy-yy.mean()
                    cov += np.sum(xx*yy); vx += np.sum(xx**2); vy += np.sum(yy**2)
            result.append(cov/np.sqrt(vx*vy+1e-30))
    return np.array(result).reshape(4,4)


def stats(a):
    h,w = a.shape
    h,w = 4*((h-8)//4), 4*((w-8)//4)
    if min(h,w)<64:
        raise ValueError('Image too small')
    p = profile(a[:h,:w]); q = profile(np.roll(a[:h,:w],(-1,-1),(0,1)))
    r = profile(a[1:h+1,1:w+1])
    return dict(crop=[w,h],profile=p.ravel().tolist(),mean=float(p.mean()),phaseRange=float(np.ptp(p)),circularMeanErr=float(abs(p.mean()-q.mean())),circularRangeErr=float(abs(np.ptp(p)-np.ptp(q))),cropShiftSingleDiff=float(abs(p[0,0]-r[0,0])),cropShiftMeanDiff=float(abs(p.mean()-r.mean())),cropShiftRangeDiff=float(abs(np.ptp(p)-np.ptp(r))))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--download',action='store_true'); ap.add_argument('--input',type=Path,default=ROOT/'images'); ap.add_argument('--output',type=Path,default=ROOT/'recomputed.json'); args=ap.parse_args()
    args.input.mkdir(parents=True,exist_ok=True); out=[]
    for row in csv.DictReader((ROOT/'sources.csv').open(encoding='utf-8')):
        path=args.input/row['local_file']
        try:
            if not path.exists() and args.download:
                url=f"https://raw.githubusercontent.com/{row['repo']}/{row['branch']}/{row['path']}"
                with urllib.request.urlopen(url, timeout=60) as r:
                    path.write_bytes(r.read())
            raw=path.read_bytes(); sha=hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
            if sha!=row['blob_sha']:
                raise ValueError(f'Git blob hash mismatch: {sha}')
            with Image.open(io.BytesIO(raw)) as im:
                a=np.asarray(im.convert('RGB'),dtype=np.float64)@np.array([.299,.587,.114])
            out.append(dict(label=row['label'],blob_sha=sha,native=[a.shape[1],a.shape[0]],**stats(a)))
        except Exception as e:
            out.append(dict(label=row['label'],error=str(e)))
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f"Completed {sum('error' not in r for r in out)}/{len(out)} images. {args.output}")

if __name__=='__main__':main()
