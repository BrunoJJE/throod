import bge
from collections import OrderedDict

import mediapipe as mp
import cv2
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh


class app_throod_eyes(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
    ])

    def start(self, args):
        # Put your initialization code here, args stores the values from the UI.
        # self.object is the owner object of this component.
        # self.object.scene is the main scene.

        self.cap = cv2.VideoCapture(1)  # Change this number according to the device to use

        self.scene = bge.logic.getCurrentScene()
        self.cam_x = self.scene.objects["Cam"].worldPosition.x
        self.cam_y = self.scene.objects["Cam"].worldPosition.y
        self.cam_z = self.scene.objects["Cam"].worldPosition.z
        self.face_x = None
        self.face_y = None
        self.face_z = None

    def update(self):
        # Put your code executed every logic step here.
        # self.object is the owner object of this component.
        # self.object.scene is the main scene.

        hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
        faces = mp_face_mesh.FaceMesh(min_detection_confidence=0.8, min_tracking_confidence=0.5, refine_landmarks=True)

        if self.cap.isOpened():

            ret, frame = self.cap.read()
            
            # BGR 2 RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Flip on horizontal
            image = cv2.flip(image, 1)
            
            # Set flag
            image.flags.writeable = False
            
            # Detections
            results_hands = hands.process(image)
            results_faces = faces.process(image)
            
            # Set flag to true
            image.flags.writeable = True
            
            # RGB 2 BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Detections
            #print(results_hands)
            
            # Rendering results
            if results_hands.multi_hand_landmarks:
                for num, hand_landmarks in enumerate(results_hands.multi_hand_landmarks):

                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style(),
                        )               

            if results_faces.multi_face_landmarks:

                # right eye center : 468
                # left eye center : 473
                #print(results_faces.multi_face_landmarks[0].landmark[468])

                print("--")
                height, width, channels = frame.shape
                #print(f"frame width :", width)
                #print(f"frame height :", height)
                #print(f"frame channels :", channels)

                # right eye center : 468
                # left eye center : 473
                #print(results_faces.multi_face_landmarks[0].landmark[468])

                # right eye iris left and right : 469, 471
                # left eye iris left and right : 474, 476

                # eye diameter
                r = results_faces.multi_face_landmarks[0].landmark[471]
                l = results_faces.multi_face_landmarks[0].landmark[469]
                iris_r_diameter_pixel = np.sqrt((r.x-l.x)**2 + (r.y-l.y)**2)

                r = results_faces.multi_face_landmarks[0].landmark[476]
                l = results_faces.multi_face_landmarks[0].landmark[474]
                iris_l_diameter_pixel = np.sqrt((r.x-l.x)**2 + (r.y-l.y)**2)

                #print(f"{iris_r_diameter_pixel =}")
                #print(f"{iris_l_diameter_pixel =}")

                # The horizontal iris diameter of the human eye remains roughly
                # constant at 11.7±0.5 mm across a wide population.
                iris_size_mm = 11.7

                # Logitech HD Pro C922 Norm focal
                normalizedFocaleX = 1.40625
                fx = min(width, height) * normalizedFocaleX

                # distance converted to cm (?)
                r_dZ = (fx * (iris_size_mm / iris_r_diameter_pixel)) / 10000.0;
                l_dZ = (fx * (iris_size_mm / iris_l_diameter_pixel)) / 10000.0;

                #print(f"{r_dZ =}")
                #print(f"{l_dZ =}")


                for face_landmarks in results_faces.multi_face_landmarks:

                    mp_drawing.draw_landmarks(
                        image,
                        face_landmarks,
                        mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_tesselation_style())

                    mp_drawing.draw_landmarks(
                        image,
                        face_landmarks,
                        mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_contours_style())

                    mp_drawing.draw_landmarks(
                        image,
                        face_landmarks,
                        mp_face_mesh.FACEMESH_IRISES,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_iris_connections_style())

                if self.face_x == None:
                    #print("# init")
                    self.face_x = results_faces.multi_face_landmarks[0].landmark[468].x
                    self.face_y = results_faces.multi_face_landmarks[0].landmark[468].y
                    #self.face_z = results_faces.multi_face_landmarks[0].landmark[468].z
                    self.face_z = (r_dZ + l_dZ)/2.0
                else:
                    #print("# test")
                    self.scene.objects["Cam"].worldPosition.x = self.cam_x + 3.0*(results_faces.multi_face_landmarks[0].landmark[468].x - self.face_x)
                    self.scene.objects["Cam"].worldPosition.y = self.cam_y - 0.12*((r_dZ + l_dZ)/2.0 - self.face_z)
                    self.scene.objects["Cam"].worldPosition.z = self.cam_z - 5.0*(results_faces.multi_face_landmarks[0].landmark[468].y - self.face_y)


