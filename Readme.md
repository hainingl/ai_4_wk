# Project Setup and Usage Guide

This guide will walk you through setting up and using a virtual environment for your Python project.

---

## Setting Up a Virtual Environment

A virtual environment allows you to manage dependencies for your project in an isolated environment.

### 1. Create a Virtual Environment

On **macOS and Linux**:
```bash
python3 -m venv venv
```

On **Windows**:
```bash
python -m venv venv
```

This will create a virtual environment in a folder named `venv`.

---

### 2. Activate the Virtual Environment

On **macOS and Linux**:
```bash
source venv/bin/activate
```

On **Windows**:
```bash
venv\Scripts\activate
```

Once activated, your terminal prompt will change to indicate that the virtual environment is active.

---

### 3. Install Required Packages

Make sure you have a `requirements.txt` file in your project directory with the necessary dependencies listed. Then run:

```bash
pip install -r requirements.txt
```

This will install all the required packages in your virtual environment.

---

### 4. Run Your Scripts

With the virtual environment activated, you can run your Python scripts as usual. For example:

```bash
python your_script.py
```

---

### 5. Deactivate the Virtual Environment

When you are done working in the virtual environment, you can deactivate it by running:

```bash
deactivate
```

---

## Example

Here’s an example workflow:

1. Create and activate the virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run your script:
   ```bash
   python your_script.py
   ```

4. Deactivate the virtual environment when done:
   ```bash
   deactivate
   ```

---

## Notes

- Replace `your_script.py` with the name of your Python script.
- Ensure your `requirements.txt` file lists all the dependencies your project needs.

