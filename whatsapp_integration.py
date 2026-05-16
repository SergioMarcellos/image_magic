#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WhatsApp Integration para image_magic
Envia imagens capturadas diretamente para WhatsApp Web
"""

import sys
import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from main import capture_webpage_to_image

def wait_for_whatsapp_login(driver, timeout=60):
    """
    Aguarda o usuário fazer login no WhatsApp Web
    
    Args:
        driver: Selenium WebDriver
        timeout: Tempo máximo de espera em segundos
    """
    print("📱 Abrindo WhatsApp Web...")
    print("⏳ Aguardando login (escaneie o QR Code)...")
    
    try:
        # Esperar pela mudança de estado (login bem-sucedido)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//span[@title='Pesquisar ou começar uma conversa']"))
        )
        print("✅ Login realizado com sucesso!")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"❌ Timeout ao aguardar login: {str(e)}")
        return False

def find_chat(driver, contact_name, timeout=10):
    """
    Procura por um contato no WhatsApp Web
    
    Args:
        driver: Selenium WebDriver
        contact_name: Nome do contato ou número
        timeout: Tempo máximo de espera
    
    Returns:
        True se encontrado, False caso contrário
    """
    try:
        print(f"🔍 Procurando por: {contact_name}")
        
        # Clicar na barra de pesquisa
        search_box = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Pesquisar ou começar uma conversa']"))
        )
        search_box.click()
        time.sleep(1)
        
        # Digitar o nome do contato
        search_box.clear()
        search_box.send_keys(contact_name)
        time.sleep(2)
        
        # Aguardar e clicar no resultado
        contact = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, f"//span[@title='{contact_name}']"))
        )
        contact.click()
        print(f"✅ Conversa com {contact_name} aberta!")
        time.sleep(1)
        return True
        
    except Exception as e:
        print(f"❌ Erro ao procurar contato: {str(e)}")
        return False

def send_image_to_whatsapp(driver, image_path, caption="", timeout=15):
    """
    Envia uma imagem para a conversa aberta
    
    Args:
        driver: Selenium WebDriver
        image_path: Caminho da imagem
        caption: Legenda da mensagem
        timeout: Tempo máximo de espera
    
    Returns:
        True se enviado com sucesso
    """
    try:
        # Obter caminho absoluto da imagem
        image_path = os.path.abspath(image_path)
        
        if not os.path.exists(image_path):
            print(f"❌ Arquivo não encontrado: {image_path}")
            return False
        
        print(f"📎 Anexando imagem: {os.path.basename(image_path)}")
        
        # Encontrar botão de anexar (clipe)
        attach_button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Anexar']"))
        )
        attach_button.click()
        time.sleep(1)
        
        # Encontrar input de arquivo
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        
        # Enviar caminho do arquivo
        file_input.send_keys(image_path)
        print("✅ Imagem selecionada!")
        time.sleep(2)
        
        # Se houver legenda, adicionar
        if caption:
            print(f"✏️ Adicionando legenda: {caption}")
            caption_input = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox'][@contenteditable='true']"))
            )
            caption_input.send_keys(caption)
            time.sleep(1)
        
        # Encontrar e clicar no botão Enviar
        send_button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Enviar']"))
        )
        send_button.click()
        print("✅ Imagem enviada com sucesso! 🎉")
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar imagem: {str(e)}")
        return False

def share_webpage_to_whatsapp(webpage_url, contact_name, caption=""):
    """
    Fluxo completo: captura webpage, abre WhatsApp e envia
    
    Args:
        webpage_url: URL da página web
        contact_name: Nome do contato/grupo
        caption: Legenda da imagem
    """
    # Gerar nome temporário para a imagem
    temp_image_name = "temp_webpage_screenshot.jpg"
    
    # Passo 1: Capturar a página web
    print("=" * 50)
    print("🚀 Iniciando compartilhamento para WhatsApp")
    print("=" * 50)
    
    try:
        capture_webpage_to_image(webpage_url, temp_image_name)
    except Exception as e:
        print(f"❌ Erro ao capturar página: {str(e)}")
        return False
    
    # Passo 2: Abrir WhatsApp Web
    print("\n" + "=" * 50)
    print("📱 Abrindo WhatsApp Web")
    print("=" * 50)
    
    try:
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://web.whatsapp.com/")
        
        # Aguardar login
        if not wait_for_whatsapp_login(driver):
            driver.quit()
            return False
        
        # Passo 3: Encontrar contato
        print("\n" + "=" * 50)
        print(f"🔍 Procurando contato: {contact_name}")
        print("=" * 50)
        
        if not find_chat(driver, contact_name):
            driver.quit()
            return False
        
        # Passo 4: Enviar imagem
        print("\n" + "=" * 50)
        print("📤 Enviando imagem")
        print("=" * 50)
        
        send_image_to_whatsapp(driver, temp_image_name, caption)
        
        # Aguardar um pouco antes de fechar
        time.sleep(3)
        driver.quit()
        
        # Limpar arquivo temporário
        if os.path.exists(temp_image_name):
            os.remove(temp_image_name)
            print(f"\n🗑️ Arquivo temporário removido")
        
        print("\n" + "=" * 50)
        print("✅ Processo concluído com sucesso!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o processo: {str(e)}")
        return False

def main():
    """Função principal"""
    if len(sys.argv) < 3:
        print("Uso: python whatsapp_integration.py <URL> <CONTATO> [LEGENDA]")
        print("\nExemplo:")
        print("  python whatsapp_integration.py https://www.google.com 'João Silva'")
        print("  python whatsapp_integration.py github.com 'Projeto Python' 'Confira nosso novo repo!'")
        print("\nNotas:")
        print("  - CONTATO: Nome exato do contato ou grupo no WhatsApp")
        print("  - LEGENDA: Opcional - texto para acompanhar a imagem")
        sys.exit(1)
    
    webpage_url = sys.argv[1]
    contact_name = sys.argv[2]
    caption = sys.argv[3] if len(sys.argv) > 3 else ""
    
    share_webpage_to_whatsapp(webpage_url, contact_name, caption)

if __name__ == "__main__":
    main()
