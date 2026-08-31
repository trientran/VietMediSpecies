#!/usr/bin/env python3
"""Figure 1: one specimen under the four preprocessing conditions.

Run this in terminal:

    python make_fig_preprocess_examples.py \
        --image /scratch/ttran72/datasets/viet-medi-species-2026/<speciesKey>/<img>.jpg \
        --out figures/fig_preprocess_examples.pdf

Optionally pass --image several times to stack multiple specimens as rows, which
reads better if we want to show that the Sobel collapse is not specific to one
photograph:

    python make_fig_preprocess_examples.py --image a.jpg --image b.jpg --image c.jpg

CesarPreprocess below is copied verbatim from Cell 8 of both training notebooks, so
the panels show exactly the transformation the models were trained on. Do not edit
it -- if it drifts from the notebook, the figure stops being evidence.

Requires: opencv-python, pillow, numpy, matplotlib.

Pick a specimen with visible venation and some colour variation. A flat green leaf
on a white herbarium sheet will understate how much the Sobel condition discards.
"""
import argparse
import os

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# --- verbatim from notebook Cell 8 -----------------------------------------
class CesarPreprocess:
    """Feature-highlighting preprocessing. PIL RGB in -> PIL RGB out."""

    def __init__(self, mode='baseline', downscale=1.0):
        self.mode, self.downscale = mode, downscale

    def __call__(self, img):
        arr = np.asarray(img.convert('RGB'))  # HWC RGB uint8
        if self.downscale and self.downscale != 1.0:
            h, w = arr.shape[:2]
            arr = cv2.resize(
                arr,
                (max(1, int(w * self.downscale)), max(1, int(h * self.downscale))),
                interpolation=cv2.INTER_AREA)
        if self.mode in ('clahe', 'clahe_sobel'):
            lab = cv2.cvtColor(arr, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            l = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l)
            arr = cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2RGB)
        if self.mode in ('sobel', 'clahe_sobel'):
            gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
            gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
            gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
            mag = cv2.magnitude(gx, gy)
            mag = np.clip(mag / (mag.max() + 1e-6) * 255.0, 0, 255).astype(np.uint8)
            if self.mode == 'sobel':
                arr = cv2.cvtColor(mag, cv2.COLOR_GRAY2RGB)          # pure edge map
            else:
                edges = cv2.cvtColor(mag, cv2.COLOR_GRAY2RGB)
                arr = cv2.addWeighted(arr, 0.7, edges, 0.3, 0.0)     # contrast + shape
        return Image.fromarray(arr)
# ---------------------------------------------------------------------------


MODES = [
    ('baseline',    '(a) Baseline'),
    ('clahe',       '(b) CLAHE'),
    ('sobel',       '(c) Sobel'),
    ('clahe_sobel', '(d) CLAHE+Sobel'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--image', action='append', required=True,
                    help='path to a dataset image; repeat for multiple rows')
    ap.add_argument('--out', default='figures/fig_preprocess_examples.pdf')
    ap.add_argument('--size', type=int, default=224,
                    help='centre-crop side length, matching the training resolution')
    args = ap.parse_args()

    rows = len(args.image)
    fig, axes = plt.subplots(rows, 4, figsize=(8.2, 2.15 * rows), squeeze=False)

    for r, path in enumerate(args.image):
        if not os.path.exists(path):
            raise SystemExit(f'image not found: {path}')
        im = Image.open(path).convert('RGB')

        # Resize the short side then centre-crop, mirroring the evaluation transform,
        # so the panels show what the network actually sees rather than the raw file.
        w, h = im.size
        scale = args.size / min(w, h)
        im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))),
                       Image.BILINEAR)
        w, h = im.size
        left, top = (w - args.size) // 2, (h - args.size) // 2
        im = im.crop((left, top, left + args.size, top + args.size))

        for c, (mode, label) in enumerate(MODES):
            ax = axes[r][c]
            ax.imshow(CesarPreprocess(mode=mode)(im))
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_linewidth(0.6)
                spine.set_color('#444444')
            if r == 0:
                ax.set_title(label, fontsize=9.5, pad=5)

    plt.tight_layout()
    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    plt.savefig(args.out, dpi=300, bbox_inches='tight')
    print('wrote', args.out)


if __name__ == '__main__':
    main()
