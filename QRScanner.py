import cv2
import numpy as np

# Load the image
img = cv2.imread('ig.png')

img = cv2.resize(img, (600, 600))

# Convert the image to grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
H, W = img.shape[:2]
gray = np.zeros((H, W), np.uint8)
for i in range(H):
    for j in range(W):
        gray[i, j] = np.clip(0.299 * img[i, j, 0] +
                             0.587 * img[i, j, 1] +
                             0.114 * img[i, j, 2], 0, 255)

# Apply a threshold to the image
# _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
threshold = 180
thresh = np.zeros((H, W), np.uint8)
for i in range(H):
    for j in range(W):
        a = gray.item(i, j)
        if a < threshold:
            b = 0
        else:
            b = 255
        thresh.itemset((i, j), b)

# Find the contours in the image
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Create an empty image to draw contours on
# contour_img = np.zeros((H, W), np.uint8)
contour_img = np.zeros(img.shape, dtype=np.uint8)

# Loop through the contours
for contour in contours:
    # Iterate through the points in the contour
    for i in range(len(contour)):
        # Get the current and next point
        current_point = contour[i][0]
        next_point = contour[(i + 1) % len(contour)][0]

        # Calculate the coordinates of the line between the current and next point
        x1, y1 = current_point[0], current_point[1]
        x2, y2 = next_point[0], next_point[1]

        # Draw the line segment pixel by pixel
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = -1 if x1 > x2 else 1
        sy = -1 if y1 > y2 else 1
        err = dx - dy

        while True:
            contour_img[y1, x1] = (0, 255, 0)  # Set pixel color to green

            if x1 == x2 and y1 == y2:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy


# Loop through the contours
for contour in contours:
    # Check if the contour is a QR code
    rect = cv2.minAreaRect(contour)
    if rect[1][0] > 50 and rect[1][1] > 50:
        box = cv2.boxPoints(rect)
        box = box.astype(int)
        cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
        x, y, w, h = cv2.boundingRect(contour)
        roi = gray[y:y+h, x:x+w]
        qrCodeDetector = cv2.QRCodeDetector()
        decodedText, points, _ = qrCodeDetector.detectAndDecode(roi)
        if points is not None:
            print("Decoded text:", decodedText)

# Display the image
cv2.imshow('Image', img)
cv2.imshow('Image-Binary', thresh)
cv2.imshow('Image-Gray', gray)
cv2.imshow('Image-contours', contour_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
