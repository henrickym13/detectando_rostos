import cv2

# Carrega modelo
foto = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Carrega imagem
img = cv2.imread('caminho da imagem')

# Converte para scala em cinza
cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detecta rostos
rosto = foto.detectMultiScale(gray, 1.1, 4)

# Desenha retangulo no rosto detectado
for (x, y, w, h) in rosto:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Mostra resultado
cv2.imshow('img', img)
cv2.waitKey()
