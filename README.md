# 📝 **PDF Outline Extractor**

## 🚀 **Overview**

**PDF Outline Extractor** is a containerised solution that **processes PDF files to extract**:

* **Document Title**
* **Headings:** H1, H2, H3 (with level, text, and page number)

This tool was built for **Hackathon Round 1A**, under strict constraints of **offline execution, CPU-only processing, <200MB model size, and ≤10 seconds runtime per 50-page PDF**.

---

## ✅ **Features**

✔️ Extracts **document title** using **font size + position heuristic**

✔️ Extracts **headings** and classifies them as **H1, H2, H3** based on font size clustering

✔️ Retains **special characters** (colons, semicolons, dots, commas, etc.) in extracted text

✔️ Outputs results in **valid JSON** format for each PDF

✔️ Fully **offline**, **CPU-only**, and **Dockerised**

---

## 📂 **Folder Structure**

```
pdf_outline_extractor_project/
├── app/
│   ├── __init__.py           # Package marker
│   ├── main.py               # Entry point script
│   ├── extractor.py          # Core extraction logic
│   ├── utils.py              # Helper functions (e.g. text cleaning)
│   └── constants.py          # Config thresholds
│
├── input/                    # Input PDFs mounted here
│   └── sample.pdf
│
├── output/                   # Output JSONs generated here
│
├── requirements.txt          # Python dependencies
├── Dockerfile                # For building the container
└── README.md                 # Project documentation
```

---

## ⚙️ **Tech Stack**

| **Component**          | **Library / Tool** | **Purpose**                                       |
| ---------------------- | ------------------ | ------------------------------------------------- |
| **PDF Parsing**        | PyMuPDF (fitz)     | Fast, lightweight PDF parsing and font extraction |
| **Numeric Operations** | numpy              | For font size clustering                          |
| **Clustering**         | scikit-learn       | KMeans clustering to detect heading hierarchy     |
| **Containerisation**   | Docker             | Portability and offline execution                 |

---

## 🔧 **Dependencies**

Listed in **requirements.txt**:

```
PyMuPDF==1.22.0
numpy
scikit-learn
```

Install them using:

```bash
pip install -r requirements.txt
```

---

## 💡 **Approach and Working**

### **1. Title Extraction**

* Extracts text blocks on the **first page**.
* Filters blocks in the **top 30% area** of the page.
* Selects block with **largest font size** as the document title.
* If no suitable block is found, falls back to **PDF metadata title**.

---

### **2. Heading Extraction**

* Parses all pages to extract text spans with their **font sizes** and **page numbers**.
* Uses **KMeans clustering** on font sizes to classify headings into **H1, H2, H3**:

  * Largest font cluster → **H1**
  * Second largest → **H2**
  * Third largest → **H3**
* Outputs each heading with:

  * **Level:** H1, H2, H3
  * **Text:** Cleaned text with special characters retained
  * **Page number**

---

### **3. Output Format**

Outputs a JSON file for each input PDF in the following format:

```json
{
  "title": "Understanding AI: An Overview",
  "outline": [
    { "level": "H1", "text": "Introduction: AI Basics", "page": 1 },
    { "level": "H2", "text": "History of AI; Milestones", "page": 2 },
    { "level": "H3", "text": "Key Areas - Machine Learning, NLP, Robotics", "page": 3 }
  ]
}
```

---

## 🐳 **Build and Execution**

### **1. Build Docker Image**

Ensure you are in the **project root directory** and run:

```bash
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
```

This builds the image with:

* **AMD64 architecture compatibility**
* All dependencies installed within the container
* Final image size under **200MB**

---

### **2. Run Docker Container**

Run using the **hackathon execution command pattern**:

```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:latest
```

✔️ **All PDFs in `/input` directory will be processed automatically.**

✔️ **Outputs are saved as .json files in `/output` directory** with the **same filenames as the input PDFs**.

---

## ⏱️ **Performance**

* Execution time: **≤10 seconds** for a **50-page PDF**
* **Model size:** None used; uses **heuristics + clustering** for <200MB total image size
* Runs **offline** with **no internet calls**

---

## 🚫 **Constraints Compliance**

✅ No hardcoded filenames

✅ No internet / API calls

✅ No GPU dependencies

✅ <200MB container size

✅ Runs on CPU (AMD64)

✅ Outputs valid JSONs as per hackathon format

---

## 👤 **Author**

**Developed by:**  Prince Chouksey, Poonam Raghuwanshi 

**Hackathon:**     Adobe Hackathon Round 1A



---

## 📞 **Contact**

For queries, connect at -  princechouksey137@gmail.com
