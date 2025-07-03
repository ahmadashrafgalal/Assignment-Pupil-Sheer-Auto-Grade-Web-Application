import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"


model1_path = os.path.abspath("APP/CNN_Models/answer_classification_model_new_update_Final9.h5")
print(model1_path)
model2_path = os.path.abspath("APP/CNN_Models/simple_answer_classification_model_no_aug3.h5")  # Model for A/B/C/D
temp_folder = os.path.abspath("APP/temp_questions")

if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

model1 = load_model(model1_path)
model2 = load_model(model2_path)

num_questions = 60  
num_columns = 3   

# ===== SPLIT IMAGE INTO QUESTIONS =====
def split_image(image_path, num_questions, num_columns):
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found.")
        return None, None

    height, width = image.shape[:2]
    questions_per_column = num_questions // num_columns
    row_height = height // questions_per_column
    col_width = width // num_columns

    question_images = []
    for col in range(num_columns):
        for row in range(questions_per_column):
            y_start = row * row_height
            y_end = (row + 1) * row_height
            x_start = col * col_width
            x_end = (col + 1) * col_width

            question_img = image[y_start:y_end, x_start:x_end]
            question_filename = os.path.join(temp_folder, f"question_{col + 1}_{row + 1}.jpg")
            cv2.imwrite(question_filename, question_img)

            question_images.append((question_img, question_filename))
            cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

    return image, question_images


# ===== CLASSIFY QUESTIONS ===== 
def classify_questions(model, question_images):
    results = []
    for index, (question_img, path) in enumerate(question_images, start=1):
        img_resized = cv2.resize(question_img, (128, 128)) / 255.0
        img_resized = np.expand_dims(img_resized, axis=0)
        prediction = model.predict(img_resized)
        label = "True" if prediction[0][0] > 0.5 else "False"
        results.append((index, path, label))
    return results


# ===== CLASSIFY TRUE QUESTIONS INTO A/B/C/D ===== 
def classify_options(model, true_questions):
    results = []
    for index, question_img, path in true_questions:
        img_resized = cv2.resize(question_img, (128, 128)) / 255.0
        img_resized = np.expand_dims(img_resized, axis=0)
        prediction = model.predict(img_resized)
        label_index = np.argmax(prediction)
        label = ["A", "B", "C", "D"][label_index]
        results.append((index, label))
    
    return results


# ===== ANNOTATE IMAGE WITH ERRORS ===== 
def annotate_image(image, tf_results):
    for index, path, label in tf_results:
        if label == "False":  # Highlight errors in red
            filename = os.path.basename(path)
            parts = filename.split("_")
            col = int(parts[1])
            row = int(parts[2].split(".")[0])

            x_start = (col - 1) * (image.shape[1] // num_columns)
            y_start = (row - 1) * (image.shape[0] // (num_questions // num_columns))
            x_end = col * (image.shape[1] // num_columns)
            y_end = row * (image.shape[0] // (num_questions // num_columns))

            cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 0, 255), 3)
    return image


# ===== MAIN WORKFLOW =====
def process_exam_sheet(input_image_path,num_questions_to_process, assignment_id):
    annotated_image, question_images = split_image(input_image_path, num_questions, num_columns)
    if question_images is None:
        print("Failed to split the image. Exiting...")
        return

    question_images = question_images[:num_questions_to_process]

    tf_results = classify_questions(model1, question_images)

    true_questions = [
        (index, question_img, path)
        for index, (question_img, path), (_, _, label) in zip(range(1, len(question_images) + 1), question_images, tf_results)
        if label == "True"
    ]

    abcd_results = classify_options(model2, true_questions)
    print(abcd_results)

    annotated_image_with_errors = annotate_image(annotated_image.copy(), tf_results)

    output_path_errors = os.path.abspath(f"pupil_sheets/annotated_image_with_errors{assignment_id}.jpg")
    cv2.imwrite(output_path_errors, annotated_image_with_errors)

    return tf_results, abcd_results, output_path_errors


def process_exam_answer(input_image_path,num_questions_to_process, assignment_id, student_id):
    annotated_image, question_images = split_image(input_image_path, num_questions, num_columns)
    if question_images is None:
        print("Failed to split the image. Exiting...")
        return

    question_images = question_images[:num_questions_to_process]

    tf_results = classify_questions(model1, question_images)

    true_questions = [
        (index, question_img, path)
        for index, (question_img, path), (_, _, label) in zip(range(1, len(question_images) + 1), question_images, tf_results)
        if label == "True"
    ]

    abcd_results = classify_options(model2, true_questions)
    print(abcd_results)

    annotated_image_with_errors = annotate_image(annotated_image.copy(), tf_results)

    output_path_errors = os.path.abspath(f"pupil_sheets/annotated_image_with_errors_{assignment_id}_{student_id}.jpg")
    cv2.imwrite(output_path_errors, annotated_image_with_errors)

    return tf_results, abcd_results, output_path_errors
