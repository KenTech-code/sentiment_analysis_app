# Sentiment Analysis App

A Python application for analyzing sentiment in text data, providing both GUI-based interaction and visualizations.

---

## Project Overview

Sentiment Analysis App allows users to input text and determine the sentiment as positive, negative, or neutral. The app also provides visualizations, including word clouds for each sentiment category.

---

## Project Structure

```
sentiment_analysis_app/
├── gui.py              # Graphical user interface
├── main.py             # Main entry point
├── preprocessing.py    # Text preprocessing functions
├── sentiment.py        # Sentiment analysis logic
├── visualization.py    # Visualization functions
├── wordcloud_negative.png
├── wordcloud_neutral.png
├── wordcloud_positive.png
└── __pycache__/        # Compiled Python files (ignored)
```

> Note: Only Python source files and essential images are tracked. Compiled files and virtual environments should be ignored using .gitignore.

---

## Requirements

* Python 3.9 or higher
* pip packages:

  * `nltk`
  * `textblob`
  * `matplotlib`
  * `wordcloud`

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## Running the Application

1. **Clone the repository:**

```bash
git clone https://github.com/KenTech-code/sentiment_analysis_app.git
cd sentiment_analysis_app
```

2. **Run the application:**

```bash
python main.py
```

This will launch the GUI.

3. **Using the App:**

   * Input text to analyze sentiment.
   * Visualizations and word clouds will be generated automatically.

---

## Features

* GUI-based interaction
* Text preprocessing
* Sentiment classification (positive, negative, neutral)
* Word cloud visualizations for each sentiment category

---

## Important Notes

* Avoid pushing large data files or virtual environment folders.
* Ensure all required Python packages are installed before running.

---

## License

This project is open-source and free to use.
