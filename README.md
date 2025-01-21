<a id="readme-top"></a>
# Spotify Data Analysis Project

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Explore the Project</summary>
  <ol>
    <li><a href="#project-overview">Project Overview</a></li>
    <li><a href="#key-features">Key Features</a></li>
    <li><a href="#folder-structure">Folder Structure</a></li>
    <li><a href="#technology-stack">Technology Stack</a></li>
    <li><a href="#setup-and-installation">Setup and Installation</a></li>
    <li><a href="#future-enhancements">Future Enhancements</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## Project Overview

This project focuses on analyzing **Spotify's Top 50 playlists** from various countries worldwide, as well as the global Top 50 playlist, retrieved using the **Spotify API**. To complement missing artist genre data, the project integrates the **Discogs API**, enriching the analysis with a more comprehensive understanding of musical styles. Additionally, **web scraping** techniques are utilized to group genres into broader categories, enhancing the clarity and depth of the analysis.

The application offers a user-friendly interface built with **Streamlit**, allowing users to visualize music trends interactively. By leveraging a combination of API integrations, web scraping, and interactive dashboards, this project provides valuable insights into how music preferences vary across regions and within a global context.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Key Features

- **Data Collection**:
  - Retrieved Top 50 playlists globally and for multiple countries using the **Spotify API**, including detailed track, album, and artist data.
  - Augmented genre data by querying the **Discogs API** to fill in missing information.
  - Implemented web scraping for genre grouping to improve consistency and analysis.

- **Data Processing**:
  - Cleaned, structured, and standardized raw data into preprocessed datasets, ensuring readiness for analysis.
  - Applied column renaming and genre classification for consistency across datasets.

- **Data Storage**:
  - Organized raw and processed data into structured folders.
  - Stored preprocessed datasets as CSV files for easy accessibility and reusability.
  - Utilized **Amazon S3** for secure storage and retrieval of data.

- **Analysis and Visualization**:
  - Built a user-friendly dashboard using **Streamlit** for interactive visualizations and data exploration.
    - **Data Preview**: Review raw data, summaries, and insights about playlists, tracks, artists, and albums. Provides an overview of key statistics such as total playlists, average followers, and unique track counts. Includes descriptive statistics for playlists, albums, artists, and tracks with interactive tabs.
    - **Playlist Analysis**: Analyze playlist-level data, including total followers by country, the most and least followed playlists, track popularity distribution by country, and top 10 tracks and artists by frequency in Playlists. Features visualizations like choropleth maps, bubble plots, boxplots sorted by median popularity, histograms, and bar plots.
    - **Tracks Analysis**: Explore track-level data such as the distribution of popularity, top 10 most popular tracks, analysis of explicit and non-explicit tracks, and the relationship between track duration and popularity with trendlines. Includes visualizations like histograms, bar plots, scatter plots, and boxplots.
    - **Artists Analysis**: Delve into artist-level data, including the distribution of artist popularity, the most popular artists by popularity and followers, genre distributions, and geographic analysis of artist presence. Features polar charts, heatmaps, choropleth maps, histograms, and bar plots.
    - **Album Insights**: Gain insights into album-level data, including the distribution of album popularity, top albums by popularity, seasonality of releases, and album type distribution. Includes visualizations such as histograms, bar plots, line charts, and pie charts.
      
- **Logging and Debugging**:
  - Implemented detailed logging for API calls, data processing, and debugging, ensuring traceability throughout the workflow.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Folder Structure

