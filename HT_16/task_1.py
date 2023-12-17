import csv
import logging
import requests
import shutil
from fpdf import FPDF
from io import BytesIO
from pathlib import Path
from PIL import Image
from requests import RequestException
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, TimeoutException
from selenium.common import StaleElementReferenceException
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO)


class RobotOrderProcessor:

    def __init__(self):
        self.parent_dir = Path(__file__).resolve().parent
        self.base_url = 'https://robotsparebinindustries.com'
        self.initialize_output_directory()
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver_wait = WebDriverWait(self.driver, 10)
        self.orders_data = []

    def initialize_output_directory(self, directory_name='output'):
        output_directory = self.parent_dir / directory_name
        try:
            with output_directory:
                if output_directory.is_dir():
                    for item in output_directory.iterdir():
                        if item.is_dir():
                            shutil.rmtree(item, ignore_errors=True)
                        else:
                            item.unlink()
                    logging.info(f"Folder '{directory_name}' cleared successfully")
                else:
                    output_directory.mkdir(parents=True)
                    logging.info(f"Folder '{directory_name}' created successfully")
        except Exception as e:
            logging.error(f"Error with creating/clearing '{directory_name}' folder: {e}")

    def get_robots_orders_data(self):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
            response = requests.get(urljoin(self.base_url, '/orders.csv'), headers=headers)
            data_list = []
            if response.status_code == 200:
                reader = csv.DictReader(response.text.splitlines())

                for row in reader:
                    data_list.append(row)

            return data_list
        except RequestException as e:
            logging.error(f"Error during request to get 'orders.csv': {e}")

    def handle_alert_buttons(self):
        try:
            self.driver_wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'alert-buttons'))
            )
            alert_buttons_selector = 'div.alert-buttons button'
            allert_buttons = self.driver.find_elements(By.CSS_SELECTOR, alert_buttons_selector)
            for button in allert_buttons:
                self.driver_wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, alert_buttons_selector))
                )

                button.click()
                if self.driver_wait.until(
                        EC.invisibility_of_element_located((By.CLASS_NAME, 'alert-buttons'))
                ):

                    break
        except WebDriverException as e:
            logging.error(f"Error while handling alert buttons: {e}")

    def navigate_to_order_page(self):
        try:
            self.driver.get(self.base_url)

            order_brn = self.driver_wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Order your robot!'))
            )
            order_brn.click()

            self.handle_alert_buttons()
        except WebDriverException as e:
            logging.error(f"Error while navigating to order page: {e}")

    def submit_order(self, order_dict):
        try:
            self.fill_order_form(order_dict)

            preview_button = self.driver_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn-secondary'))
            )

            self.click_element_with_retry(preview_button)

            self.driver_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#robot-preview-image'))
            )
            images_list = self.get_robot_images()

            order_button = self.driver_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn-primary'))
            )

            self.click_element_with_retry(order_button)

            receipt_html, receipt_number = self.get_receipt_html_and_number()

            return images_list, receipt_html, receipt_number
        except WebDriverException as e:
            logging.error(f"Error with submitting the order and making order process: {e}")

    def is_alert_danger_message(self):
        try:
            alert_div = WebDriverWait(self.driver, 0.5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.col-sm-7 div.alert[role="alert"]'))
            )
            return bool(alert_div.text)
        except TimeoutException:
            return False

    def successful_order(self):
        try:
            WebDriverWait(self.driver, 0.5).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#order-completion')))

            receipt_number = self.driver.find_element(By.CSS_SELECTOR, 'p.badge.badge-success').text
            return bool(receipt_number)
        except TimeoutException:
            return False

    def click_element_with_retry(self, button):
        max_retries = 10
        current_retry = 0

        while current_retry < max_retries:
            try:
                self.driver_wait.until(EC.element_to_be_clickable(button)).click()
                if self.successful_order():
                    return

                if self.is_alert_danger_message():
                    current_retry += 1
                else:
                    return

            except ElementClickInterceptedException:
                logging.error("ElementClickInterceptedException: The element receiving the events is obscuring the element that was requested to be clicked")
                try:
                    self.driver_wait.until(EC.element_to_be_clickable(button))
                    self.driver.execute_script("arguments[0].click();", button)
                    if self.successful_order():
                        return

                    if self.is_alert_danger_message():
                        current_retry += 1
                    else:
                        return
                except (StaleElementReferenceException, ElementClickInterceptedException):
                    current_retry += 1
            except StaleElementReferenceException:
                logging.error("StaleElementReferenceException: Reference to an element is now “stale”, the element no longer appears on the DOM of the page.")
                current_retry += 1
            except WebDriverException:
                current_retry += 1

    def fill_order_form(self, order_dict):
        try:
            self.driver_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'form'))
            )
            self.select_head(order_dict['Head'])
            self.select_body(order_dict['Body'])
            self.enter_legs_count(order_dict['Legs'])
            self.enter_address(order_dict['Address'])
        except WebDriverException as e:
            logging.error(f"Error while filling the order form: {e}")

    def select_head(self, head_value):
        try:
            head_select = self.driver.find_element(By.ID, 'head')
            head_select.click()
            self.driver_wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#head option'))
            )

            option_css = f'#head option[value="{head_value}"]'
            option_element = self.driver_wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, option_css))
            )
            option_element.click()

            self.driver_wait.until(
                EC.text_to_be_present_in_element_value((By.ID, 'head'), head_value)
            )
        except WebDriverException as e:
            logging.error(f"Error in selecting head: {e}")

    def select_body(self, body_value):
        try:
            body_radio = self.driver.find_element(
                By.CSS_SELECTOR, f'.radio.form-check input#id-body-{body_value}'
            )
            body_radio.click()
            self.driver_wait.until(
                EC.element_to_be_selected(body_radio)
            )
        except WebDriverException as e:
            logging.error(f"Error in selecting body: {e}")

    def enter_legs_count(self, legs_value):
        try:
            option_css = 'input.form-control[type="number"]'
            legs_field = self.driver.find_element(By.CSS_SELECTOR, option_css)
            legs_field.send_keys(legs_value)
            self.driver_wait.until(
                EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, option_css), legs_value)
            )
        except WebDriverException as e:
            logging.error(f"Error while entering legs count: {e}")

    def enter_address(self, address_value):
        try:
            option_css = 'input.form-control[type="text"]'
            address_field = self.driver.find_element(By.CSS_SELECTOR, option_css)
            address_field.send_keys(address_value)
            self.driver_wait.until(
                EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, option_css), address_value)
            )
        except WebDriverException as e:
            logging.error(f"Error while entering address: {e}")

    def get_receipt_html_and_number(self):
        try:
            self.driver_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#order-completion')))
            receipt_html = self.driver.find_element(By.CLASS_NAME, 'alert.alert-success').get_attribute('outerHTML')
            receipt_number = self.driver.find_element(By.CSS_SELECTOR, 'p.badge.badge-success').text

            return receipt_html, receipt_number
        except WebDriverException as e:
            logging.error(f"Error in getting receipt html and number: {e}")

    def get_robot_images(self):
        try:
            images_list = []
            images_elements = [
                {'name': 'Head', 'selector': '#robot-preview-image img[alt="Head"]'},
                {'name': 'Body', 'selector': '#robot-preview-image img[alt="Body"]'},
                {'name': 'Legs', 'selector': '#robot-preview-image img[alt="Legs"]'}
            ]

            for elem in images_elements:
                elem_src = self.driver.find_element(By.CSS_SELECTOR, elem['selector']).get_attribute('src')
                image = Image.open(BytesIO(requests.get(elem_src).content))
                images_list.append(image)

            return images_list
        except WebDriverException as e:
            logging.error(f"Error in getting robot images: {e}")

    def create_order_pdf(self, order_dict):
        try:
            images_list, receipt_html, receipt_number = self.submit_order(order_dict)
            logging.info(f"Order submitted successfully. Receipt Number: {receipt_number}")
            robot_image = self.create_robot_image(images_list)
            output_filename = self.parent_dir / "output" / f"{receipt_number}_robot.pdf"

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, receipt_html)

            robot_image_file = self.parent_dir / "output" / f"{receipt_number}_robot.jpg"
            robot_image.save(str(robot_image_file), format='JPEG')

            pdf.image(str(robot_image_file), x=70, y=75, w=70)

            pdf.output(str(output_filename))
            logging.info(f"PDF file '{f'output/{receipt_number}.pdf'}' created successfully")
            robot_image_file.unlink()

            self.handle_another_order()
        except Exception as e:
            logging.error(f"Error with creating order pdf: {e}")

    def create_robot_image(self, images):
        try:
            max_width = max(image.width for image in images)
            resized_images = self.resize_images(images, max_width)

            image_height = sum(image.height for image in resized_images)
            robot_image = Image.new('RGB', (max_width, image_height))

            height_offset = 0

            for image in resized_images:
                robot_image.paste(image, (0, height_offset))
                height_offset += image.height

            logging.info(f"Robot image created successfully")
            return robot_image
        except Exception as e:
            logging.error(f"Error with creating robot image: {e}")

    def resize_images(self, images, max_width):
        resizes_images = []

        for image in images:
            new_size = (max_width, image.height)
            resized_image = image.resize(new_size)
            resizes_images.append(resized_image)

        return resizes_images

    def handle_another_order(self):
        try:
            order_another_button = self.driver_wait.until(
                EC.presence_of_element_located((By.ID, 'order-another'))
            )
            self.click_element_with_retry(order_another_button)

            self.handle_alert_buttons()
        except WebDriverException as e:
            logging.error(f"Error handling another order: {e}")

    def get_orders_data(self):
        try:
            self.navigate_to_order_page()

            robots_orders_data = self.get_robots_orders_data()

            for robot_order_data_dict in robots_orders_data:
                self.create_order_pdf(robot_order_data_dict)
        except WebDriverException as e:
            logging.error(f"Error in getting orders images: {e}")

    def close_browser(self):
        self.driver.quit()


if __name__ == "__main__":
    robots_order_process = RobotOrderProcessor()
    robots_order_process.get_orders_data()