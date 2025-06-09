from ultralytics import YOLO

model=YOLO('/home/helix/yolo11n.onnx', task='detect')
results=model.predict(source=0, show=True, classes=0)
