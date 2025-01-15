# Upwork Test Script

This script automates the process of interacting with a web page using a headless browser. It uses the `Display` and `Driver` classes to manage the browser and perform actions on the web page.

## Requirements

- Python 3.x
- Selenium
- PyVirtualDisplay

## Installation

1. Install the required Python packages:
    ```bash
    pip install selenium pyvirtualdisplay
    ```

2. Ensure you have the necessary web driver installed (e.g., ChromeDriver for Google Chrome).

## Usage

1. Run the script:
    ```bash
    python upwork_test.py
    ```

2. The script will:
    - Start a virtual display.
    - Launch a headless browser.
    - Navigate to the specified URL.
    - Perform actions on the web page, such as clicking buttons.

## Notes

- Make sure to update the `driver.get` URL and the CSS selectors in the `wait_for_element` method to match the target web page.
- Adjust the sleep times as necessary to ensure the elements are loaded before interacting with them.

## Troubleshooting

- If you encounter issues with the web driver, ensure it is correctly installed and the path is set in your environment variables.
- Check the CSS selectors to ensure they match the elements on the web page.

## License

This project is licensed under the MIT License.