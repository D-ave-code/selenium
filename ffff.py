from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

# URL del formulario de Google
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSebAR7SAmwvpQ06lxJba62HSS7E1UrDR2mhYyG-BEuHqoehJg/viewform?pli=1&pli=1"

# Configurar opciones de Chrome
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Puedes activarlo si no necesitas ver la interfaz
chrome_options.add_argument("--disable-gpu")

# Inicializar el navegador
driver = webdriver.Chrome(options=chrome_options)
driver.get(form_url)
time.sleep(2)

# Completar campos
edificio = 0
dias = 0
tipo_comida = 0

# Llenar campo "ULTIMAITX"
nombre_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
nombre_input = driver.find_element(By.XPATH, nombre_xpath)
nombre_input.send_keys("2846981")

# Llenar campo "nombre"
ultimatix_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
ultimatix_input = driver.find_element(By.XPATH, ultimatix_xpath)
ultimatix_input.send_keys("David Espinosa")

# Selección de opciones
for i in range(2, 11, 2):
    checkbox = driver.find_element(By.XPATH, f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[{i}]/span/div[2]')
    if not checkbox.is_selected():
        checkbox.click()
        if checkbox.is_selected():
            edificio += 1

for i in range(2, 11, 2):
    checkbox = driver.find_element(By.XPATH, f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[{i}]/span/div[3]')
    if not checkbox.is_selected():
        checkbox.click()
        if checkbox.is_selected():
            dias += 1

for i in range(2, 11, 2):
    checkbox = driver.find_element(By.XPATH, f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[3]/div/div[1]/div/div[{i}]/span/div[2]')
    if not checkbox.is_selected():
        checkbox.click()
        if checkbox.is_selected():
            tipo_comida += 1

# Verifica si todo fue seleccionado
if edificio == 5 and dias == 5 and tipo_comida == 5:
    print("Todo correcto")
else:
    print("Error")

# Espera para asegurar que todo esté cargado
time.sleep(2)

# Ajustar la ventana a la altura total del documento
total_height = driver.execute_script("return document.body.scrollHeight")
print(f"Altura total del documento: {total_height}")
driver.set_window_size(1200, total_height)

# Hacer scroll al tope
driver.execute_script("window.scrollTo(0, 100)")
time.sleep(1)  # Esperar un poco para que se renderice bien

# Tomar la captura de pantalla
driver.save_screenshot("formulario_completo.png")
print("✅ Captura tomada correctamente como 'formulario_completo.png'")


# Cerrar navegador
driver.quit()
