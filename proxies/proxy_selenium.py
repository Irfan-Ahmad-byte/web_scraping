import csv
import random
import time
from selenium import webdriver

def get_working_ip(proxies):
    """
    Returns a working IP address from a list of proxies.

    Args:
        proxies (list): A list of proxies in the format 'IP:port'.

    Returns:
        str: The IP address of a working proxy.
    """
    num_attempts = 0
    while num_attempts < 7:
        proxy = random.choice(proxies)
        if test_ip(proxy):
            print(f"Using IP address: {proxy}")
            return proxy
        else:
            num_attempts += 1
            print(f"IP address {proxy} is blocked. Trying another IP address...")
    return None

def test_ip(ip_address):
    """
    Tests if a given IP address is accessible by opening a browser window and visiting https://www.whatismyip.com/

    Args:
        ip_address (str): The IP address to test.

    Returns:
        bool: True if the IP address is accessible, False otherwise.
    """
    try:
        options = webdriver.ChromeOptions()
        proxy = f"{ip_address}"
        options.add_argument(f"--proxy-server={proxy}")
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.whatismyip.com/')
        time.sleep(5)
        ip = driver.find_element_by_xpath('//span[@class="green"]/strong').text
        driver.quit()
        return ip
    except:
        return None

def main():
    # Read the proxies from the CSV file
    with open('selected_proxies.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        proxies = [row[0] for row in reader]
    
    # Get a working IP address
    ip_address = get_working_ip(proxies)
    if ip_address is None:
        print("All IP addresses are blocked. Aborting...")
        return

    # Set up the browser with the proxy
    options = webdriver.ChromeOptions()
    proxy = f"{ip_address}"
    options.add_argument(f"--proxy-server={proxy}")
    driver = webdriver.Chrome(options=options)

    # Visit Fiverr and get the current IP
    driver.get('https://www.fiverr.com/')
    current_ip = test_ip(ip_address)
    if current_ip is None:
        print("Could not get current IP address. Aborting...")
    else:
        print(f"Current IP address: {current_ip}")

    # Close the browser
    driver.quit()

if __name__ == '__main__':
    main()

