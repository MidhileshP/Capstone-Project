import cv2
import pytesseract
from gtts import gTTS
import pygame
import time
from PIL import Image
import os



# Initialize video capture
vid = cv2.VideoCapture(0)

if not vid.isOpened():
    print("Error: Could not open the camera.")
    exit()


while True:
    try:
        #Capture frame-by-frame
        ret, frame = vid.read()
        if not ret:
            print("Error: Could not read a frame.")
            continue

        # Display the live video feed
    

        # Save the captured frame
        image_path = "captured_image.jpg"
        cv2.imwrite(image_path, frame)

        # Preprocess the image for 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        # OCR with Tesseract
        extracted_text = pytesseract.image_to_string(gray, config='-l eng --oem 3 --psm 6')
    

        # Check if any text is recognized
        if extracted_text.strip():
            print("Extracted Text:")
            print(extracted_text)

            tts=gTTS(text=extracted_text,lang='en',slow=False)
            audio_path="speech.mp3"
            tts.save(audio_path)

            fast_audio="speech_fast.mp3"
            os.system(f'ffmpeg -y -i {audio_path} -filter:a "atempo=1.25" -vn {fast_audio}')

            pygame.mixer.init()
            pygame.mixer.music.load(fast_audio)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.5)

            os.remove(audio_path)
            os.remove(fast_audio)




            
        else:
            print("No text detected in the captured image.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Release the video capture object
vid.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()

print("Program exited.")
