from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import correo as email
import datetime

dia_inicio = (datetime.datetime.now() + 
              datetime.timedelta(days=2)).strftime("%d")
dia_fin = (datetime.datetime.now() + 
           datetime.timedelta(days=6)).strftime("%d")
hora_envio = datetime.datetime.now().strftime("%H:%M:%S")
# URL del formulario de Google
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSebAR7SAmwvpQ06lxJba62HSS7E1UrDR2mhYyG-BEuHqoehJg/viewform?pli=1&pli=1"
# Configurar opciones de Chrome para ejecutarlo sin cabeza (sin interfaz gráfica)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Activar modo headless
chrome_options.add_argument("--disable-gpu")  # Deshabilitar la aceleración por GPU
# Iniciar el navegador en modo headless
driver = webdriver.Chrome(options=chrome_options)
# Inicializar el navegador (Chrome)
driver.get(form_url)
edificio = 0
dias = 0
tipo_comida = 0
# Esperar a que cargue el formulario
# Llenar campo "ULTIMAITX"
nombre_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
nombre_input = driver.find_element(By.XPATH, nombre_xpath)
nombre_input.send_keys("2846981")
#time.sleep(1)
# Llenar campo "nombre"
ultimatix_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
ultimatix_input = driver.find_element(By.XPATH, ultimatix_xpath)
ultimatix_input.send_keys("David Espinosa")
total_height = driver.execute_script("return document.body.scrollHeight")
print(f"Altura total del documento: {total_height}")
driver.set_window_size(1200, total_height+300)
#time.sleep(1)
# Seleccionar un botón de opción (radio button) - Ejemplo: 2da opción
for i in range(2, 11, 2):
    checkbox = driver.find_element(By.XPATH, f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[{i}]/span/div[2]')
    if not checkbox.is_selected():
        checkbox.click()
        edificio = edificio +1
#time.sleep(1)
for i in range(2, 11, 2):
    checkbox = driver.find_element(By.XPATH, f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[{i}]/span/div[3]')               
    if not checkbox.is_selected():
        checkbox.click()
        dias = dias +1
#time.sleep(1)
for i in range(2, 11, 2):
    checkbox = driver.find_element(By.XPATH, f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[3]/div/div[1]/div/div[{i}]/span/div[2]')
                                                        
    if not checkbox.is_selected():
        checkbox.click()
        tipo_comida = tipo_comida +1
driver.execute_script("window.scrollTo(0, 1000)")
time.sleep(1)  # Esperar un poco para que se renderice bien

# Tomar la captura de pantalla
print ( dia_fin)
nombre = str(dia_inicio) + "-"+ str(dia_fin) + "-"+str(hora_envio).replace(":", "-") + ".png" 
print (nombre)
driver.save_screenshot(f"{nombre}.png")

#time.sleep(2)
if edificio == 5 and dias == 5 and tipo_comida == 5:
    """ submit_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Enviar')]")
    submit_button.click()
    #time.sleep(1)
    driver.quit() """
    print("Todo correcto")
    email.enviar_correo(
        asunto="Formulario completado correctamente",
        mensaje="El formulario fue llenado y validado con éxito.",
        destinatario="espinozadavid34@yahoo.es",
        ruta_imagen=f"{nombre}.png"  # Cambia esto por la ruta de tu imagen
    )
else:
    print("Error")
""" # Enviar el formulario
submit_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Enviar')]")
submit_button.click() """
time.sleep(1)
# Cerrar el navegador después de enviar

#driver.quit()
