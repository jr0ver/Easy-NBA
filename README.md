# Easy-NBA

**Easy-NBA** is a Flask-based web application designed to be the all-in one experience for NBA statistical data. It uses a combination of web scraping, database management, and machine learning to provide an immersive experience in visualizing, comparing, analyzing, and predicting career statistical data. After initial web requests to query for any NBA  player data, Easy-NBA stores the data in a MySQL database for quick DB access and operations. With this large custom dataset, users are able to compare players, generate player overviews, list achievements, rank player similarity using machine learning, and a whole lot more. With a local environment created through SQLite and a hosted option with MySQL, **Easy-NBA** provides two methods of using the app.

**Easy-NBA** is feature-heavy as mentioned above, but has a wide range of future advancements due to the many possibilities of the custom dataset. With some clean up tasks to go, **Easy-NBA** will soon be ready for deployment!

## Features and Usage
- (to be listed soon with images)

## Technologies Used

- **Backend/Frontend**: Python Flask, JavaScript, HTML/CSS
- **Data Handling/Visualization**: Jupyter, Pandas, BeautifulSoup, Seaborn, Plotly
- **Database**: MySQL, SQLite
- **Machine Learning**: Scikit-learn

## Deployment/Installation

#### Option 1: Visit Deployment

- Awaiting future hosting and deployment -

#### Option 2: Installing through Git

1. Clone the repository using Git:
    ```bash
    git clone https://github.com/zsspan/Easy-NBA
    ```
2. Start the server via (run.py)
    ```bash
    python3 run.py
    ```

## Data

The main data used for some calculations is a large 'master-table' containing rows of career data among many players. With the helper file in the utils directory, players can continue to scrape for players and add to the dataset. This dataset is currently updated in the MySQL version of the app, but users can access the SQLite version for a local experience
