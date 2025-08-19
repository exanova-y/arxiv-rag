def download_pdf(pdf_url, output_file):
    """
    Downloads a PDF file from the given URL and saves it to the specified file.

    Args:
        pdf_url (str): The URL of the PDF file to download.
        output_file (str): The path and name of the file to save the PDF to.

    Returns:
        str: A message indicating success or the nature of an error.
    """
    try:
        # Send a GET request to the PDF URL
        response = requests.get(pdf_url)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Write the content of the PDF to the output file
        with open(output_file, "wb") as file:
            file.write(response.content)

        return f"PDF downloaded successfully and saved as '{output_file}'."

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


download_pdf_tool = FunctionTool.from_defaults(
    download_pdf,
    name='download_pdf_file_tool',
    description='python function, which downloads a pdf file by link'
)
fetch_arxiv_tool = FunctionTool.from_defaults(
    fetch_arxiv_papers,
    name='fetch_from_arxiv',
    description='download the {max_results} recent papers regarding the topic {title} from arxiv' 
)