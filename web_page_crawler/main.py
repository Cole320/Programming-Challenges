from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Configure webdriver
driver_options = Options()

driver = webdriver.Chrome(options=driver_options)

# Load Vultr Docs Site
driver.get("https://www.vultr.com/docs/category/databases/")

# Look Through Docs Site to Find All Categories
category_elements = driver.find_elements_by_class_name("nav__link")
category_links = []

for element in category_elements:
    if ".com/docs/category" in element.get_attribute("href") and element.get_attribute("href").replace("#",
                                                                                                       "") not in category_links:
        category_links.append(element.get_attribute("href").replace("#", ""))

print("Found " + str(len(category_links)) + " Categories:")
print(*category_links, sep="\n")

with open("categories", "a") as file:
    for category in category_links:
        file.write(category + "\n")

# Loop Through All Categories to Find All Articles
articles = []

for category_link in category_links:
    valid_page = True
    current_page = 1

    while valid_page:
        page = category_link + "?page=" + str(current_page)
        success = False
        while not success:
            driver.get(page)

            if "Error 32e5238" in driver.find_element_by_tag_name("body").text:
                print("[Rate Limit - Retrying]")
                time.sleep(5)
            else:
                success = True

        page_element = driver.find_elements_by_class_name("list-group__item")

        for element in page_element:
            articles.append(element.get_attribute("href"))

        if not len(page_element):
            valid_page = False

        current_page += 1

print("-"*25)
print("Found " + str(len(articles)) + " Articles:")
print(*articles, sep="\n")

with open("articles", "a") as file:
    for article in articles:
        file.write(article + "\n")

# Iterate Through Articles to Find Out of Date Articles
archived_articles = []

for article in articles:
    success = False

    # Rate Limit Prevention
    while not success:
        driver.get(article)

        if "Error 32e5238" in driver.find_element_by_tag_name("body").text:
            print("[Rate Limit - Retrying]")
            time.sleep(5)
        else:
            success = True

    # Check if Article is Outdated
    if "Archived content" in driver.find_element_by_tag_name("body").text:
        archived_articles.append(article)


print("-"*25)
print("Found " + str(len(archived_articles)) + " Archived Articles:")
print(*archived_articles, sep="\n")

with open("archived_articles", "a") as file:
    for article in archived_articles:
        file.write(article + "\n")

# Close the webdriver
driver.close()
