from bs4 import BeautifulSoup
import json
import sys

# Load the HTML file
with open("index.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

file = open('rules.json')
rules = json.load(file)

# site config
for config, value in rules['configs']:

    # Define the tag you want to identify in the HTML
    tag_to_convert = config  # Change this to the HTML element you want to convert
    if hasattr(config['loop']):
        # for looping
        loop_variable = value
    else:
        # for value converting
        # Define the variables for injecting into Blade
        php_variable = value

        # Find all instances of the tag you want to convert
        elements_to_convert = soup.find_all(tag_to_convert)

        # Iterate through the found elements and replace with Blade syntax
        for element in elements_to_convert:
            # Replace the content of the HTML tag with Blade syntax
            if (tag_to_convert.find("src")):
                element['src'] = php_variable
            elif (tag_to_convert.find("href")):
                element['href'] = php_variable
            elif (tag_to_convert.find("onclick")):
                element['onclick'] = php_variable
            else:
                element.string = php_variable  # Inject a PHP variable

            # You can also convert the tag into a Blade loop
            # For example, uncomment the following lines to create a foreach loop
            # element.name = "foreach"
            # element['items'] = f"{loop_variable}"
            # element.insert(0, f"@foreach({loop_variable} as ${loop_variable})")

# Save the modified HTML content as a Laravel Blade file
with open("index.blade.php", "w", encoding="utf-8") as output_file:
    output_file.write(str(soup))

print("HTML file has been converted to a Laravel Blade file and saved as 'output.blade.php'")
