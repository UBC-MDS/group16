library(dash)
library(dashHtmlComponents)
library(geojsonio)
library(leaflet)
library(plotly)
library(htmlwidgets)
library(htmltools)




# INPUT IS A PATH TO A FILE


vancity <- geojsonio::geojson_read("data/map.geojson", what = "sp")




app = Dash$new()


m1 <- leaflet(vancity) %>%
     addProviderTiles("MapBox", options = providerTileOptions(
        id = "mapbox.light",
        accessToken = Sys.getenv('MAPBOX_ACCESS_TOKEN')))

bins <- c(0, 500, 1000, 1500, 2000, 2500, 3000, 3500, Inf)
pal <- colorBin("YlOrRd", domain = vancity$X2021, bins = bins)

labels <- sprintf(
    "<strong>%s</strong><br/>%g Crimes",
    vancity$name, vancity$X2021
) %>% lapply(htmltools::HTML)

m2 <- m1 %>% addPolygons(
    fillColor = ~pal(X2021),
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
#    addLegend(pal = pal, values = ~X2021, opacity = 0.7, title = NULL,
#              position = "bottomright")

saveWidget(m2, file="m.html")

app$layout(htmlDiv(list(htmlIframe(id = "map", srcDoc = htmltools::includeHTML("m.html")))))

app$run_server(debug=T)