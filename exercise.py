import cv2
import numpy as np
import time
import PoseModule as pm
import PoseModule1 as pd1

def bicep_curls():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    dir = 0
    pTime = 0

    while True:
        success, img = cap.read()
        img = cv2.resize(img, (1280, 720))
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            angle = detector.findAngle(img, 11, 13, 15)
            per = np.interp(angle, (200, 300), (0, 100))
            bar = np.interp(angle, (200, 300), (650, 100))
            
            # Draw percentage bar
            cv2.rectangle(img, (1210, 100), (1250, 650), (255, 0, 0), 3)
            cv2.rectangle(img, (1210, int(bar)), (1250, 650), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (1200, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            color = (255, 0, 255)
            if per == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (0, 255, 0)
                if dir == 1:
                    count += 0.5
                    dir = 0
            print(count)

            # Set the position of the count text
            count_text_x = 45
            count_text_y = 670

            # Define the count text font properties
            count_font = cv2.FONT_HERSHEY_SIMPLEX
            count_font_scale = 5
            count_thickness = 10

            # Determine the size of the count text
            (count_text_width, count_text_height), _ = cv2.getTextSize(str(int(count)), count_font, count_font_scale, count_thickness)

            # Calculate the position to center the count text
            count_text_x -= count_text_width // 2
            count_text_y += count_text_height // 2

            # Draw the count text
            cv2.putText(img, str(int(count)), (count_text_x, count_text_y), count_font, count_font_scale, (255, 0, 0), count_thickness)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
    
        cv2.imshow("Image", img)
    
        if cv2.waitKey(1) == ord("e"):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def shoulder_raise():
    cap = cv2.VideoCapture(0)
    detector = pd1.poseDetector()
    count = 0
    rep_up = 0
    bTime = time.time()  # Initialize bTime with current time

    while True:
        success, image = cap.read()
        image = cv2.resize(image, (1280, 720))
        image = cv2.flip(image, 2)
        image = detector.findPose(image, False)
        lmList = detector.findPosition(image, False)
        wrist = []

        if len(lmList) != 0:
            upbody_r = detector.findAngle(image, 24, 12, 14)
            upbody_l = detector.findAngle(image, 23, 11, 13)
            per_l = np.interp(upbody_l, (235, 270), (100, 0))
            per_r = np.interp(upbody_r, (95, 124), (0, 100))


            # Check if wrist is higher than shoulder
            if lmList[11][2] > lmList[14][2]:  
                # Draw the right position for right arm
                wrist.append([lmList[14][1], lmList[14][2] - detector.lenght(image, 14, 16)])
                # Draw the right position for left arm  
                wrist.append([lmList[13][1], lmList[13][2] - detector.lenght(image, 14, 16)])  
                angle_r = detector.cosin2angle(image, wrist[0], 14, 16)
                angle_l = detector.cosin2angle(image, wrist[1], 13, 15)

            if per_l == 100 and per_r == 100:
                color = (255, 0, 255)

                if rep_up == 0:
                    count += 0.5
                    rep_up = 1

            if per_l == 0 and per_r == 0:
                color = (0, 255, 0)

                if rep_up == 1:
                    count += 0.5
                    rep_up = 0

            print(count)

            # Set the position of the count text
            count_text_x = 45
            count_text_y = 670

            # Define the count text font properties
            count_font = cv2.FONT_HERSHEY_SIMPLEX
            count_font_scale = 5
            count_thickness = 10

            # Determine the size of the count text
            (count_text_width, count_text_height), _ = cv2.getTextSize(str(int(count)), count_font, count_font_scale, count_thickness)

            # Calculate the position to center the count text
            count_text_x -= count_text_width // 2
            count_text_y += count_text_height // 2

            # Draw the count text
            cv2.putText(image, str(int(count)), (count_text_x, count_text_y), count_font, count_font_scale, (255, 0, 0), count_thickness)

        nTime = time.time()
        fps = 1 / (nTime - bTime)
    
        # Update bTime with the current time
        bTime = nTime  
    
        cv2.imshow("Image", image)
    
        if cv2.waitKey(5) & 0xff == ord("e"):
            break
    
    cap.release()
    cv2.destroyAllWindows()


def main():
    exercise_running = False
    choice = ""

    while True:
        if not exercise_running:
            print("Select an exercise:")
            print("1. Bicep Curls")
            print("2. Shoulder Raise")
            print("Enter 'e' to exit")
            choice = input("Enter your choice: ")

        if choice == "1":
            exercise_running = True
            bicep_curls()
            exercise_running = False
        elif choice == "2":
            exercise_running = True
            shoulder_raise()
            exercise_running = False
        elif choice.lower() == "e":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

