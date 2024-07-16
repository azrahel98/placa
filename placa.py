import base64
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
    
    
    detectados = []
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
           
            conf = float(box.conf[0])
            cls = box.cls[0]
            label = f'{result.names[int(cls)]} {conf:.2f}'
            
            if conf > 0.56:
                _, buffer = cv2.imencode('.jpg', frame[y1:y2, x1:x2])
                plate_string = base64.b64encode(buffer).decode('utf-8')

                detectados.append({
                    'label':label,
                    'confianza':conf,
                    'placa':plate_string
                })
    cv2.destroyAllWindows()
    return detectados      
    
    
    
    
