import cv2
import detectMask
import main

# global variable for writing files
global index
index = 1


# function to detect frontal faces
def detectFrontalFaces(image):
    # get cascadeClassifier
    face_cascade = cv2.CascadeClassifier("../faceDetect/venv/Lib/site-packages" +
                                         "/cv2/data/haarcascade_frontalface_default.xml")

    # change the color to gray scaled
    if image.ndim == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # detect face
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    result = []

    # write into result
    for (x, y, width, height) in faces:
        result.append((x, y, x + width, y + height))

    return result


# function to detect right profile faces
def detectRightProfileFace(image):
    # get cascadeClassifier
    face_cascade = cv2.CascadeClassifier("./venv/Lib/site-packages" +
                                         "/cv2/data/haarcascade_profileface.xml")

    # change the color to gray scaled
    if image.ndim == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # detect face
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    result = []

    # write into result
    for (x, y, width, height) in faces:
        result.append((x, y, x + width, y + height))

    return result


# function to detect left profile faces
def detectLeftProfileFace(image):
    # flip the image
    image_flip = cv2.flip(image, 180)
    # get cascadeClassifier
    face_cascade = cv2.CascadeClassifier("./venv/Lib/site-packages" +
                                         "/cv2/data/haarcascade_profileface.xml")

    # change the color to gray scaled
    if image_flip.ndim == 3:
        gray = cv2.cvtColor(image_flip, cv2.COLOR_BGR2GRAY)
    else:
        gray = image_flip

    # detect face
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    result = []

    # write into result
    for (x, y, width, height) in faces:
        result.append((x, y, x + width, y + height))

    return result


# function to detect full body
def detectFullBody(image):
    # get cascadeClassifier
    face_cascade = cv2.CascadeClassifier("./venv/Lib/site-packages" +
                                         "/cv2/data/haarcascade_fullbody.xml")

    # change the color to gray scaled
    if image.ndim == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # detect face
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    result = []

    # write into result
    for (x, y, width, height) in faces:
        result.append((x, y, x + width, y + height))

    return result


# function to save images with faces
def saveFaces(image, inputUI, api):
    # detect for every side of faces
    frontal_faces = detectFrontalFaces(image)
    right_profile_faces = detectRightProfileFace(image)
    left_profile_faces = detectLeftProfileFace(image)
    full_body = detectFullBody(image)

    # if there is a face then save it
    if (len(frontal_faces) != 0) | (len(right_profile_faces) != 0) | (len(left_profile_faces) != 0) | (
            len(full_body) != 0):
        global index
        address = "./" + "auto_" + str(index) + ".jpg"
        cv2.imwrite(address, image)

        if api == "Baidu":
            result = detectMask.baidu_API_fingMask(address)
        elif api == "JD":
            result = detectMask.jd_API_fingMask(address)
        elif api == "SNN":
            result = detectMask.snn_API_fingMask(address)

        inputUI.label_4.setText(result)
        inputUI.label_4.repaint()
        index += 1
        if index > 50:
            index = 1

        main.log(result, 'info')
