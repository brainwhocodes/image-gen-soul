"""Histogram palette measurement; no style presets or image generation."""
import argparse, json
from pathlib import Path
import numpy as np
from PIL import Image
from color_pipeline import load_srgb

def palette(image):
    """5-bit RGB histogram -> six weighted clusters; area shares cover all samples."""
    im=image.convert('RGBA'); im.thumbnail((256,256))
    a=np.asarray(im,dtype=np.float64).reshape(-1,4)
    a=a[a[:,3]>0]; rgb=a[:,:3]; weight=a[:,3]/255
    if not len(a): return {'colors':[], 'luminance': [0]*32, 'method':'transparent image'}
    bins=(rgb//8).astype(int)
    keys=bins[:,0]*1024+bins[:,1]*32+bins[:,2]
    ids,inv=np.unique(keys,return_inverse=True)
    counts=np.bincount(inv,weights=weight)
    means=np.stack([np.bincount(inv,weights=rgb[:,c]*weight)/counts for c in range(3)],axis=1)
    centers=[means[counts.argmax()]]
    for _ in range(min(5,len(means)-1)):
        dist=((means[:,None,:]-np.array(centers)[None,:,:])**2).sum(2).min(1)
        centers.append(means[(dist*np.sqrt(counts)).argmax()])
    centers=np.array(centers)
    for _ in range(15):
        labels=((means[:,None,:]-centers[None,:,:])**2).sum(2).argmin(1)
        for k in range(len(centers)):
            selected=labels==k
            if selected.any(): centers[k]=np.average(means[selected],axis=0,weights=counts[selected])
    area=np.bincount(labels,weights=counts,minlength=len(centers))
    colors=[{'hex':'#'+''.join(f'{int(round(c)):02x}' for c in centers[k]),'percent':round(float(area[k]/area.sum()*100),2)} for k in np.argsort(-area)]
    linear=np.where(rgb/255<=.04045,rgb/255/12.92,((rgb/255+.055)/1.055)**2.4)
    luminance=linear@np.array([.2126,.7152,.0722])
    hist=np.histogram(luminance,bins=32,range=(0,1),weights=weight)[0]
    return {'colors':colors,'luminance':[round(float(v/hist.sum()*100),3) for v in hist],'method':'5-bit sRGB histogram; 6 weighted RGB clusters; 256 px sample; alpha-weighted area shares. Luminance: 32 linear-light bins.'}

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Measure an alpha-weighted sRGB histogram palette')
    parser.add_argument('image', type=Path)
    parser.add_argument('--report', type=Path)
    args=parser.parse_args()
    rgb,alpha,meta=load_srgb(args.image)
    if alpha is not None: rgb.putalpha(alpha)
    result={'source':meta, **palette(rgb)}
    text=json.dumps(result,indent=2)
    if args.report:
        if args.report.exists(): raise SystemExit('Report already exists; choose a new path.')
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(text,encoding='utf-8')
    else: print(text)
