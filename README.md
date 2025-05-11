IMDb_2024_Movies

🎬 IMDb 2024 Movie Visualization Dashboard

Welcome to the IMDb 2024 Dashboard, an interactive data visualization project built using Streamlit, Python, MySQL, and Selenium. This dashboard offers insights into 2024's movies across genres like horror, adventure, fantasy, animation, and family by presenting dynamic visual analytics.

🚀 Project Overview

With a growing number of movie releases every year, filtering quality content can be a challenge. This project solves that by collecting and visualizing IMDb movie data from 2024. From scraping and storing to analyzing and presenting, the project captures the entire data pipeline for genre-based movie analysis.

We used Selenium to automate the scraping of IMDb for metadata like titles, ratings, votes, and durations. The data is cleaned using Pandas, stored in a MySQL database, and displayed through a rich Streamlit dashboard with interactive filtering and visual storytelling.

🧰 Tech Stack

Python (Pandas, Matplotlib, Seaborn, Plotly)

Streamlit – for interactive dashboard UI

MySQL – for structured data storage

Selenium – for web scraping automation

🔄 Project Workflow

⚡ 1. Data Collection (Selenium Web Scraping)

Scraped IMDb pages using automated Selenium scripts.

Collected movie metadata:

Title

Genre

IMDb Rating

Duration

Voting Counts

Saved each genre's data as a .csv file.

⚡ 2. Data Cleaning & Preprocessing

Processed raw .csv files using Pandas.

Standardized and formatted features.

⚡ 3. Database Storage (MySQL)

Created a MySQL database imdb_genre_2024.

Loaded cleaned data into the movies_genre_2024 table.

Connected dashboard using SQLAlchemy for real-time querying.

⚡ 4. Interactive Dashboard (Streamlit)

Built a modern UI with Streamlit.

Implemented filters: genre, rating, votes, duration.

Added interactivity with Plotly, Matplotlib, and Seaborn charts.

📊 Dashboard Features

🏅 Top 10 Movies by Rating & Votes – Bar charts

📊 Genre-wise Movie Count – Distribution plot

⏱️ Average Duration by Genre – Horizontal bar

🗳️ Voting Trends by Genre – Bar chart

⭐ Rating Distribution – Histogram

🏆 Top-Rated Movies by Genre – Data table

🥧 Popular Genres by Votes – Pie chart

🎬 Shortest & Longest Movies – Summary cards

🔥 Ratings by Genre – Heatmap

📈 Votes vs Ratings Correlation – Scatter plot

📁 Repository Structure
├── imdb_scraper.ipynb         # Selenium-based scraper for genre data
├── imdb_dashboard.py          # Streamlit dashboard source code
├── *.csv                      # Cleaned CSV files for each genre
├── README.md                  # Documentation

🙌 Acknowledgements

IMDb for providing accessible movie metadata.

Open-source contributors of Pandas, Selenium, Plotly, Streamlit, and Seaborn.

📬 Contact

For queries or collaborations, feel free to reach out:

LinkedIn: [Saranya Balu](https://www.linkedin.com/in/saranya-balu25/)

GitHub Issues: Open a ticket in this repository
