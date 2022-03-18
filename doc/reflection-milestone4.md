## Reflection

### Summary

We achieved the dashboard we planned in week one, including three main plots, a card, and a filter panel. We have received positive feedback on the dashboard structure and length of the data period covered, which provides users better insight through trend analysis. We strived to create the DashR and DashPy app in a way that delivers the same visualization and functionalities.

Beyond our original proposal, we added more details to improve the usage scenarios based on the feedback. Users now can filter the crime data based on the neighbourhood(s), year, and time of the day. The dashboard also provides the link to the original dataset. 

### Improvements
From the feedback, we have made major improvements on the following

- We added an information section at the bottom of the left filter panel,  which provides the link to the Vancouver Police Department Open Data.
- We changed the Neighbourhood filter from the dropdown list to a collapse button, allowing the user to select multiple neighbourhoods simultaneously.
- We updated the map from circles to a choropleth map. The colour (from yellow to red) represents the crime counts from low to high, improving visual appeal and functionality. 
- We changed the bar chart to display the top 5 crimes by type for crucial information. We also updated the legend position to show full crime names. 
- We updated the dashboard icon and added attribution.
- We updated the README with a new demo to show added functionalities.

### Future Plans

There are some functionalities we are unable to implement given the time constraints but planned for the future advance

1. The dashboard focuses on neighbouhoods statistics while users may also be interested in the overall crime status of Vancouver city. We can add Vancouver-all as an option that allows users to understand the general crime trends and compare them with neighbourhhods. 
2. Due to privacy concerns, we did not collaborate with the geospatial information from the dataset. However, we can potentially narrow the selection by breaking neighbourhood into blocks, which could help users for better location decisions. 
