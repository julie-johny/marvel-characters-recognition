import face_recognition
import cv2 #install opencv

input_movie = cv2.VideoCapture("\\videos\\infinity_war_trailer.mp4")
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

fourcc = cv2.VideoWriter_fourcc(*'XVID')

output_movie = cv2.VideoWriter('output.avi', fourcc, 23.98, (640,266))

for i in range(1,68):
    lmm_image="lmm_image"+str(i)
    lmm_face_encoding="lmm_face_encoding"+str(i)
    lmm_image= face_recognition.load_image_file("\\data\\"+str(i)+".png")
    lmm_face_encoding = face_recognition.face_encodings(lmm_image)[0]
    list.append(lmm_face_encoding)

known_faces = list

face_locations = []

face_encodings = []

face_names = []

frame_number = 0



while True:

    # Grab a single frame of video

    ret, frame = input_movie.read()

    frame_number += 1

    if not ret:

        break


    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)

    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []

    for face_encoding in face_encodings:

        # See if the face is a match for the known face(s)

        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.6)

        name = None
file=open('names.txt','r')
names=file.readlines()
for i in range(0,68):
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



# All done!

input_movie.release()

cv2.destroyAllWindows()
