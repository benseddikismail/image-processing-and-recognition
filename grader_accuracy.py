import subprocess

def calculate_accuracy(ground_truth, grader_output):
    correct_count = 0
    for question, answer in ground_truth.items():
        if grader_output[question] == answer:
            correct_count += 1
    total_count = len(ground_truth)
    accuracy = (correct_count / total_count) * 100
    return accuracy

def get_answers(file_path):
    answers = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split()
            question_number = int(parts[0])
            answer = parts[1]
            answers[question_number] = answer
    return answers

def test_grader(image, grader_output, ground_truth):
    subprocess.run(["python3", "grade.py", image, grader_output])
    grader_output_answers = get_answers(grader_output)
    ground_truth_answers = get_answers(ground_truth)
    accuracy = calculate_accuracy(ground_truth_answers, grader_output_answers)
    return accuracy

image1 = "test-images/a-3.jpg"  
image2 = "test-images/a-27.jpg"
image3 = "test-images/b-13.jpg"
image4 = "test-images/c-18.jpg"
image5 = "test-images/a-30.jpg"

grader_output1 = "output_a-3.txt"
grader_output2 = "output_a-27.txt"
grader_output3 = "output_b-13.txt"
grader_output4 = "output_c-18.txt"
grader_output5 = "output_a-30.txt"

ground_truth1 = "test-images/a-3_groundtruth.txt"
ground_truth2 = "test-images/a-27_groundtruth.txt"
ground_truth3 = "test-images/b-13_groundtruth.txt"
ground_truth4 = "test-images/c-18_groundtruth.txt"
ground_truth5 = "test-images/a-30_groundtruth.txt"

accuracy1 = test_grader(image1, grader_output1, ground_truth1)
print(f"Accuracy for a-3: {accuracy1:.2f}%")
accuracy2 = test_grader(image2, grader_output2, ground_truth2)
print(f"Accuracy for a-27: {accuracy2:.2f}%")
accuracy3 = test_grader(image3, grader_output3, ground_truth3)
print(f"Accuracy for b-13: {accuracy3:.2f}%")
accuracy4 = test_grader(image4, grader_output4, ground_truth4)
print(f"Accuracy for c-18: {accuracy4:.2f}%")
accuracy5 = test_grader(image5, grader_output5, ground_truth5)
print(f"Accuracy for a-30: {accuracy5:.2f}%")

overall_accuracy = (accuracy1 + accuracy2 + accuracy3 + accuracy4 + accuracy5) / 5
print(f"Average Accuracy: {overall_accuracy:.2f}%")
