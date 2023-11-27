import argparse
import os
from openai import OpenAI
from pypdf import PdfReader
from dotenv import load_dotenv

max_characters = 4096
VERBOSE = False
CLIENT = None

def check_text_match(data, prompt):
    if not CLIENT:
        if VERBOSE:
            print(f"No OpenAI API client instance!")
        exit(3)
    try:
        completion = CLIENT.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=4,
            messages=[
                {"role": "system", "content": f"You are a semantic search function. Your task is to respond \"True\" or \"False\", depending on whether the text you are given matches the following concept(s): \"{prompt}\""},
                {"role": "user", "content": data}
            ]
        )
        if VERBOSE:
            print(f"Response from GPT: {completion.choices[0].message}")
        return "True" in completion.choices[0].message.content
    except Exception as e:
        if VERBOSE:
            print(f"OpenAI API error: {e}")
        exit(2)

def read_page(filename):
    reader = PdfReader(filename)
    extracted_text: str = ""
    for page in reader.pages: 
        extracted_text += page.extract_text()
        if len(extracted_text) >= max_characters:
            return extracted_text[:max_characters]
    return None

def check_pdf_match(filename, prompt):
    if VERBOSE:
        print(f"Checking if {filename} matches the prompt...")
    data = read_page(filename)
    return check_text_match(data, prompt) if data else False

def search_folder(dir_path, prompt):
    pdfs = []
    # First get all pdfs in folder
    for file_path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, file_path)) and (".pdf" in file_path):
            pdfs.append(os.path.join(dir_path, file_path))
    if VERBOSE:
        print(f"PDFs in given folder: {','.join(pdfs)}")
    return [p for p in pdfs if check_pdf_match(p, prompt)]

if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(
        prog='SemanticPDFSearch',
        description=
            'ChatGPT powered PDF semantic search tool \
            - goes through a folder and performs semantic search based off a concept/topic string. \
            Returns a list of file paths to PDFs that match the search string.',
        epilog='(Requires an OpenAI API key)'
    )
    parser.add_argument('dir', help="Path to a directory containing '.pdf' files to filter based on the provided concept.")
    parser.add_argument('concept', help="The concept that the given PDFs need to match.")
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    
    CLIENT = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )
    VERBOSE = args.verbose

    if not os.path.isdir(args.dir):
        if VERBOSE:
            print("Provided path is not a directory!")
        exit(1)
    if len(args.concept.strip()) == 0:
        if VERBOSE:
            print("Concept string is empty!")
        exit(1)
    
    for pdf in search_folder(args.dir, args.concept):
        print(pdf)
    exit(0)
