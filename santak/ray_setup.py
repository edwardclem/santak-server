import pickle as pkl
import ray
import numpy as np
import cv2
from flask import session

# probably want to do this separately and initialize ray in a separate
# process/container than the Flask app. Only problem is how to 
# track which objects get loaded into the Ray shared memory instance? 
# that seems like it could be an okay application of a "config" module, 
# but that kind of state tracking seems iffy in a Flask app. 

def setup_ray():
    if not ray.is_initialized():
        ray.init()

def setup_prototypes(fname, eps_frac=0.5):
    with open(fname, "rb") as f:
        proto_data = pkl.load(f)
    id2img = proto_data["id2img"]
    id2allcontour = proto_data["id2contour"]

    # load all prototype contours into Ray shared memory
    id2contour = {}
    for key, contours in id2allcontour.items():
        stacked = np.vstack(contours)
        eps = cv2.arcLength(stacked, True) * eps_frac
        approx = cv2.approxPolyDP(stacked, eps, True)
        id2contour[key] = ray.put(approx)

    return id2img, id2contour


setup_ray()

id2img, id2contour = setup_prototypes("data/prototypes/proto_50")

    

    
