from ultralytics import YOLO
import cv2

model = YOLO("yolo11n-pose.pt")

results = model("/Users/grantversluis/Adv Alg Hw/IMG_9073 2.JPG")
r = results[0]

overlay = r.plot()

cv2.imwrite("pose_overlay.jpg", overlay)
cv2.imshow("pose", overlay)

cv2.waitKey(0)
cv2.destroyAllWindows()