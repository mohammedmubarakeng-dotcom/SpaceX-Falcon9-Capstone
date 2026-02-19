SpaceX Falcon 9 Launch Dataset

📁 Dataset Overview

This directory contains all datasets used in the SpaceX Falcon 9 first stage landing prediction project. The data has been organized into {raw} and {processed} directories to maintain data lineage and reproducibility.

📂 Directory Structure
data/
├── raw/ Original, unmodified datasets as collected
└── processed/ Cleaned, transformed datasets ready for analysis


---

🟢 Raw Data (`/data/raw/`)

1. `spacex_web_scraped.csv`
Description: Raw data collected through web scraping from Wikipedia and SpaceX launch records.

| Column           | Description                  | Data Type | Example          |
|------------------|------------------------------|-----------|------------------|
| Flight No.       | Launch sequence number        | Integer   | 1                |
| Launch site      | Launch facility name          | String    | CCAFS            |
| Payload          | Mission payload description   | String    | Dragon CRS-1     |
| Payload mass     | Mass of payload (with units)  | String    | "4,700 kg"       |
| Orbit            | Target orbit type             | String    | LEO              |
| Customer         | Launch customer               | String    | NASA             |
| Launch outcome   | Success/failure of launch     | String    | Success          |
| Version Booster  | Booster version with serial   | String    | F9 v1.1 B1021    |
| Booster landing  | Landing outcome               | String    | Success          |
| Date             | Launch date (original format) | String    | 4 June 2010      |
| Time             | Launch time (UTC)             | String    | 18:45            |




Characteristics:
- Contains 121 launch records
- Raw format with data quality issues
- Mixed date formats
- Payload masses with commas and units
- Inconsistent booster naming
- Special characters and symbols

2. `dataset_part_1.csv`
Description: Initial cleaned version after basic data wrangling, with standardized formats.

| Column         | Description                        | Data Type | Example        |
|----------------|------------------------------------|-----------|----------------|
| FlightNumber   | Launch sequence number             | Float     | 1.0            |
| Date           | Standardized date (YYYY-MM-DD)     | String    | 2010-06-04     |
| BoosterVersion | Falcon 9 version                   | String    | Falcon 9       |
| PayloadMass    | Payload mass in kg (cleaned)       | Float     | 6123.54        |
| Orbit          | Target orbit (standardized)        | String    | LEO            |
| LaunchSite     | Launch site (standardized)         | String    | CCSFS SLC 40   |
| Outcome        | Landing outcome category           | String    | None None      |
| Flights        | Number of flights for booster      | Integer   | 1              |
| GridFins       | Grid fins presence                 | Boolean   | False          |
| Reused         | Booster reuse status               | Boolean   | False          |
| Legs           | Landing legs presence              | Boolean   | False          |
| LandingPad     | Landing pad identifier             | String    | (null)         |
| Block          | Booster block version              | Float     | 1.0            |
| ReusedCount    | Number of times reused             | Integer   | 0              |
| Serial         | Booster serial number              | String    | B0003          |
| Longitude      | Launch site longitude              | Float     | -80.577366     |
| Latitude       | Launch site latitude               | Float     | 28.561857      |


Characteristics:
- 90 launch records
- Standardized date format
- Cleaned numeric payload masses
- Consistent column names
- Geospatial coordinates included

---

 🔵 Processed Data (`/data/processed/`)

3. `dataset_part_2.csv`
Description: Enhanced dataset with binary classification labels for machine learning.

