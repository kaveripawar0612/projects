# Signature Forgery Detection Using AI

Portfolio implementation for offline signature verification using computer vision and deep learning concepts.

### Planned pipeline
Image → OpenCV preprocessing → CNN feature extraction → sequence/embedding comparison → genuine/forged decision → explainability.

The repository includes a lightweight baseline that can run without claiming research-level performance. For a full experiment, connect a properly licensed signature dataset such as CEDAR and train/evaluate on writer-disjoint splits.

### Stack
Python • OpenCV • TensorFlow/Keras • NumPy

### Run baseline
```bash
pip install -r requirements.txt
python baseline.py --image path/to/signature.png
```
