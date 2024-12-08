import os
import shutil
import subprocess
import sys
import socket
import qrcode_terminal

def check_python():
    """Sprawdza, czy Python jest zainstalowany i dostępny w PATH."""
    python_path = shutil.which("python")
    if python_path is None:
        print("Alert: Zainstaluj Python i dodaj go do PATH.")
        return False
    else:
        print(f"Python jest zainstalowany: {python_path}")
        return True

def install_requirements():
    """Instaluje zależności z pliku requirements.txt."""
    if not os.path.exists("requirements.txt"):
        print("Nie znaleziono pliku requirements.txt. Upewnij się, że plik znajduje się w tym samym folderze co skrypt.")
        return False
    
    try:
        print("Instalowanie zależności z requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Zależności zostały zainstalowane.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas instalacji zależności: {e}")
        return False

def get_local_ip():
    """Pobiera lokalny adres IP komputera."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        print(f"Błąd przy pobieraniu adresu IP: {e}")
        return "127.0.0.1"

def run_django_server():
    """Uruchamia serwer Django na IP komputera i porcie 8000."""
    local_ip = get_local_ip()
    try:
        print(f"Uruchamianie serwera Django na http://{local_ip}:8000...")
        data = f"http://{local_ip}:8000"
        qrcode_terminal.draw(data)
        subprocess.check_call([sys.executable, "canteam/manage.py", "runserver", f"{local_ip}:8000"])
    except FileNotFoundError:
        print("Nie znaleziono pliku manage.py. Upewnij się, że skrypt jest uruchamiany w katalogu projektu Django.")
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas uruchamiania serwera Django: {e}")

if __name__ == "__main__":
    if not check_python():
        sys.exit(1)
    
    if not install_requirements():
        sys.exit(1)
    
    run_django_server()
