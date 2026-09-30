# SnapAssist — AI Field Engineer Assistant

SnapAssist is a privacy-first engineering assistant that combines computer vision, retrieval-augmented generation (RAG), and natural-language interaction to help technicians and engineering students identify electrical components and access relevant maintenance and safety information.

## Key Features

- Image-based electrical component detection
- Engineering knowledge retrieval using RAG
- Natural-language engineering Q&A
- Maintenance and safety guidance
- Local-first processing architecture
- Web-based Gradio interface
- FastAPI backend for modular deployment

## Architecture

User Image
    ↓
Computer Vision
    ↓
Component Identification
    ↓
Engineering Knowledge Retrieval
    ↓
Question Understanding
    ↓
Relevant Engineering Guidance

## Technology Stack

- Python
- FastAPI
- Gradio
- Ultralytics YOLO
- Sentence Transformers
- NumPy / Scikit-learn
- OpenCV
- Pillow

## Example Questions

The assistant can answer questions such as:

- What is an MCB?
- What does an MCB do?
- How do I maintain an MCB?
- What safety precautions should I take?
- What should I check if an MCB keeps tripping?

## Snapdragon AI Optimization

SnapAssist is designed for deployment on Snapdragon-powered Windows PCs.

The computer-vision pipeline is intended to use Qualcomm AI Hub optimized models and Qualcomm's QNN execution stack where supported.

Qualcomm AI Hub provides optimized model deployments for Snapdragon platforms, including object-detection models targeting the Snapdragon X Elite NPU.

Reference AI Hub benchmarks are used only as deployment references; local benchmark results should be measured separately on the target Snapdragon device.

## Current Prototype

The current prototype has been developed and tested on a Windows PC.

The application currently demonstrates:

1. Image upload
2. Component analysis
3. Engineering knowledge retrieval
4. Natural-language Q&A
5. FastAPI + Gradio integration

Snapdragon-specific deployment and NPU benchmarking are the next deployment stage.

## Privacy

The intended deployment architecture is local-first. Images and engineering queries can be processed locally without requiring cloud upload of sensitive field images.

## Project Structure

```text
SnapAssist/
├── app/
│   ├── main.py
│   ├── ui.py
│   └── services/
│       ├── vision.py
│       ├── rag.py
│       └── llm.py
├── data/
│   └── knowledge.json
├── models/
├── uploads/
├── requirements.txt
├── README.md
└── .gitignore