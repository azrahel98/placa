import cv2
from ultralytics import YOLO
import io
import numpy as np


def verificar(img):
    model = YOLO('./best.pt')
    in_memory_file = io.BytesIO(img.read())
    file_bytes = np.asarray(bytearray(in_memory_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    results = model(frame,device="cpu")
    
    placa_count = 0
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
           
            plate_filename = f'./folder/plate_{placa_count}.jpg'
            conf = float(box.conf[0])
            cls = box.cls[0]
            label = f'{result.names[int(cls)]} {conf:.2f}'
            
            if conf > 0.56:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                cv2.imwrite(plate_filename,frame[y1:y2, x1:x2])
            
    cv2.destroyAllWindows()