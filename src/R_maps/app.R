library(dash)
library(dashHtmlComponents)
library(geojsonio)
library(leaflet)
library(plotly)
library(htmlwidgets)
library(htmltools)


app <- Dash$new(external_stylesheets = dbcThemes$BOOTSTRAP)

app$layout(dbcContainer(
        list(
            dccDropdown(
                id='y-select',
                options = list(list(label = "2017", value = "2017"),
                               list(label = "2018", value = "2018"),
                               list(label = "2019", value = "2019"),
                               list(label = "2020", value = "2020"),
                               list(label = "2021", value = "2021")),
                value = '2017',
                persistence=TRUE,
                persistence_type='session'
            )
            ,
            htmlDiv(list(htmlIframe(id = "map")))
            )

    )
)


app$callback(
    output('map', 'srcDoc'),
    list(input('y-select', 'value')),
    function(yyyy) {
        file = switch(yyyy,
        '2021' = "data/map2021.geojson",
        '2020' = "data/map2020.geojson",
        '2019' = "data/map2019.geojson",
        '2018' = "data/map2018.geojson",
        '2017' = "data/map2017.geojson")
        vancity <- geojsonio::geojson_read(file, what = "sp")
        m1 <- leaflet(vancity) %>%
            addProviderTiles("MapBox", options = providerTileOptions(
                id = "mapbox.light",
                accessToken = Sys.getenv('MAPBOX_ACCESS_TOKEN')))
        bins <- c(0, 500, 1000, 1500, 2000, 2500, 3000, 3500, Inf)
        pal <- colorBin("YlOrRd", domain = vancity$year, bins = bins)
        labels <- sprintf(
            "<strong>%s</strong><br/>%g Crimes",
            vancity$name, vancity$year
        ) %>% lapply(htmltools::HTML)
        m2 <- m1 %>% addPolygons(
            fillColor = ~pal(year),
            weight = 2,
            opacity = 1,
            color = "white",
            dashArray = "1",
            fillOpacity = 0.7,
            highlightOptions = highlightOptions(
                weight = 5,
                color = "#666",
                dashArray = "",
                fillOpacity = 0.7,
                bringToFront = TRUE),
            label = labels,
            labelOptions = labelOptions(
                style = list("font-weight" = "normal", padding = "3px 8px"),
                textsize = "15px",
                direction = "auto")) #%>%
        #    addLegend(pal = pal, values = ~year, opacity = 0.7, title = NULL,
        #              position = "bottomright")
        saveWidget(m2, file="m.html")
        htmltools::includeHTML("m.html")
    }
)

app$run_server(debug=T)