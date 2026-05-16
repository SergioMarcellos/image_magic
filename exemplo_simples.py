"""
EXEMPLO SIMPLES - Ocultar um link em uma imagem JPEG
Para iniciantes em Python
"""

# Passo 1: Importar as bibliotecas necessárias
from PIL import Image  # Para trabalhar com imagens
import piexif          # Para trabalhar com metadados

# Passo 2: Criar uma função simples
def ocultar_link(caminho_imagem, link):
    """
    Função simples para ocultar um link em uma imagem
    
    Parâmetros:
        caminho_imagem: O arquivo da sua foto (ex: "foto.jpg")
        link: O link que quer ocultar (ex: "https://google.com")
    """
    
    # Abrir a imagem
    print("📷 Abrindo a imagem...")
    imagem = Image.open(caminho_imagem)
    
    # Se não for RGB, converter
    if imagem.mode != 'RGB':
        imagem = imagem.convert('RGB')
    
    # Carregar metadados existentes
    print("🔍 Lendo metadados...")
    exif_dict = piexif.load(caminho_imagem)
    
    # Adicionar o link nos metadados
    # Aqui estamos dizendo: "Coloca este link no campo de descrição da foto"
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = link.encode('utf-8')
    
    # Converter para formato que a imagem entende
    exif_bytes = piexif.dump(exif_dict)
    
    # Salvar a imagem com o link oculto
    nome_saida = caminho_imagem.replace('.jpg', '_com_link.jpg')
    imagem.save(nome_saida, "jpeg", exif=exif_bytes, quality=95)
    
    print(f"✅ Pronto! Imagem salva como: {nome_saida}")
    print(f"📍 Link oculto: {link}")


def extrair_link(caminho_imagem):
    """
    Função simples para extrair o link oculto de uma imagem
    
    Parâmetro:
        caminho_imagem: A foto que tem o link oculto
    """
    
    print("🔍 Procurando link na imagem...")
    
    # Carregar metadados
    exif_dict = piexif.load(caminho_imagem)
    
    # Procurar o link no campo de descrição
    if piexif.ImageIFD.ImageDescription in exif_dict["0th"]:
        link = exif_dict["0th"][piexif.ImageIFD.ImageDescription].decode('utf-8')
        print(f"✅ Link encontrado: {link}")
        return link
    
    print("❌ Nenhum link encontrado na imagem")
    return None


# Passo 3: Usar as funções
if __name__ == "__main__":
    
    # EXEMPLO 1: Ocultar um link
    print("=" * 50)
    print("EXEMPLO 1: Ocultar um link")
    print("=" * 50)
    ocultar_link("foto.jpg", "https://www.google.com")
    
    print("\n")
    
    # EXEMPLO 2: Extrair o link
    print("=" * 50)
    print("EXEMPLO 2: Extrair o link")
    print("=" * 50)
    extrair_link("foto_com_link.jpg")