```
Spotify-Data-Analysis
├── .streamlit
├── config
│   ├── config.yaml                # Configuration for APIs and project settings
│   ├── country_coords.yaml        # Country-specific coordinates for analysis
│   ├── path_config.yaml           # Paths to raw and processed data
│   └── s3_files.yaml              # S3 configurations 
├── data
│   ├── genres
│   │   ├── additional_genres.yaml # Additional genre mappings
│   │   └── genres.yaml            # Genre classifications
│   ├── preprocessed
│   │   ├── albums.csv             # Preprocessed albums data
│   │   ├── artists_full.csv       # Preprocessed artists data
│   │   ├── playlists.csv          # Preprocessed playlists data
│   │   └── tracks.csv             # Preprocessed tracks data
│   └── raw
│       └── playlists              # Raw JSON files of playlists
├── images                         # Placeholder for visualization outputs
├── logs
│   ├── app.log                    # Application logs
│   └── logger_config.py           # Logging configuration
├── pages                          # Modular scripts for Streamlit dashboard
│   ├── albums_analysis.py
│   ├── artists_analysis.py
│   ├── data_preview.py
│   ├── playlists_analysis.py
│   └── tracks_analysis.py
├── source                         # Source code for APIs and preprocessing
│   ├── api
│   │   ├── discogs.py             # Interactions with Discogs API
│   │   ├── s3_functions.py        # Functions for interacting with Amazon S3 
│   │   ├── secrets_functions.py   # Secure token handling
│   │   └── spotify.py             # Interactions with Spotify API 
│   ├── preprocessing
│   │   └── data_prep.py           # Data preprocessing pipeline
|   ├── web_scraping/              # Web scraping utilities
|       └── chosic.py              # Scrapes genres and subgenres from Chosic
│   └── utils.py                   # Utilities for configuration management and S3 synchronization
├── streamlit_utils                # Utilities for Streamlit dashboard
│   ├── data_processing.py
│   ├── layouts.py
│   └── plots.py
├── download_preprocess_data.py    # Script to automate data collection and preprocessing
├── streamlit_app.py               # Main Streamlit app
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation (this file)
└── .gitignore                     # Files to ignore in version control
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Technology Stack
- **Programming Language**: Python
- **APIs**: Spotify API, Discogs API
- **Visualization**: Streamlit
- **Data Processing**: Pandas
- **Web Scraping**: BeautifulSoup, Requests
- **Cloud Storage**: Amazon S3
- **Version Control**: Git, GitHub

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---


## Setup and Installation

_This is an example of how you may give instructions on setting up your project locally. Follow these steps to run the project:_

1. Clone the repository:
   ```bash
   git clone https://github.com/Viktoriia-Shalaieva/Spotify-Data-Analysis.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Spotify-Data-Analysis
   ```   
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Optional**: Create a `.credentials.yaml` file in the main directory with the following structure:
   ```yaml
   aws:
     aws_access_key_id: YOUR_AWS_ACCESS_KEY_ID
     aws_secret_access_key: YOUR_AWS_SECRET_ACCESS_KEY

   spotify:
     client_id: YOUR_SPOTIFY_CLIENT_ID
     client_secret: YOUR_SPOTIFY_CLIENT_SECRET

   discogs:
     discogs_api_token: YOUR_DISCOGS_API_TOKEN
   ```

   - Replace `YOUR_AWS_ACCESS_KEY_ID` and `YOUR_AWS_SECRET_ACCESS_KEY` with your AWS credentials.
   - Replace `YOUR_SPOTIFY_CLIENT_ID` and `YOUR_SPOTIFY_CLIENT_SECRET` with your Spotify API credentials. You can obtain these by creating an app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Replace `YOUR_DISCOGS_API_TOKEN` with your Discogs API token, available from your [Discogs developer account](https://www.discogs.com/settings/developers).

   > **Note**: This step is required only if you intend to run the `download_preprocess_data.py` script to update the data.

5. **Optional for updating data**: Run the data preprocessing script:
   ```bash
   python download_preprocess_data.py
   ```
   > **Note**: As of [November 27, 2024](https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api), Spotify has deprecated access to playlist API endpoints. If you don't have access to the Spotify API, you can skip this step and use the local data provided in the `data/` folder.

6. Launch the Streamlit dashboard:
   ```bash
   streamlit run streamlit_app.py
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

---
## Future Enhancements
- Advanced trend analysis using machine learning models.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---
## Contact
For any inquiries or collaboration opportunities, please feel free to contact me via [LinkedIn](https://linkedin.com/in/viktoriia-shalaieva) or [email](mailto:viktoriia.shalaieva@gmail.com).
<p align="right">(<a href="#readme-top">back to top</a>)</p>

--- 

Start exploring music trends today with the **Spotify Data Analysis App**! 🎶
