import os
from openai import OpenAI
import csv
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

client = OpenAI(api_key="")

def pdf_to_text(pdf_path):
    # Open the pdf file
    pdf_document = fitz.open(pdf_path)
    num_pages = pdf_document.page_count
    text = ""

    for page_number in range(num_pages):
        # Get a page from the pdf
        page = pdf_document.load_page(page_number)
        # Render page to an image
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))

        # Use pytesseract to convert image to text
        page_text = pytesseract.image_to_string(img, lang='por')
        text += page_text

    return text


input_folder = "."
output_folder = "output"
json_object = {}

directory = '/home/brpl/od-seeds/zztests'

# Get a list of all .txt files in the directory
txt_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.txt')]

# Open each .txt file as a list object

def ask_chatgpt(prompt):
    print(prompt)
    print(type(prompt))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Analise o contrato realizado e extraia as informações do CONTRATANTE e me passe como um csv com o seguinte header: Nome, Sobrenome, Nascimento, Naturalidade, Genero, Capacidade, CEP, Número da Residência, Complemento Endereço, Bairro, Cidade, Estado, RG, CPF, NIT, NB, Estado Civil, Profissao, Empresa Atual, Nome da Mae, Telefone, Email      -- ignore todas as demais informações, se tiverem informações em branco ou você não encontrar simplesmente deixe em branco, não precisa mencionar nada, não precisa adicionar o cabeçalho na resposta, apenas o conteúdo encontrado"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content





with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for file in txt_files:
        if os.path.getsize(file) > 60:  # Check if file is not empty
            with open(file, 'r') as openfile:
                text = openfile.read()
                result = ask_chatgpt(text)
                writer.writerow([result])
        else:
            print("Blank_File")
            new_file_path = file[:-4] + '.pdf'
            print(new_file_path)
            info = pdf_to_text(new_file_path)
            result = ask_chatgpt(info)
            writer.writerow([result])

