import cv2

# Baca citra
image = cv2.imread("ig.png")

# Dapatkan ukuran citra
height, width, _ = image.shape

# Hitung titik tengah koordinat piksel
x_center = width // 2
y_center = height // 2

# Dapatkan nilai RGB pada titik tengah
b, g, r = image[y_center, x_center]

# Tampilkan titik tengah dan nilai RGB
print("Titik tengah koordinat piksel:")
print("X: ", x_center)
print("Y: ", y_center)
print("Nilai RGB pada titik tengah:")
print("R: ", r)
print("G: ", g)
print("B: ", b)
