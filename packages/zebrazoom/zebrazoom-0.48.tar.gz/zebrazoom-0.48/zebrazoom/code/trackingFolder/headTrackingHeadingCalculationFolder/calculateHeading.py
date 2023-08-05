import cv2
import math
import numpy as np

from zebrazoom.code.trackingFolder.trackingFunctions import calculateAngle
from zebrazoom.code.trackingFolder.trackingFunctions import distBetweenThetas

def computeHeading(thresh1, x, y, headSize, hyperparameters):
  
  videoWidth  = hyperparameters["videoWidth"]
  videoHeight = hyperparameters["videoHeight"]
  
  x = x + int(headSize)
  y = y + int(headSize)
  
  paddedImage = np.zeros((len(thresh1) + 2 * int(headSize), len(thresh1[0]) + 2 * int(headSize)))
  paddedImage[:, :] = 255
  paddedImage[int(headSize):len(thresh1)+int(headSize), int(headSize):len(thresh1[0])+int(headSize)] = thresh1
  thresh1 = paddedImage
  
  thresh1 = thresh1.astype(np.uint8)

  ymin  = y - headSize
  ymax  = y + headSize
  xmin  = x - headSize
  xmax  = x + headSize
  
  img = thresh1[int(ymin):int(ymax), int(xmin):int(xmax)]
  
  img[0,:] = 255
  img[len(img)-1,:] = 255
  img[:,0] = 255
  img[:,len(img[0])-1] = 255
  
  y, x = np.nonzero(img)
  x = x - np.mean(x)
  y = y - np.mean(y)
  coords = np.vstack([x, y])
  cov = np.cov(coords)
  evals, evecs = np.linalg.eig(cov)
  sort_indices = np.argsort(evals)[::-1]
  x_v1, y_v1 = evecs[:, sort_indices[0]]  # Eigenvector with largest eigenvalue
  x_v2, y_v2 = evecs[:, sort_indices[1]]
  scale = 20
  theta = calculateAngle(0, 0, x_v1, y_v1)
  theta = (theta - math.pi/2) % (2 * math.pi)
  
  if hyperparameters["debugHeadingCalculation"]:
    img2 = img.copy()
    img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    cv2.line(img2, (int(len(img2[0])/2), int(len(img2)/2)), (int(len(img[0])/2 + 20 * math.cos(theta)), int(len(img)/2 + 20 * math.sin(theta))), (255,0,0), 1)
    cv2.imshow('imgForHeadingCalculation', img2)
    cv2.waitKey(0)
  
  return theta


def calculateHeading(x, y, i, thresh1, thresh2, takeTheHeadClosestToTheCenter, hyperparameters):

  nbList = hyperparameters["nbList"]
  expDecreaseFactor = hyperparameters["expDecreaseFactor"]
  firstFrame = hyperparameters["firstFrame"]
  lastFrame = hyperparameters["lastFrame"]
  minAreaBody = hyperparameters["minAreaBody"]
  maxAreaBody = hyperparameters["maxAreaBody"]
  headSize = hyperparameters["headSize"]
  debugTracking = hyperparameters["debugTracking"]
  headEmbeded = hyperparameters["headEmbeded"]
  
  if hyperparameters["debugHeadingCalculation"]:
    cv2.imshow('thresh1', thresh1)
    cv2.waitKey(0)
    cv2.imshow('thresh2', thresh2)
    cv2.waitKey(0)
  
  cx = 0
  cy = 0
  cxNew = 0
  cyNew = 0
  
  minAreaCur = minAreaBody
  maxAreaCur = maxAreaBody
  while (cx == 0) and (minAreaCur > -200):
    
    thresh1[0,:]                 = 255
    thresh1[len(thresh1)-1,:]    = 255
    thresh1[:,0]                 = 255
    thresh1[:,len(thresh1[0])-1] = 255
    
    contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
      area = cv2.contourArea(contour)
      if (area > minAreaCur) and (area < maxAreaCur):
        M = cv2.moments(contour)
        if takeTheHeadClosestToTheCenter == 0:
          if M['m00']:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
          else:
            cx = 0
            cy = 0
        else:
          if M['m00']:
            cxNew = int(M['m10']/M['m00'])
            cyNew = int(M['m01']/M['m00'])
          else:
            cx = 0
            cy = 0
          
          distToCenterNew = math.sqrt((cxNew-x)**2 + (cyNew-y)**2)
          distToCenter    = math.sqrt((cx-x)**2    + (cy-y)**2)
          # print("distToCenter:",distToCenter," ; distToCenterNew:",distToCenterNew)
          if distToCenterNew < distToCenter:
            cx = cxNew
            cy = cyNew
            # print("change realized, new center is:", cx, cy)
    minAreaCur = minAreaCur - 100
    maxAreaCur = maxAreaCur + 100
  
  
  heading = computeHeading(thresh2, x, y, headSize, hyperparameters)
  lastFirstTheta = calculateAngle(x, y, cx, cy)
  
  headingApproximate = lastFirstTheta
  headingPreciseOpt1 = heading
  headingPreciseOpt2 = (heading + math.pi) % (2*math.pi)
  diffAngle1 = distBetweenThetas(headingApproximate, headingPreciseOpt1)
  diffAngle2 = distBetweenThetas(headingApproximate, headingPreciseOpt2)
  if (diffAngle1 > diffAngle2):
    heading = headingPreciseOpt1
  else:
    heading = headingPreciseOpt2
  
  return [heading, lastFirstTheta]


def calculateHeadingSimple(x, y, thresh2, hyperparameters):
  
  headSize = hyperparameters["headSize"]
  heading = computeHeading(thresh2, x, y, headSize, hyperparameters)
  
  return heading
