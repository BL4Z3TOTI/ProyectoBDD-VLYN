import os
import cv2
import numpy as np
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection


class FaceRecognizerLite:
    def __init__(self, embed_dim=128):
        self.embed_dim = embed_dim

    def detect_face(self, img):
        with mp_face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5
        ) as fd:
            results = fd.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            if not results.detections:
                return None

            box = results.detections[0].location_data.relative_bounding_box
            h, w, _ = img.shape
            x1 = int(box.xmin * w)
            y1 = int(box.ymin * h)
            x2 = x1 + int(box.width * w)
            y2 = y1 + int(box.height * h)

            return img[y1:y2, x1:x2]

    def get_embedding(self, face):
        face = cv2.resize(face, (64, 64))
        arr = face.astype(np.float32) / 255.0
        flat = arr.flatten()
        if len(flat) < self.embed_dim:
            padded = np.zeros(self.embed_dim, dtype=np.float32)
            padded[:len(flat)] = flat
            return padded
        return flat[:self.embed_dim]

    def compare(self, emb1, emb2):
        return np.linalg.norm(emb1 - emb2)

    def load_database(self, db_path):
        database = {}
        for person in os.listdir(db_path):
            person_dir = os.path.join(db_path, person)
            if not os.path.isdir(person_dir):
                continue

            embeddings = []
            for file in os.listdir(person_dir):
                path = os.path.join(person_dir, file)
                try:
                    img = cv2.imread(path)
                    if img is None:
                        continue
                    face = self.detect_face(img)
                    if face is None:
                        continue
                    emb = self.get_embedding(face)
                    embeddings.append(emb)
                except:
                    continue

            if embeddings:
                database[person] = np.mean(np.array(embeddings), axis=0)

        return database

    def predict(self, img_path, db_path):
        img = cv2.imread(img_path)
        if img is None:
            return None

        face = self.detect_face(img)
        if face is None:
            return None

        emb = self.get_embedding(face)

        database = self.load_database(db_path)

        best_person = None
        best_dist = 999999

        for person, emb_ref in database.items():
            dist = self.compare(emb, emb_ref)
            if dist < best_dist:
                best_dist = dist
                best_person = person

        if best_person is None:
            return None

        return {
            "person": best_person,
            "distance": best_dist
        }

