# 🎨 image_magic

Converte links de páginas web em imagens JPEG. Uma ferramenta simples e prática para capturar screenshots de websites e salvá-los como arquivos de imagem.

## 📋 Descrição

O **image_magic** é um projeto Python que permite converter qualquer página web em uma imagem JPEG de alta qualidade. Ideal para documentação, arquivamento de conteúdo ou criação de previews visuais de websites.

## 🚀 Recursos

- ✅ Converte URLs em imagens JPEG
- ✅ Fácil de usar
- ✅ Suporta páginas web completas
- ✅ Configuração simples

## 📦 Requisitos

- Python 3.7 ou superior
- Navegador web (Chrome/Chromium recomendado)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/SergioMarcellos/image_magic.git
cd image_magic
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 💻 Como Usar

```bash
python main.py <URL> <nome_da_imagem.jpg>
```

### Exemplo:

```bash
python main.py https://www.google.com google_screenshot.jpg
```

Isso irá capturar a página do Google e salvar como `google_screenshot.jpg`.

## 📁 Estrutura do Projeto

```
image_magic/
├── README.md              # Este arquivo
├── main.py               # Script principal
├── requirements.txt      # Dependências do projeto
└── screenshots/          # Pasta para salvar as imagens geradas
```

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## 📝 Licença

Este projeto está licenciado sob a MIT License.

## 👨‍💻 Autor

[SergioMarcellos](https://github.com/SergioMarcellos)

---

**Desenvolvido com ❤️**
