# **UMLS-BMKG: Node and Edge CSV Generator for UMLS RRF Files**

This repository provides a Python-based, fully automated pipeline for converting **UMLS Rich Release Format (RRF)** files into **nodes.csv** and **edges.csv** files suitable for building a Biomedical Knowledge Graph (BMKG).
It is designed to support research workflows that require transforming UMLS relational resources into property-graph–compatible formats (e.g., Neo4j, TigerGraph, NebulaGraph).


## **Overview**

The scripts in this repository perform:

* Parsing of UMLS **MRCONSO**, **MRREL**, and **MRSTY** RRF files
* Generation of:

  * **nodes.csv** — concept nodes with semantic types and source vocabulary metadata
  * **edges.csv** — relationship edges standardized with provenance fields
* Automatic filtering, normalization, and structuring of UMLS data
* Exporting graph-ready files that can be directly loaded into any property-graph database


## **Prerequisites**

### 1. **UMLS License**

To use this pipeline, you must have a valid UMLS Metathesaurus license:
[https://www.nlm.nih.gov/research/umls/](https://www.nlm.nih.gov/research/umls/)

After obtaining the license, download the latest UMLS release and extract the RRF files.

### 2. **Python 3.8+**

Install dependencies:

```bash
pip install -r requirements.txt
```


## **How to Run**

1. Place the following UMLS RRF files in a directory:

   * `MRCONSO.RRF`
   * `MRREL.RRF`
   * `MRSTY.RRF`

2. Update the input paths inside the Python script.

3. Run the script to generate the graph files:

```bash
python build_nodes.py
python build_edges.py
```

4. Output files will be generated:

```
output/
 ├── nodes.csv
 └── edges.csv
```

These files can be imported into Neo4j or any property-graph system.


## **Important Note on Licensing**

This repository **does not contain** or redistribute UMLS RRF datasets.
Users must download UMLS files manually in compliance with:

* **UMLS Terms of Use**
* **NLM Licensing & Data Restrictions**

The scripts in this repository operate only on locally provided licensed files.

