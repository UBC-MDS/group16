library(dash)
library(dashBootstrapComponents)
library(dashHtmlComponents)
library(dashCoreComponents)
library(broom)
library(rgdal)
library(dplyr)
library(plotly)
library(ggplot2)

app <- Dash$new(external_stylesheets = dbcThemes$BOOTSTRAP)

app$layout(
    dbcContainer(
        list(
            dccDropdown(
                id='y-select',
                options = list(list(label = "2017", value = "2017"),
                               list(label = "2018", value = "2018"),
                               list(label = "2019", value = "2019"),
                               list(label = "2020", value = "2020"),
                               list(label = "2021", value = "2021")),
                value = '2021'
            ),
            dccGraph(id='plot-area')
        )
        
        )
    )

app$callback(
    output('plot-area', 'figure'),
    list(input('y-select', 'value')),
    function(year) {
        df <- read.csv("map_df2.csv") %>% 
            filter(YEAR==year) 
        url_geojson <- "https://raw.githubusercontent.com/UBC-MDS/vancouver_crime_dashboard/main/data/vancouver.geojson"
        geojson <- rgdal::readOGR(url_geojson)
        geojson2 <- broom::tidy(geojson, region = "name")
        geojson2 <- geojson2 %>%
            left_join(df, by = c("id" = "Neighborhood"))

        p <- ggplot() +
                geom_polygon(data = geojson2, 
                aes(x = long, y = lat, group = group, fill = Count)) +
                scale_fill_gradient(low = "yellow2", high = "red3", na.value = NA)

        ggplotly(p)
    }
)


app$run_server(debug = T)
