from sheep_scraper import SheepScraper

if __name__=='__main__':
    find_them = SheepScraper()
    find_them.scrape_geojson()
    find_them.append_to_the_herd_history()