| Column         | Description                          | Data Type | Example        |
|----------------|--------------------------------------|-----------|----------------|
| FlightNumber   | Launch sequence number               | Float     | 1.0            |
| Date           | Launch date                          | String    | 2010-06-04     |
| BoosterVersion | Falcon 9 version                     | String    | Falcon 9       |
| PayloadMass    | Payload mass in kg                   | Float     | 6104.96        |
| Orbit          | Target orbit                         | String    | LEO            |
| LaunchSite     | Launch site                          | String    | CCAFS SLC 40   |
| Outcome        | Detailed outcome                     | String    | None None      |
| Flights        | Number of flights                    | Float     | 1.0            |
| GridFins       | Grid fins (0/1)                      | Float     | 0.0            |
| Reused         | Reused (0/1)                         | Float     | 0.0            |
| Legs           | Landing legs (0/1)                   | Float     | 0.0            |
| LandingPad     | Landing pad ID                       | String    |                |
| Block          | Block version                        | Float     | 1.0            |
| ReusedCount    | Times reused                         | Float     | 0.0            |
| Serial         | Booster serial                       | String    | B0003          |
| Longitude      | Site longitude                       | Float     | -80.577366     |
| Latitude       | Site latitude                        | Float     | 28.561857      |
| Class          | Target Variable (0=failure, 1=success)| Integer   | 0             |


Key Feature:
- Added `Class` column for binary classification
- 90 records with 17 features
- Used for model training and evaluation

4. `dataset_part_3.csv`
Description: One-hot encoded features ready for machine learning algorithms.

| Column Group | Columns | Description |
|--------------|---------|-------------|
| Numerical | FlightNumber, PayloadMass, Flights, Block, ReusedCount | Continuous features |
| Binary | GridFins, Reused, Legs | Boolean flags (0/1) |
| Orbit Dummies | Orbit_ES-L1, Orbit_GEO, Orbit_GTO, Orbit_HEO, Orbit_ISS, Orbit_LEO, Orbit_MEO, Orbit_PO, Orbit_SO, Orbit_SSO, Orbit_VLEO | One-hot encoded orbit types |
| Launch Site Dummies | LaunchSite_CCAFS SLC 40, LaunchSite_KSC LC 39A, LaunchSite_VAFB SLC 4E | One-hot encoded launch sites |
| Landing Pad Dummies | LandingPad_5e9e3032383ecb267a34e7c7, LandingPad_5e9e3032383ecb554034e7c9, LandingPad_5e9e3032383ecb6bb234e7ca, LandingPad_5e9e3032383ecb761634e7cb, LandingPad_5e9e3033383ecbb9e534e7cc | One-hot encoded landing pads |
| Serial Dummies | Serial_B0003 through Serial_B1062 | One-hot encoded booster serials |

Characteristics:
- 90 records with 80+ features
- All categorical variables one-hot encoded
- Ready for scikit-learn models
- No missing values
- All features numeric (float64)

---

Data Pipeline Summary:

Raw Data (spacex_web_scraped.csv)
↓
[Data Wrangling - Notebook 02]
↓
Initial Clean (dataset_part_1.csv)
↓
[Feature Engineering - Notebook 02]
↓
With Class Labels (dataset_part_2.csv)
↓
[One-Hot Encoding - Notebook 02]
↓
ML Ready Features (dataset_part_3.csv)


Data Quality Notes

Raw Data Issues Resolved:
- ✅ Inconsistent date formats → Standardized to YYYY-MM-DD
- ✅ Payload masses with commas → Converted to float
- ✅ Missing values → Handled appropriately
- ✅ Special characters → Cleaned or removed
- ✅ Inconsistent categories → Standardized

Key Statistics:
- Total launches: 90
- Successful landings: 58 (64.4%)
- Failed landings: 32 (35.6%)
- Launch sites: 3 (CCAFS, KSC, VAFB)
- Orbit types: 11
- Date range: 2010-06-04 to 2020-11-05

Recommended Usage

| Dataset | Use Case |
|---------|----------|
| `spacex_web_scraped.csv` | Original source, web scraping practice |
| `dataset_part_1.csv` | Exploratory data analysis, SQL queries |
| `dataset_part_2.csv` | Visualization, correlation analysis |
| `dataset_part_3.csv` | Machine learning model training |

Data Processing Code

The data processing steps are documented in:
- `notebooks/02-data-wrangling.ipynb`
- `notebooks/03-eda-sql.ipynb`

 📜 License

This dataset is provided for educational purposes as part of the IBM Data Science Professional Certificate Capstone project. Original data source: SpaceX launch records and Wikipedia.

---

Last Updated: February 2026
Data Version: 1.0
Records: 90 launches