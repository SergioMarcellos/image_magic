"""
Script para ocultar um link em uma imagem JPEG
Embute o link nos metadados EXIF da imagem
"""

from PIL import Image
from PIL.ExifTags import TAGS
import piexif
import os

def hide_link_in_image(image_path, link, output_path):
    """
    Oculta um link em uma imagem JPEG usando metadados EXIF
    
    Args:
        image_path (str): Caminho para a imagem original
        link (str): Link para ser oculto
        output_path (str): Caminho para salvar a imagem com o link oculto
    
    Returns:
        bool: True se sucesso, False caso contrário
    """
    try:
        # Abrir a imagem
        image = Image.open(image_path)
        
        # Se a imagem não está em RGB, converter
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Carregar dados EXIF existentes ou criar novos
        try:
            exif_dict = piexif.load(image_path)
        except:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}
        
        # Adicionar o link no campo de comments (tag 270)
        # ou no campo UserComment (tag 37510)
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = link.encode('utf-8')
        
        # Também adicionar no Exif UserComment como backup
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = link.encode('utf-8')
        
        # Converter para bytes
        exif_bytes = piexif.dump(exif_dict)
        
        # Salvar a imagem com os metadados
        image.save(output_path, "jpeg", exif=exif_bytes, quality=95)
        
        print(f"✓ Link oculto com sucesso!")
        print(f"  Imagem salva em: {output_path}")
        print(f"  Link armazenado: {link}")
        return True
        
    except Exception as e:
        print(f"✗ Erro ao ocultar link: {str(e)}")
        return False

def extract_link_from_image(image_path):
    """
    Extrai o link oculto de uma imagem JPEG
    
    Args:
        image_path (str): Caminho para a imagem
    
    Returns:
        str: Link encontrado ou None
    """
    try:
        # Carregar dados EXIF
        exif_dict = piexif.load(image_path)
        
        # Tentar extrair do ImageDescription
        if piexif.ImageIFD.ImageDescription in exif_dict["0th"]:
            link = exif_dict["0th"][piexif.ImageIFD.ImageDescription].decode('utf-8')
            return link
        
        # Tentar extrair do UserComment
        if piexif.ExifIFD.UserComment in exif_dict["Exif"]:
            link = exif_dict["Exif"][piexif.ExifIFD.UserComment].decode('utf-8')
            return link
        
        return None
        
    except Exception as e:
        print(f"✗ Erro ao extrair link: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python hide_link_in_image.py <caminho_imagem> <link> [caminho_saida]")
        print("\nExemplo:")
        print("  python hide_link_in_image.py foto.jpg https://exemplo.com output.jpg")
        print("  python hide_link_in_image.py foto.jpg https://exemplo.com (salva como foto_hidden.jpg)")
        sys.exit(1)
    
    image_path = sys.argv[1]
    link = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else image_path.replace('.jpg', '_hidden.jpg').replace('.jpeg', '_hidden.jpeg')
    
    if not os.path.exists(image_path):
        print(f"✗ Arquivo não encontrado: {image_path}")
        sys.exit(1)
    
    # Ocultar link
    hide_link_in_image(image_path, link, output_path)
    
    # Verificar se foi armazenado
    extracted = extract_link_from_image(output_path)
    if extracted:
        print(f"✓ Verificação: Link extraído com sucesso: {extracted}")
