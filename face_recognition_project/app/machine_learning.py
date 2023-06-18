# Import Libraries
import numpy as np
import cv2
import pickle
import os
from django.conf import settings

STATIC_DIR = settings.STATIC_DIR


# ### Load Models
# - Face detection
# - Feature extraction
# - Face recognition
# - Face emotion recognition

# Face Detection
face_detector_model = cv2.dnn.readNetFromCaffe(os.path.join(STATIC_DIR, "models/deploy.prototxt.txt"),
                                              os.path.join(STATIC_DIR, "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"))

# Feature Extraction
face_feature_model = cv2.dnn.readNetFromTorch(os.path.join(STATIC_DIR, "models/openface.nn4.small2.v1.t7"))

# Face Recognition - best_model_face_person.pkl
face_recgonition_model = pickle.load(open(os.path.join(STATIC_DIR, "models/Big_DataSet_best_model_face_person_2.pkl"), mode="rb"))


# ### Pipeline model
def pipeline_model(path):    
    img = cv2.imread(path)
    image = img.copy()
    h, w = img.shape[:2]

    # face detection
    img_blob = cv2.dnn.blobFromImage(img, 1, (300, 300), (1.4, 177, 123), swapRB=False, crop=False)
    face_detector_model.setInput(img_blob)
    detections = face_detector_model.forward()
    
    # machine learning result
    machinelearning_result = dict(count = [],
                                  face_detect_confidence = [],
                                 face_name = [],
                                 face_name_score = [])
    count = 0
    if len(detections) > 0:
        for i, confidence in enumerate(detections[0, 0, :, 2]):
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h]) 
                startx, starty, endx, endy = box.astype(int)

                # feature extraction
                face_cropped = img[starty:endy, startx:endx]
                face_blob = cv2.dnn.blobFromImage(face_cropped, 1/255, (96, 96), (0, 0, 0), swapRB=True, crop=True)
                face_feature_model.setInput(face_blob)
                vectors = face_feature_model.forward()

                # predict face name
                face_name = face_recgonition_model.predict(vectors)[0]
                face_score = face_recgonition_model.predict_proba(vectors).max()

                # draw face box
                cv2.rectangle(image, (startx, starty), (endx, endy), (0, 255, 0), 3)
                # put text
                text = "{} : {:.2f} %".format(face_name, confidence*100)
                cv2.putText(image, text, (startx, starty-10), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2)
                
                # append to machine learning result dict
                count += 1
                machinelearning_result['count'].append(count)
                machinelearning_result['face_detect_confidence'].append(confidence)
                machinelearning_result['face_name'].append(face_name)
                machinelearning_result['face_name_score'].append(face_score)
                
                
                # save Processed image and cropped image
                cv2.imwrite(os.path.join(settings.MEDIA_ROOT, "ml_output/processed.jpg"), image)
                cv2.imwrite(os.path.join(settings.MEDIA_ROOT, "ml_output/face_cropped_image_{}.jpg".format(count)), face_cropped)
                print("Images saved in media/ml_output")
                
                
                
    return machinelearning_result