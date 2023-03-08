import csv
import random
import time

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType


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
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = ip_address
        proxy.ssl_proxy = ip_address
        options.add_argument(f'--proxy-server={ip_address}')
        driver = webdriver.Remote(command_executor='http://localhost:4444', options=options)
        driver.get('https://www.whatismyip.com/')
        time.sleep(5)
        driver.quit()
        return True
    except Exception as e:
        raise e


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


def use_proxies(url, num_tries=3):
    """
    Visits a website using different proxy IPs until successful.

    Args:
        url (str): The URL to visit.
        num_tries (int): The number of attempts to make before giving up. Default is 3.

    Returns:
        None
    """
    # Read the proxies from the CSV file
    with open('selected_proxies.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        proxies = [row[0] for row in reader]

    num_attempts = 0
    while num_attempts < num_tries:
        ip_address = get_working_ip(proxies)
        if ip_address is None:
            print("All IP addresses are blocked. Aborting...")
            return

        try:
            options = webdriver.ChromeOptions()
            proxy = Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = ip_address
            proxy.ssl_proxy = ip_address
            options.add_argument(f'--proxy-server={ip_address}')
            driver = webdriver.Remote(command_executor='http://localhost:4444', options=options)
            driver.get(url)
            print(f"Using IP address: {ip_address}")
            time.sleep(120)  # 2 minutes
            driver.quit()
            print("Session closed successfully")
            num_attempts = 0  # reset num_attempts on successful session
        except:
            print(f"Session failed with IP address {ip_address}. Trying again...")
            num_attempts += 1

    print("All attempts failed. Aborting...")


# Define the main function
def main():
    # Set the URL of the website to interact with
    url = 'https://fiverr.com'

    # Set the number of tries before giving up
    num_tries = 3

    # Call the use_proxies function
    use_proxies(url, num_tries)


# Run the main function
if __name__ == '__main__':
    main()
    
    

