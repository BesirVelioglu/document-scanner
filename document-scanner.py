import cv2
import numpy as np
import utlis

########################################################################
webCamFeed = False  # Kameradan almak yerine resmi yüklemek için False yapıyoruz
pathImage = "C:/Sodec-staj-projects/document-scanner/document.jpg"  # İşlemek istediğiniz resmin yolu
cap = cv2.VideoCapture(1)
cap.set(10,160)
heightImg = 640
widthImg  = 480
########################################################################

utlis.initializeTrackbars()
count = 0

while True:
    if webCamFeed:
        success, img = cap.read()
    else:
        img = cv2.imread(pathImage)  # Resmi yüklüyoruz
    img = cv2.resize(img, (widthImg, heightImg))  # Resmi yeniden boyutlandırıyoruz
    imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8)  # Boş bir resim oluşturuyoruz (test/debug için)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Resmi gri tonlamaya çeviriyoruz
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # Gaussian Blur ekliyoruz
    thres = utlis.valTrackbars()  # Threshold değerlerini alıyoruz
    imgThreshold = cv2.Canny(imgBlur, thres[0], thres[1])  # Canny Blur uyguluyoruz
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)  # Dilate işlemi uyguluyoruz
    imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # Erosion işlemi uyguluyoruz

    ## TÜM KONTURLARI BULMA
    imgContours = img.copy()  # Görüntüyü kopyalıyoruz (görüntüleme amaçlı)
    imgBigContour = img.copy()  # Görüntüyü kopyalıyoruz (görüntüleme amaçlı)
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Tüm konturları buluyoruz
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)  # Tespit edilen tüm konturları çiziyoruz

    # EN BÜYÜK KONTURU BULMA
    biggest, maxArea = utlis.biggestContour(contours)  # En büyük konturu buluyoruz
    if biggest.size != 0:
        biggest = utlis.reorder(biggest)
        cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20)  # En büyük konturu çiziyoruz
        imgBigContour = utlis.drawRectangle(imgBigContour, biggest, 2)
        pts1 = np.float32(biggest)  # Warp için noktaları hazırlıyoruz
        pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # Warp için noktaları hazırlıyoruz
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

        # Her bir kenardan 20 piksel çıkarıyoruz
        imgWarpColored = imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
        imgWarpColored = cv2.resize(imgWarpColored, (widthImg, heightImg))

        # ADAPTİF THRESHOLD UYGULAMA
        imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
        imgAdaptiveThre = cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
        imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
        imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre, 3)

        # Görüntüleme için Resim Dizisi
        imageArray = ([img, imgGray, imgThreshold, imgContours],
                      [imgBigContour, imgWarpColored, imgWarpGray, imgAdaptiveThre])

    else:
        imageArray = ([img, imgGray, imgThreshold, imgContours],
                      [imgBlank, imgBlank, imgBlank, imgBlank])

    # Görüntüleme için Etiketler
    lables = [["Original", "Gray", "Threshold", "Contours"],
              ["Biggest Contour", "Warp Prespective", "Warp Gray", "Adaptive Threshold"]]

    stackedImage = utlis.stackImages(imageArray, 0.75, lables)
    cv2.imshow("Result", stackedImage)

    # 's' tuşuna basıldığında resmi kaydetme
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("Scanned/myImage" + str(count) + ".jpg", imgWarpColored)
        cv2.rectangle(stackedImage, ((int(stackedImage.shape[1] / 2) - 230), int(stackedImage.shape[0] / 2) + 50),
                      (1100, 350), (0, 255, 0), cv2.FILLED)
        cv2.putText(stackedImage, "Scan Saved", (int(stackedImage.shape[1] / 2) - 200, int(stackedImage.shape[0] / 2)),
                    cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 255), 5, cv2.LINE_AA)
        cv2.imshow('Result', stackedImage)
        cv2.waitKey(300)
        count += 1
