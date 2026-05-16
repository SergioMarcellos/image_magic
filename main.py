#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
image_magic - Conversor de páginas web em imagens JPEG
Autor: Sergio Marcellos
"""

import sys
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image
import io

def validate_url(url):
    """Valida se a URL é válida"""
    if not url.startswith(('http://', 'https://')):
        return f"https://{url}"
    return url

def validate_filename(filename):
    """Valida e garante que o arquivo termine com .jpg"""
    if not filename.lower().endswith('.jpg'):
        filename += '.jpg'
    return filename

def capture_webpage_to_image(url, output_filename):
    """
    Captura uma página web e converte para JPEG
    
    Args:
        url (str): URL da página web
        output_filename (str): Nome do arquivo JPEG de saída
    """
    try:
        # Validar entrada
        url = validate_url(url)
        output_filename = validate_filename(output_filename)
        
        print(f"🌐 Acessando: {url}")
        
        # Configurar opções do Chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Modo headless
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Inicializar o driver
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # Acessar a página
            driver.get(url)
            
            # Capturar screenshot
            print("📸 Capturando screenshot...")
            screenshot = driver.get_screenshot_as_png()
            
            # Converter para JPEG
            print("🎨 Convertendo para JPEG...")
            image = Image.open(io.BytesIO(screenshot))
            
            # Converter RGB se necessário (PNG pode ter transparência)
            if image.mode in ('RGBA', 'LA', 'P'):
                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = rgb_image
            
            # Salvar como JPEG com qualidade alta
            image.save(output_filename, 'JPEG', quality=95)
            
            print(f"✅ Imagem salva com sucesso: {output_filename}")
            print(f"📊 Tamanho: {os.path.getsize(output_filename) / 1024:.2f} KB")
            
        finally:
            driver.quit()
            
    except Exception as e:
        print(f"❌ Erro ao capturar a página: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    """Função principal"""
    if len(sys.argv) < 3:
        print("Uso: python main.py <URL> <nome_do_arquivo.jpg>")
        print("\nExemplo:")
        print("  python main.py https://www.google.com google.jpg")
        print("  python main.py github.com github.jpg")
        sys.exit(1)
    
    url = sys.argv[1]
    output_filename = sys.argv[2]
    
    capture_webpage_to_image(url, output_filename)

if __name__ == "__main__":
    main()
