ETL pipeline with OpenSea API

<p>Application that handles data extraction transformation and load processes.</p>
<p>Data is extracted from opensea api. the project curretly is focused in ethereum collections.</p>
<p>App has database manager module (CUSTOM ORM), that handles database creation and connection processes,crud operations on tables, crud operations on models(collections).data filtering functionality such as selecting rows using operators like like, ilike, in, ordered,limited etc..</p>
<p>Apps file manager and data manager classes is responsible for data extraction from opensea api, data transformation and load processes</p>
<p>Currently for data lake i use local machine.Extracted data is saved in json and csv formats and is version controlled using timestamp.</p>

### Future improvements

1. **load data asynchronously in a local data lake.**
1. **make database io bound tasks asynchronous.**

### Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)

### Prerequisites

- <img src="readme/assets/python.png" width="25" style="position: relative; top: 8px" /> _Python @3.X and up_

#

### Getting Started

1. **Clone the repository**:

   ```bash
   git clone https://github.com/NikaKhiz/sweeft_etl_pipeline.git
   cd sweeft_etl_pipeline
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install all of the necessary libraries**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Generate .env file from .env.example and provide necessary variable values**:

   ```bash
   cp .env.example .env
   ```

## Usage

**Run scripts**:

- Simply run the `python main.py` command in the root directory:

```bash
python main.py
```

### the code above will fetch etherium based collections from opensea api, transform and save it in to the database and raw data will be saved as json and csv in local data lake.
