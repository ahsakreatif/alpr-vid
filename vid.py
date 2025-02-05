import sys
import numpy as np
import cv2
from openalpr import Alpr
import os

def init_alpr():
    try:
        # Check if config files exist
        if not os.path.exists("openalpr.conf"):
            print("Error: openalpr.conf not found")
            sys.exit(1)
        if not os.path.exists("runtime_data"):
            print("Error: runtime_data directory not found")
            sys.exit(1)
            
        # Initialize ALPR
        alpr = Alpr("id", "openalpr.conf", "runtime_data")
        if not alpr.is_loaded():
            print("Error loading OpenALPR")
            sys.exit(1)
            
        alpr.set_top_n(1)
        alpr.set_default_region("id")
        return alpr
    except Exception as e:
        print(f"Error initializing ALPR: {str(e)}")
        sys.exit(1)

def process_video():
    alpr = init_alpr()
    
    try:
        # Uncomment the appropriate video source
        # cap = cv2.VideoCapture("http://0.0.0.0:4747/mjpegfeed?640x480")
        # cap = cv2.VideoCapture("http://192.168.200.22:4747/mjpegfeed?640x480")
        cap = cv2.VideoCapture("sample/1.mp4")
        # cap = cv2.VideoCapture(1)

        if not cap.isOpened():
            print("Error: Could not open video source")
            sys.exit(1)

        while True:    
            ret, frame = cap.read() 

            if not ret:
                break

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Save frame to temporary file
            temp_img_path = "temp_frame.jpg"
            cv2.imwrite(temp_img_path, frame)

            try:
                results = alpr.recognize_file(temp_img_path)

                for i, plate in enumerate(results['results'], 1):
                    print(f"Plate #{i}")
                    print("   %12s %12s" % ("Plate", "Confidence"))
                    for candidate in plate['candidates']:
                        prefix = "*" if candidate['matches_template'] else "-"
                        print("  %s %12s%12f" % (
                            prefix, 
                            candidate['plate'], 
                            candidate['confidence']
                        ))
            except Exception as e:
                print(f"Error processing frame: {str(e)}")

    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        # Cleanup
        if 'cap' in locals():
            cap.release()
        if 'alpr' in locals():
            alpr.unload()
        cv2.destroyAllWindows()
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)

if __name__ == "__main__":
    process_video()
