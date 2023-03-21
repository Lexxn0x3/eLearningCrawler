import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

#                                            Put your configuration here
#####################################################################################################
# Define the login credentials
username = "your_username"
password = "your_password"

# Define the login URL, should be this
login_url = "https://elearning.ohmportal.de/login/index.php"

# URL of the Moodle page containing the files
url = "https://elearning.ohmportal.de/course/view.php?id=1234"

#replace with your desired file types
fileTypes = {".pdf", ".mp4", ".xlsx", ".xls", ".txt"}

#replace with your desired save path
save_location = "C:\\Users\\your_username\\Desktop\\Download"

###########################################################################################################
#                                               End configuration

def isWantedFile(href, fileTypes):
    for type in fileTypes:
        if href.endswith(type):
            return True
    return False

# Create a session object
session = requests.Session()

# Send a GET request to the login page to retrieve the login form
login_page = session.get(login_url)

# Parse the HTML of the login page using BeautifulSoup
soup = BeautifulSoup(login_page.content, 'html.parser')

# Find the login form and extract the required form data
form = soup.find('form', {'id': 'login'})
login_data = {
    'username': username,
    'password': password,
    'logintoken': form.find('input', {'name': 'logintoken'})['value'],
    'rememberusername': 1,
}

# Submit the login form to the Moodle site
session.post(login_url, data=login_data)

# Fetch the HTML of the page containing the PDF files
pdf_page = session.get(url)

#save page
with open(save_location + "\\page.html", 'wb') as f:
    f.write(pdf_page.content)

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(pdf_page.content, 'html.parser')

# Find all the links on the page
links = soup.find_all('a')

for link in links:
    href = link.get('href')

    #continue if not resource
    try:
        if "/mod/resource/" not in href:
            continue
    except:
        continue

    # Check if the link points to a PHP resource
    if href and 'view.php' in href:
        # Fetch the HTML of the PHP resource
        #php_url = url + href
        php_url = href;
        response = session.get(php_url)
        html = response.content

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Find all the links on the page
        linksPhp = soup.find_all('a')

        # Loop through all the links on the page
        for linkPhp in linksPhp:
            hrefPhp = linkPhp.get('href')

            # Check if the link points to a PDF file
            #if hrefPhp.endswith('.pdf'):
            if isWantedFile(hrefPhp, fileTypes):
                # Get the filename from the URL and replace % with a space
                filename = os.path.basename(urllib.parse.unquote(hrefPhp))

                # Join the specified location and modified filename
                save_path = os.path.join(save_location, filename)

                # Check if the directory exists, and create it if it doesn't exist
                if not os.path.isdir(save_location):
                    os.makedirs(save_location)

                # Download the file
                print("downloading " + hrefPhp +"  (" + filename +")" + "...")
                responsePhp = session.get(hrefPhp)
                with open(save_path, 'wb') as f:
                    f.write(responsePhp.content)
                print("Done\n")
print("Everyting Downloaded... (I hope) :D")