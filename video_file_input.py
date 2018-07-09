import face_recognition
import cv2

# This is a demo of running face recognition on a video file and saving the results to a new video file.
#
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.# Open the input movie file

input_movie = cv2.VideoCapture("B:\\videos\\infinity_war_trailer.mp4")

length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
# Create an output movie file (make sure resolution/frame rate matches input video!)

fourcc = cv2.VideoWriter_fourcc(*'XVID')

output_movie = cv2.VideoWriter('output.avi', fourcc, 23.98, (640,266))


lmm_image = face_recognition.load_image_file("B:\\data\\1.png")
lmm_face_encoding = face_recognition.face_encodings(lmm_image)[0]

# Load some sample pictures and learn how to recognize them.
for i in range(1,68):
    lmm_image="lmm_image"+str(i)
    lmm_face_encoding="lmm_face_encoding"+str(i)
    lmm_image= face_recognition.load_image_file("B:\\data\\"+str(i)+".png")
    lmm_face_encoding = face_recognition.face_encodings(lmm_image)[0]
    list.append(lmm_face_encoding)

known_faces = list



# Initialize some variables

face_locations = []

face_encodings = []

face_names = []

frame_number = 0



while True:

    # Grab a single frame of video

    ret, frame = input_movie.read()

    frame_number += 1



    # Quit when the input video file ends

    if not ret:

        break



    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)

    rgb_frame = frame[:, :, ::-1]



    # Find all the faces and face encodings in the current frame of video

    face_locations = face_recognition.face_locations(rgb_frame)

    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)



    face_names = []

    for face_encoding in face_encodings:

        # See if the face is a match for the known face(s)

        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.6)



        # If you had more than 2 faces, you could make this logic a lot prettier

        # but I kept it simple for the demo

        name = None
file=open('names.txt','r')
names=file.readlines()
for i in range(0,68):
        if match[i]:
            name =names[i]



        face_names.append(name)


# Label the results

for (top, right, bottom, left), name in zip(face_locations, face_names):

    if not name:

        continue



        # Draw a box around the face

    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)



    # Draw a label with a name below the face

    cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)

    font = cv2.FONT_HERSHEY_DUPLEX

    cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)



# Write the resulting image to the output video file

print("Writing frame {} / {}".format(frame_number, length))

output_movie.write(frame)



# All done!

input_movie.release()

cv2.destroyAllWindows()