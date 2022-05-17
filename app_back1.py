import cvzone
import cv2
import numpy as np

from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.5, maxHands=1)
i = 0
while True:
    # Get image frame
    success, img = cap.read()

    # Find the hand and its landmarks
    hands,img = detector.findHands(img)
    a = "bbox"
    b = [hands_dict[a] for hands_dict in hands]
    b = np.array(b)
    if len(b) != 0:
        cropped_image = img[b[0][1]:b[0][1]+b[0][3], b[0][0]:b[0][0]+b[0][2]]
        image = cv2.imencode('.jpg', cropped_image)
        print(image[1])
        #cv2.imwrite('img'+str(i)+'.jpeg',cropped_image)
        i+=1
        im = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2GRAY)
        #print(b[0][0], ", ", b[0][1], ", ", b[0][2], ", ", b[0][3])  
    
    # Display
    cv2.imshow("Image", img) 
    cv2.waitKey(1)
