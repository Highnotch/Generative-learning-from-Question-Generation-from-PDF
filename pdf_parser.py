from PyPDF2 import PdfFileReader
import openai


#### CAN CHANGE THE CODE A BIT IN TERMS OF PAGES TO sTART:::



def parse_pdf(file,start_page=20):
    pdf_text = ""
    pdf_reader = PdfFileReader(file)
    for page_num in range(start_page,pdf_reader.numPages): ## <----------------------
        page = pdf_reader.getPage(page_num)
        pdf_text += page.extractText()

    return pdf_text