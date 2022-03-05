# Vancouver Crime Dashboard
Link to the dashboard: [Vancouver Crime Dashboard](https://vancouver-crime-dashboard.herokuapp.com/)

## Motivation
Safety is an important factor for consideration when choosing a place to live. Vancouver is a major destination city for immigrants from all over the world and Canadians looking to relocate within Canada. Our dashboard visualizes crime data in Vancouver and helps newcomers decide where to move to, depending on how safe specific neighborhoods are. In addition, we provide general information, such as trends in crimes in Vancouver for the past five years and the number of crimes at different times of day, to increase newcomers' understanding of public safety and crime in Vancouver as a whole as you make your decision to relocate.

## Description of the dashboard

https://user-images.githubusercontent.com/67261289/156861936-a38e4f9a-06d6-4430-82e8-8a8896b06fb8.mp4

The Vancouver crime statistics dashboard displays criminal incidents that occurred over the past 5 years under the Vancouver Police Department jurisdiction.

On the left, there is a panel that enables filtering the data by neighbourhood and defining a year range.

Right above the filtering panel, on the top-left corner, there is a summary statistic that shows the total number of crimes for the user-selected neighbourhood and year.

A bar chart depicts the count of crimes by type, based on the global criteria mentioned above, enabling analysis of most frequent crimes by neighbourhood.

The map of Vancouver is presented in the right upper corner, with its corresponding number of crimes by neighbourhood as circles. As the number of crimes increases, the size of the circles also increases. Additionally, the map shows the number of crimes as a tooltip when the user hovers over different areas of the city.

The final graph is a time series that illustrates the crimes that happened in the past five years. Moreover, the user can turn on a specific toggle from the filtering panel to segregate the crimes by the time of the day when the incident occurred (day, night or both) and inspect trends.

### Installation

You can download this file, create a conda environment and activate it as follows.
```
conda env create -f environment.yaml
conda activate van-crime
```
You can view the source code in `src/app.py`.

### Run locally

Make sure you are in the root directory of the repository. Then, run the following command in Terminal:
```
python src/app.py
```
You will be given an URL to use the dashboard.


### Contributing

Contributors: Cici Du, Melisa Maidana, Paniz Fazlali, Shi Yan Wang (DSCI 532 - Group 16).

Interested in contributing? Check out the contributing guidelines.

We would love to know what other datasets we can bring into our dashboard to make it more useful. Please also feel free to offer suggestions on other interactive options you'd like to see.

Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

### License

This dashboard was created by Cici Du, Melisa Maidana, Paniz Fazlali, Shi Yan Wang (DSCI 532 - Group 16).

It is licensed under the terms of the MIT license.
