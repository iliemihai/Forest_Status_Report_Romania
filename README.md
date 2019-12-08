# Forest Status Report Romania

In this repository, we extract text from PDF file report, process it and after push it into Spacy pipeline for name entity extraction.
Afterwards, the extracted results are ploted in a map.
The PDF document represents a report of Romanian Ministry of Water and Forests. It was released in 2017 and represents the forest status.

## Requirements

This project uses the following Python libraries

* `PyPDF2`
* `spaCy` : Used for name entity extraction in Romanian
* `NumPy` : Used for matrix multiplication
* `pandas` : Data analytcs tool
* `matplotlib` : Creating plots tool
* `seaborn` : Creating plots tool
* `geopandas` : Ploting maps tool

## Word counts

The plot bellow represents the moust frequent words used in a document.
![States Count](./scripts/images/words_counts.png)

## Mentions per county

The plot bellow represents how many times the name of each county appears in the document. This can be viewed as a metric which outputs the counties which have the biggest problems with deforestation.

![States Count](./scripts/images/map_2017.png)
