import argparse
import cv2
import numpy as np

parser=argparse.ArgumentParser(); parser.add_argument('--image',required=True); args=parser.parse_args()
img=cv2.imread(args.image,cv2.IMREAD_GRAYSCALE)
if img is None: raise SystemExit('Could not read image')
img=cv2.resize(img,(224,224)); img=cv2.GaussianBlur(img,(3,3),0); img=cv2.normalize(img,None,0,255,cv2.NORM_MINMAX)
# Simple image-quality/shape baseline. This is not a trained forgery classifier.
edges=cv2.Canny(img,50,150); ink_ratio=(img<180).mean(); edge_ratio=(edges>0).mean()
print(f'Preprocessed shape: {img.shape}')
print(f'Ink ratio: {ink_ratio:.4f}')
print(f'Edge ratio: {edge_ratio:.4f}')
print('Baseline complete. Train a CNN on genuine/forged labels for classification.')
