import ray
import cv2
import numpy as np
import time

from santak.ray_setup import id2contour

@ray.remote
def distance(cnt1, cnt2):
    try:
        return cv2.createShapeContextDistanceExtractor().computeDistance(cnt1, cnt2)
    except cv2.error as e:
        # print("WARNING: character ID {} suffered error".format(char_id))
        return np.inf

def match(img, n_matches=10):
    # img = img[0:300, 0:300]  # crop to 300x300
    # perform Canny edge detection
    edges = cv2.Canny(img, 300, 300)
    # get contour of image
    cnt_target, _ = cv2.findContours(
        edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    if len(cnt_target) == 0:
        return []

    stacked = np.vstack(cnt_target)
    eps = cv2.arcLength(stacked, True) * 0.5
    approx = cv2.approxPolyDP(stacked, eps, True)
    approx_id = ray.put(approx)

    keys, contours = zip(*id2contour.items())
    print("Starting Ray execution")
    now = time.time()
    distances_ids = [
        distance.remote(approx_id, contour_id) for contour_id in contours
    ]
    results = ray.get(distances_ids)

    print(f"Ray execution done, took: {time.time() - now} sec ")

    distances = {key: res for key, res in zip(keys, results)}

    ranked_shapes = sorted(distances, key=distances.get)
    closest = ranked_shapes[:n_matches]

    return closest