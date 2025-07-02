# Use an official CPU-based PyTorch image as a parent image
FROM pytorch/pytorch:latest

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application code to the container
COPY . /app

# Install system dependencies that might be needed by OpenCV and other libraries
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Install Python dependencies
# We install torch and torchvision first from the base image, then the rest via pip
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the training script
CMD ["python", "src/train.py"]
