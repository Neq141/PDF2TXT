import os
import re
import PyPDF2


def pdf_to_markdown(file_path) :
    try :
        with open ( file_path, 'rb' ) as file :
            pdf_reader = PyPDF2.PdfReader ( file )
            text = [ ]

            for page in pdf_reader.pages :
                page_text = page.extract_text ()
                text.append ( page_text.rstrip () )

            markdown = '\n\n'.join ( text )
            markdown = re.sub ( r'\n{3,}', '\n\n', markdown )
            markdown = re.sub ( r'^\s+', '', markdown, flags = re.MULTILINE )
            markdown = re.sub ( r'\n\s+', '\n', markdown )

            return markdown
    except (FileNotFoundError, PyPDF2.utils.PdfReadError) :
        print ( f"Error: Unable to read file '{file_path}'" )
        return None


def select_file() :
    while True :
        file_path = input ( "Enter the path of the PDF file you want to convert: " )
        if os.path.isfile ( file_path ) :
            return file_path
        else :
            print ( f"'{file_path}' is not a valid file path." )


def convert_to_markdown(file_path) :
    markdown = pdf_to_markdown ( file_path )
    if markdown is not None :
        output_file_path = f"{file_path [ :-3 ]}md"
        with open ( output_file_path, 'w' ) as file :
            file.write ( markdown )
        print ( f"Conversion complete. Markdown saved to '{output_file_path}'." )


def select_directory() :
    while True :
        directory_path = input ( "Enter the path of the directory containing PDF files: " )
        if os.path.isdir ( directory_path ) :
            return directory_path
        else :
            print ( f"'{directory_path}' is not a valid directory path." )


def list_files(directory_path) :
    files = [ ]
    for file_name in os.listdir ( directory_path ) :
        if file_name.lower ().endswith ( '.pdf' ) :
            files.append ( file_name )
    return files


def select_file_from_list(file_list) :
    print ( "Select a file to convert:" )
    for index, file_name in enumerate ( file_list ) :
        print ( f"{index + 1}. {file_name}" )
    while True :
        choice = input ( "Enter the number of the file you want to convert: " )
        if choice.isdigit () and int ( choice ) >= 1 and int ( choice ) <= len ( file_list ) :
            return file_list [ int ( choice ) - 1 ]
        else :
            print ( f"'{choice}' is not a valid choice." )


def convert_directory() :
    directory_path = select_directory ()
    file_list = list_files ( directory_path )
    if not file_list :
        print ( "Error: No PDF files found in directory." )
        return
    file_name = select_file_from_list ( file_list )
    file_path = os.path.join ( directory_path, file_name )
    convert_to_markdown ( file_path )


if __name__ == '__main__' :
    convert_directory ()
