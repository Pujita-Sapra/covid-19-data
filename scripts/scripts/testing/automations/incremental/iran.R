urls <- read_html("https://irangov.ir/ministry-of-health-and-medical-education") %>%
    html_nodes(".list-content-body a") %>%
    html_attr("href") %>%
    paste0("http://irangov.ir", .)

for (url in urls) {
    page <- read_html(url)

    date <- page %>%
        html_node(".content_detail_date") %>%
        html_text %>%
        str_squish() %>%
        ymd_hms() %>%
        date()

    count <- page %>%
        html_node(".content_detail_body") %>%
        html_text() %>%
        str_extract("[\\d,]+\\sCOVID-19 tests have been taken across the country") %>%
        str_extract("^[\\d,]+") %>%
        str_replace_all("[^\\d]", "") %>%
        as.integer()

    if (!is.na(count)) break
}

stopifnot(!is.na(count))

add_snapshot(
    count = count,
    date = date,
    sheet_name = "Iran",
    country = "Iran",
    units = "tests performed",
    testing_type = "PCR only",
    source_url = url,
    source_label = "Government of Iran"
)
