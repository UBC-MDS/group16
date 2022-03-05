## Reflection

### Summary

Our dashboard contains three main plots, a card and a filter panel.

The bar plot shows counts of crimes by crime type and it can be filtered by neighbourhood and year. The map layered with a scatter plot shows Vancouver neighborhoods and the sizes of the scatter plot elements are proportional to the count of crimes in those neighborhoods. This map can be filtered year. Finally, our line plot can be filtered by time of day, so the user can visualize count of crimes by day, night or both across the past 5 years. The card can be filtered by both neighborhood and year.

### Evaluation
Our dashboard serves its purpose of providing information of safety and crime for Vancouver current and potential residents. The interactive elements that we have incorporated help the users gain more control over what they want to see and are easy to use and intuitive to understand.

### Limitations and Improvements

In terms of limitations, we think there are mainly two areas we can focus on.

1. When we implemented the map, we had to drop rows from the dataset where the geospatial information is unavailable due to privacy concerns. We can potentially add another filter that controls whether we filter our dataset in this way, because right now the other two plots are also affected and the information we are providing might be limited due to this data issue.

2. We implemented the neighborhood filter as a dropdown menu, but this limits the number of neighborhood inspection to one. We can potentially use a different type of filter component so users can pick more than one choice.

In addition to these two areas, we can potentially bring in another dataset for Vancouver population and derive per capita crime data from it as it wouldn’t be fair to only compare the number of crimes when the population in each neighborhood can vary. Adding this additional information can provide more context and promote better understanding of crime in Vancouver. 
