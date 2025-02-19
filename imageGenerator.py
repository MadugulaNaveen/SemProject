import cv2
import numpy as np

# Load the image
image = cv2.imread("input.jpeg")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply median blur
gray_blurred = cv2.medianBlur(gray, 9)

# Detect edges using adaptive thresholding
edges = cv2.adaptiveThreshold(gray_blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

# Apply bilateral filter to smoothen colors
color = cv2.bilateralFilter(image, d=9, sigmaColor=250, sigmaSpace=200)

# Combine edges and color
cartoon = cv2.bitwise_and(color, color, mask=edges)

# Save and display result
cv2.imwrite("cartoon_image.jpg", cartoon)
cv2.imshow("Cartoon", cartoon)
cv2.waitKey(0)
cv2.destroyAllWindows()
