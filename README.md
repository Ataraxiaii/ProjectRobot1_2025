# 🤖 Micro:bit Face Recognition Robot

## Project Overview 😎
The `ProjectRobot1_2025` is an innovative hardware - software integrated project. Its objective is to build a robot with face recognition capabilities using Micro:bit components and Python scripts. Developed in an `agile approach`, it consists of two main phases: planning and implementation. In the planning phase, the Scrum framework is adopted, focusing on iterative development, user stories, and team collaboration to ensure efficient project progress. In the implementation phase, functions are gradually realized, leading to the completion of the robot's construction and function demonstration.

## Key Features ✨
### 1. Image Display Function 🖼️
- Cycles through displaying images of numbers from 1 to 9 on the Micro:bit's LED matrix, with each number shown for 1 second.

### 2. Face Recognition Function 😀
- Utilizes a camera to capture images and the YOLO model for face detection. After a face is detected, a facial landmark detection model extracts facial features. Compares the detected face with registered faces, displays the recognition result (registered or unregistered), and sends the result via serial communication. New face features can be registered by pressing a button.

### 3. Face Data Hashing Function 🔒
- Based on the face recognition function, this feature applies the `PBKDF2 - HMAC - SHA256` algorithm to hash the extracted facial features. It stores and compares the hashed features to enhance data security and privacy.

## Hardware Setup 🛠️
### Required Hardware 📦
- **Micro:bit Development Board**: Serves as the robot's control core, running Python scripts and controlling components.
- **K210 Camera Module**: Captures images for the face recognition function.

### Setup Steps 📋
- Connect the camera module to the Micro:bit development board via corresponding interfaces for data transmission.
- Ensure all hardware connections are secure to prevent loose or poor - contact issues.

### Hardware Photos 📷
<div style="display: flex; justify-content: center;">
    <img src="https://github.com/Ataraxiaii/ProjectRobot1_2025/blob/main/Project%20Images/Hardware%20Component.jpg" alt="Hardware Photo 1" style="width: 45%; margin-right: 5%;">
    <img src="https://github.com/Ataraxiaii/ProjectRobot1_2025/blob/main/Project%20Images/Robot%20Car.jpg" alt="Hardware Photo 2" style="width: 45%;">
</div>

## Software Introduction 💻
### Development Environment 🛠️
- **Programming Language**: Python
- **Development Tools**: Mu editor, CanMV-IDE

### Code Structure 📁
The project code is divided into three main exercise modules, each implementing a specific function: image display, face recognition, and face data hashing.

## How to Run the Project 🚀
1. Connect the Micro:bit development board to your computer.
2. Use `Mu Editor` to upload the relevant Python script to the Micro:bit.
3. Use TF card to upload YOLO models for K210 camera module.
