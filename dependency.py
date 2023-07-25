"""
Create env
    python -m venv C:\Workspace\resume-agent\venv

Activate env
    .\venv\Scripts\activate

Install pipreqs and torch
    pip install pipreqs
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117

Generate requirements.txt
    pipreqs ./ --force --encoding=utf8

Manually put these in requirements.txt
pdfminer.six==20221105
pywin32==306
!!! Pillow must be lower than 10.0.0 !!!

Install dependencies
    pip install --upgrade -r requirements.txt
"""
import torch

if torch.cuda.is_available():
    print("CUDA is available. Testing on GPU.")
else:
    print("CUDA is not available. Testing on CPU.")
