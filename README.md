# ev-sight
# EVSight - Electric Vehicle Charger Detection

This project aims to build and fine-tune an object detection model to identify electric vehicle (EV) charging stations in images. The model is built using the YOLOv5 architecture.

## Features

-   Object detection model fine-tuned on a custom dataset of EV chargers.
-   Data processing scripts to convert annotations from various formats.
-   A FastAPI backend to serve the model and provide predictions.
-   Docker support for easy deployment.
-   A comprehensive test suite using `pytest`.

## Project Structure

```
ev-sight/
├── .gitignore
├── Dockerfile
├── README.md
├── data/
│   ├── predefined_classes.txt
│   └── ... (COCO format data)
├── requirements.txt
├── src/
│   ├── api.py
│   ├── model.py
│   ├── prepare_yolo5_data.py
│   └── process_gemini_annotations.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_dataset.py
│   └── test_model.py
└── yolov5/
    └── ... (YOLOv5 repository)
```

-   `data/`: Contains the training and validation datasets.
-   `src/`: Contains the core Python source code for the project.
    -   `api.py`: The FastAPI application to serve the model.
    -   `model.py`: The PyTorch Lightning module for the object detection model.
    -   `prepare_yolo5_data.py`: Script to prepare data for YOLOv5 training.
    -   `process_gemini_annotations.py`: Script to process annotations from Gemini.
-   `tests/`: Contains the test suite for the project.
-   `yolov5/`: A submodule containing the YOLOv5 repository.
-   `Dockerfile`: For building the Docker image.
-   `requirements.txt`: A list of all Python dependencies for this project.

## Getting Started

### Prerequisites

-   Python 3.8+
-   Docker (optional)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/ev-sight.git
    cd ev-sight
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Usage

1.  **Prepare the data:**

    Run the data processing scripts in `src/` to prepare your dataset.

2.  **Train the model:**

    Follow the instructions in the `yolov5` directory to train the model on the custom dataset.

3.  **Run the API:**

    ```bash
    uvicorn src.api:app --host 0.0.0.0 --port 8000
    ```

### Docker

To build and run the application using Docker:

```bash
docker build -t ev-sight .
docker run -p 8000:8000 ev-sight
```

## Testing

To run the test suite:

```bash
pytest
```
