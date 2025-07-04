import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class TestLoginPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.base_url = "https://miunsta.vercel.app"
        cls.wait = WebDriverWait(cls.driver, 15)  # Aumentado el tiempo de espera
        
        # Usuarios de prueba
        cls.users = {
            "admin": {"email": "admin@example.com", "password": "password123", "role": "ADMIN"},
            "docente": {"email": "docente@example.com", "password": "password123", "role": "DOCENTE"},
            "alumno": {"email": "alumno@example.com", "password": "password123", "role": "ALUMNO"},
        }

    def setUp(self):
        self.driver.get(f"{self.base_url}/login")
        time.sleep(2)  # Espera para asegurar carga completa

    def tearDown(self):
        # Limpiar cookies después de cada test
        self.driver.delete_all_cookies()
        time.sleep(1)

    def login(self, email, password):
        """Función helper para realizar login"""
        email_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='correo@ejemplo.com']"))
        )
        email_field.clear()
        email_field.send_keys(email)
        
        password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_field.clear()
        password_field.send_keys(password)
        
        login_btn = self.driver.find_element(By.XPATH, "//button[contains(., 'Iniciar Sesión')]")
        login_btn.click()
        time.sleep(2)  # Espera para el proceso de login

    def test_01_elementos_login(self):
        """Verificar elementos básicos del formulario de login"""
        # Verificar título de la página
        self.assertIn("MiUnsta", self.driver.title)
        
        # Verificar campos del formulario
        email_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='correo@ejemplo.com']"))
        )
        self.assertTrue(email_field.is_displayed())
        
        password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        self.assertTrue(password_field.is_displayed())
        
        login_btn = self.driver.find_element(By.XPATH, "//button[contains(., 'Iniciar Sesión')]")
        self.assertTrue(login_btn.is_displayed())

    def test_02_validacion_formulario(self):
        """Probar validaciones del formulario"""
        login_btn = self.driver.find_element(By.XPATH, "//button[contains(., 'Iniciar Sesión')]")
        login_btn.click()
        
        # Verificar mensajes de error
        email_error = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'email válido')]"))
        )
        self.assertTrue(email_error.is_displayed())
        
        password_error = self.driver.find_element(By.XPATH, "//p[contains(text(), '6 caracteres')]")
        self.assertTrue(password_error.is_displayed())

    def test_03_login_admin(self):
        """Probar login exitoso para admin"""
        user = self.users["admin"]
        self.login(user["email"], user["password"])
        
        # Verificar redirección
        try:
            self.wait.until(
                EC.url_contains(f"/dashboards/{user['role'].lower()}")
            )
            self.assertIn(f"/dashboards/{user['role'].lower()}", self.driver.current_url)
        except TimeoutException:
            self.fail("No se redirigió al dashboard de admin")

    def test_04_login_docente(self):
        """Probar login exitoso para docente"""
        user = self.users["docente"]
        self.login(user["email"], user["password"])
        
        # Verificar redirección
        try:
            self.wait.until(
                EC.url_contains(f"/dashboards/{user['role'].lower()}")
            )
            self.assertIn(f"/dashboards/{user['role'].lower()}", self.driver.current_url)
        except TimeoutException:
            self.fail("No se redirigió al dashboard de docente")

    def test_05_login_alumno(self):
        """Probar login exitoso para alumno"""
        user = self.users["alumno"]
        self.login(user["email"], user["password"])
        
        # Verificar redirección
        try:
            self.wait.until(
                EC.url_contains(f"/dashboards/{user['role'].lower()}")
            )
            self.assertIn(f"/dashboards/{user['role'].lower()}", self.driver.current_url)
        except TimeoutException:
            self.fail("No se redirigió al dashboard de alumno")

    def test_06_credenciales_invalidas(self):
        """Probar login con credenciales incorrectas"""
        self.login("noexiste@example.com", "contrasena-incorrecta")
        
        # Verificar mensaje de error
        error_msg = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'incorrectas')]"))
        )
        self.assertTrue(error_msg.is_displayed())

    def test_07_logout(self):
        """Probar funcionalidad de logout"""
        # Login primero
        user = self.users["admin"]
        self.login(user["email"], user["password"])
        
        # Esperar redirección
        self.wait.until(
            EC.url_contains(f"/dashboards/{user['role'].lower()}")
        )
        
        # Hacer logout (ajusta este selector según tu implementación)
        logout_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Cerrar sesión')]"))
        )
        logout_btn.click()
        
        # Verificar que volvemos al login
        self.wait.until(
            EC.url_contains("/login")
        )
        self.assertIn("/login", self.driver.current_url)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)