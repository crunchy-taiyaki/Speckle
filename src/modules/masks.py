import numpy as np

def ring_mask(img, r1, r2):
    H, W = img.shape
    x, y = np.meshgrid(np.arange(W), np.arange(H))
    d2 = (x - 256)**2 + (y - 256)**2
    mask = d2 < (r1)**2
    mask1 = d2 > (r2)**2
    img_masked_ring = np.copy(img)
    img_masked_ring = np.ma.array(img_masked_ring, mask = mask)
    img_masked_ring = np.ma.array(img_masked_ring, mask = mask1)
    return img_masked_ring

