import os
from dotenv import load_dotenv
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service #Fix deprecated executable_path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import EdgeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from keyboard import wait
from time import sleep
import logging
import yaml
import sys
import time
import random
import keyboard

load_dotenv()

logging.basicConfig(
    format="%(levelname)s:%(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("out.log"), logging.StreamHandler(sys.stdout)],
)

class Prenota:
    def check_file_exists(file_name):
        # parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        file_path = os.path.join(os.getcwd(), file_name)
        return os.path.isfile(file_path)

    def load_config(file_path):
        # Open the YAML file
        with open(file_path, "r") as file:
            # Load the YAML content into a Python dictionary
            config = yaml.safe_load(file)
        return config

    if __name__ == "__main__":
        if check_file_exists("files/residencia.pdf"):
            logging.info(
                f"Timestamp: {str(datetime.now())} - Required files available."
            )
            email = os.getenv("username_prenotami")
            password = os.getenv("password_prenotami")
            user_config = load_config("parameters.yaml")
            print(user_config.get("full_address"))
            # chrome_options = ChromeOptions() #Some changes for optimize the load
            # chrome_options.add_experimental_option("detach", True)
            # chrome_options.add_argument("--start-maximized")
            # chrome_options.add_argument("--disable-dev-shm-usage")
            # chrome_options.add_argument('--blink-settings=imagesEnabled=false')
            # chrome_options.add_argument("--no-sandbox")
            # driver = webdriver.Chrome(
            #     options=chrome_options, service=Service(ChromeDriverManager().install(), #Some Changes for fix deprecated executable_path
            # ))
            edge_options = EdgeOptions()
            edge_options.use_chromium = True  # Set this to True for Chromium-based Edge
            driver = webdriver.Edge(executable_path="D:\Downloads\msedgedriver.exe", options=edge_options)

            try:
                driver.get("https://prenotami.esteri.it/")
                # Wait for the page to fully load
                email_box = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.ID, "login-email"))
                )
                password_box = driver.find_element(By.ID, "login-password")
                # time.sleep(1)
                email_box.send_keys(email)
                # time.sleep(1)
                password_box.send_keys(password)
                # time.sleep(2) #2 default
                button = driver.find_elements(
                    By.XPATH, "//button[contains(@class,'button primary g-recaptcha')]"
                )
                button[0].click()
                logging.info(
                    f"Timestamp: {str(datetime.now())} - Successfuly logged in."
                )
                time.sleep(10) #Waiting some time to fully load after login and skip errors

            except Exception as e:
                logging.info(f"Exception: {e}")

            for i in range(200):
                random_number = random.randint(1, 3)

                if user_config["request_type"] == "citizenship":
                    try:
                        driver.get("https://prenotami.esteri.it/Services/Booking/751")
                        time.sleep(10) #Waiting some time to fully load and skip errors
                        
                        try:
                            appts_available = driver.find_element(
                                By.XPATH, "//*[@id='WlNotAvailable']"
                            ).get_attribute("value")
                            logging.info(
                                f"Timestamp: {str(datetime.now())} - Scheduling is not available right now."
                            )
                        except NoSuchElementException:
                            logging.info(
                                f"Timestamp: {str(datetime.now())} - Element WlNotAvailable not found. Start filling the forms."
                            )
                            file_location = os.path.join("files/residencia.pdf")
                            choose_file = driver.find_elements(By.ID, "File_0")
                            choose_file[0].send_keys(file_location)
                            privacy_check = driver.find_elements(By.ID, "PrivacyCheck")
                            privacy_check[0].click()
                            submit = driver.find_elements(By.ID, "btnAvanti")
                            submit[0].click()
                            with open("files/citizenship_form.html", "w") as f:
                                f.write(driver.page_source)
                            break
                    except Exception as e:
                        logging.info(f"Exception {e}")
                        break		
                elif user_config["request_type"] == "passport":
                    def get_page(driver): 
                        try:
                            driver.get("https://prenotami.esteri.it/Services/Booking/4685")#/Booking/671 
                            element = WebDriverWait(driver, 6).until( EC.presence_of_element_located((By.ID, "typeofbookingddl")) )
                            selects = driver.find_elements(By.TAG_NAME, "select")
                            for select in selects:
                                s = Select(select)
                                if len(s.options) == 0:
                                    return False
                            return True
                        except TimeoutException:
                            return False
                    while not get_page(driver):
                        logging.info(
                                f"Timestamp: {str(datetime.now())} - Scheduling is not available right now. Running while function"
                            )
                        if keyboard.is_pressed("p"):
                            print("Bot paused. Press R to continue.")
                            wait("r")
                            print("Bot resumed.")
                        time.sleep(2)

                    appts_available = driver.find_elements(By.XPATH, "//*[@id='WlNotAvailable']")
                    if len(appts_available) > 0:
                        logging.info(f"Timestamp: {str(datetime.now())} - Scheduling is not available right now.")
                    else:
                        h5_element = driver.find_elements(By.XPATH, "//h5[contains(text(), 'Stante l')]")
                        if len(h5_element) > 0:
                            logging.info(f"Timestamp: {str(datetime.now())} - Scheduling is not available right now (H5 message).")
                        else:
                            logging.info(f"Timestamp: {str(datetime.now())} - Element WlNotAvailable not found. Start filling the forms.")

                            with open("files/passport_form.html", "w") as f:
                                f.write(driver.page_source)

                            s0 = Select(driver.find_element(By.ID, "typeofbookingddl"))
                            s0.select_by_value(user_config.get("booking_value"))

                            if user_config["booking_value"] == "2":
                                s1 = Select(driver.find_element(By.ID, "ddlnumberofcompanions"))
                                s1.select_by_value(user_config.get("number_of_companions"))

                            q0 = driver.find_element(By.ID, "DatiAddizionaliPrenotante_0___testo")
                            q0.send_keys(user_config.get("full_address"))

                            s2 = Select(driver.find_element(By.ID, "ddls_1"))
                            s2.select_by_visible_text(user_config.get("has_under_age_children"))

                            q1 = driver.find_element(By.ID, "DatiAddizionaliPrenotante_2___testo")
                            q1.send_keys(user_config.get("total_children"))

                            s3 = Select(driver.find_element(By.ID,"ddls_3"))
                            s3.select_by_visible_text(user_config.get("marital_status"))

                            q2 = driver.find_element(By.ID, "DatiAddizionaliPrenotante_4___testo")
                            q2.send_keys(user_config.get("name_surname_couple"))

                            s4 = Select(driver.find_element(By.ID,"ddls_5"))
                            s4.select_by_visible_text(user_config.get("possess_expired_passport"))

                            q3 = driver.find_element(By.ID, "DatiAddizionaliPrenotante_6___testo")
                            q3.send_keys(user_config.get("passport_number"))

                            q4 = driver.find_element(By.ID, "DatiAddizionaliPrenotante_7___testo")
                            q4.send_keys(user_config.get("height"))

                            s5 = Select(driver.find_element(By.ID,"ddls_8"))
                            s5.select_by_visible_text(user_config.get("eye_color"))

                            # time.sleep(1)

                            file0 = driver.find_element(By.XPATH,'//*[@id="File_0"]')
                            file0.send_keys(os.getcwd() + "/files/identidade.pdf")

                            # time.sleep(1)

                            file1 = driver.find_element(By.XPATH,'//*[@id="File_1"]')
                            file1.send_keys(os.getcwd() + "/files/residencia.pdf")

                            # Additional applicant data
                            if user_config["booking_value"] == "2":
                                q5 = driver.find_element(By.ID, "Accompagnatori_0__CognomeAccompagnatore")
                                q5.send_keys(user_config.get("surname_1"))
                                
                                q6 = driver.find_element(By.ID, "Accompagnatori_0__NomeAccompagnatore")
                                q6.send_keys(user_config.get("name_1"))

                                date_1 = driver.find_element(By.ID,"Accompagnatori_0__DataNascitaAccompagnatore")
                                date_1.send_keys(user_config.get("date_of_birth_1"))

                                s6 = Select(driver.find_element(By.ID,"TypeOfRelationDDL0"))
                                s6.select_by_visible_text(user_config.get("kinship_relationship_1"))

                                q7 = driver.find_element(By.ID, "Accompagnatori_0__DatiAddizionaliAccompagnatore_0___testo")
                                q7.send_keys(user_config.get("full_address_1"))

                                s7 = Select(driver.find_element(By.ID,"ddlsAcc_0_1"))
                                s7.select_by_visible_text(user_config.get("has_under_age_children_1"))

                                q8 = driver.find_element(By.ID, "Accompagnatori_0__DatiAddizionaliAccompagnatore_2___testo")
                                q8.send_keys(user_config.get("total_children_1"))

                                s8 = Select(driver.find_element(By.ID,"ddlsAcc_0_3"))
                                s8.select_by_visible_text(user_config.get("marital_status_1"))

                                q9 = driver.find_element(By.ID, "Accompagnatori_0__DatiAddizionaliAccompagnatore_4___testo")
                                q9.send_keys(user_config.get("name_surname_couple_1"))

                                s9 = Select(driver.find_element(By.ID,"ddlsAcc_0_5"))
                                s9.select_by_visible_text(user_config.get("possess_expired_passport_1"))

                                q10 = driver.find_element(By.ID, "Accompagnatori_0__DatiAddizionaliAccompagnatore_6___testo")
                                q10.send_keys(user_config.get("passport_number_1"))

                                q11 = driver.find_element(By.ID, "Accompagnatori_0__DatiAddizionaliAccompagnatore_7___testo")
                                q11.send_keys(user_config.get("height_1"))

                                s10 = Select(driver.find_element(By.ID,"ddlsAcc_0_8"))
                                s10.select_by_visible_text(user_config.get("eye_color_1"))

                                # time.sleep(1)

                                file0 = driver.find_element(By.XPATH,'//*[@id="Accompagnatori_0__DocumentiAccompagnatore_0___File"]')
                                file0.send_keys(os.getcwd() + "/files/identidade_1.pdf")

                                # time.sleep(1)

                                file1 = driver.find_element(By.XPATH,'//*[@id="Accompagnatori_0__DocumentiAccompagnatore_1___File"]')
                                file1.send_keys(os.getcwd() + "/files/residencia_1.pdf")

                            otp_send = driver.find_element(By.ID,"otp-send")
                            otp_send.click()

                            otp_input = driver.find_element(By.ID,"otp-input")
                            otp_code = input("Ingrese el código OTP recibido por correo: ")
                            otp_input.send_keys(otp_code)

                            checkBox = driver.find_element(By.ID,"PrivacyCheck")
                            checkBox.click()

                            form_submit = driver.find_element(By.ID,"btnAvanti")
                            form_submit.click()

                            break
                    # except Exception as e:
                    #     logging.info(f"Exception {e}")
                    #     break

                time.sleep(random_number)

        else:
            logging.info(
                "Required files not available. Check the required files in readme.md file. Ending execution."
            )
            sys.exit(0)
        current_window = driver.current_window_handle
        print("Current window:", current_window)

        user_input = input(
            f"Timestamp: {str(datetime.now())} - Go ahead and fill manually the rest of the process. When finished, type quit to exit the program and close the browser. "
        )
        while True:
            if user_input == "quit":
                driver.quit()
                break