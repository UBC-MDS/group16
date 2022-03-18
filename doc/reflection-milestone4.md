## Reflection

### Summary

We achieved the dashboard we planned in week one, including three main plots, a card, and a filter panel for DashPy and DashR with a user-friendly interface. Users can filter the crime statistics of Vancouver from 2017 to 2021 by Neighbourhood, Year, and Time of the day.

We created the DashPy and DashR that deliver the exact visualization and functionalities. The only difference is for Crimes by Type (top left bar chart). DashPy displayed the Top 5 crimes for the selected criteria with the legend at the bottom, while DashR displayed all crime types in descending order without a legend but tooltips interactivity. 

Based on the feedback, users enjoyed the interface of the dashboard and the length of data it covers, allowing them to explore the long-term trend of the issue. We also improved our dashboard beyond the original proposal by taking advice from reviewers.

### Improvements on DashPy

From the feedback, we have made major improvements on the following

- Added a description section under the dashboard title through the Learn more collapse button. 
- Included an information section for the link to the open data at the bottom of the left filter panel. 
- Changed the Neighbourhood filter from the dropdown list to a collapse button, allowing users to select multiple neighbourhoods simultaneously.
- Updated the map from circles to a choropleth map. The colour (from yellow to red) represents the crime counts from low to high.
- Switched the bar chart from displaying all crime types to the top 5. 
- Updated the favicon to better fit the usage scenario

### Limitations and Improvements on DashR

We strived to create DashR and DashPy to deliver the exact visualization and functionalities. However, we faced difficulties pushing the DashR to Heroku due to package incompatibility for the map component. 

To solve the problem, we took the advice from @florencia to provide instructions on how to access the DashR locally, given the time constraints. We have planned to explore more DashR options for map visualizations with other packages for the next step.

### Future Plans

There are some functionalities we plan for the future advance

1. The dashboard focuses on neighbouhoods statistics while users may also be interested in the overall crime status of Vancouver city. We can add Vancouver-all as an option that allows users to understand the general crime trends and compare them with neighbourhhods. 
2. Due to privacy concerns, we did not collaborate with the geospatial information from the dataset. However, we can potentially narrow the selection by breaking neighbourhood into blocks, which could help users for better location decisions. 
