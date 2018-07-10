import face_recognition
import cv2 #opencv needs to be installed

input_movie = cv2.VideoCapture("\\videos\\infinity_war_trailer.mp4")
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

fourcc = cv2.VideoWriter_fourcc(*'XVID')

#Make sure to adjust the frame height,width and rate in next line
output_movie = cv2.VideoWriter('output.avi', fourcc, 23.98, (640,266))

list=[]

#Since we are using data folder as image set,loop 45 times. 
for i in range(1,46):
    image="image"+str(i)
    face_encoding="face_encoding"+str(i)
    image= face_recognition.load_image_file("\\data\\"+str(i)+".png")
    face_encoding = face_recognition.face_encodings(image)[0]
    list.append(face_encoding)

known_faces = list
face_locations = []
face_encodings = []
face_names = []
frame_number = 0

while True:
    ret, frame = input_movie.read()
    frame_number += 1
    if not ret:
        break
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.6)
        name = None

        #Names file contains the names to be displayed in order of images in data.
        file=open('names.txt','r')
        names=file.readlines()

        for i in range(0,45):
            if match[i]:
                name =names[i]
                face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
    
    print("Writing frame {} / {}".format(frame_number, length))
    output_movie.write(frame)
    
input_movie.release()
cv2.destroyAllWindows()
