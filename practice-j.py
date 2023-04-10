import json
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# use your `key` and `endpoint` environment variables
key = os.environ.get('FR_KEY')
endpoint = os.environ.get('FR_ENDPOINT')

# formatting function
def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])


def analyze_read():
    # sample form document
    formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/read.png"

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_analysis_client.begin_analyze_document_from_url(
        "prebuilt-read", formUrl
    )
    result = poller.result()

    # Convert the result to a dictionary
    output = {
        "content": result.content,
        "styles": [
            {"is_handwritten": style.is_handwritten}
            for style in result.styles
        ],
        "pages": [
            {
                "page_number": page.page_number,
                "width": page.width,
                "height": page.height,
                "unit": page.unit,
                "lines": [
                    {
                        "content": line.content,
                        "bounding_box": [
                            {"x": p.x, "y": p.y} for p in line.polygon
                        ],
                    }
                    for line in page.lines
                ],
                "words": [
                    {"content": word.content, "confidence": word.confidence}
                    for word in page.words
                ],
            }
            for page in result.pages
        ],
    }

    # Write the dictionary to a JSON file
    with open("output.json", "w") as f:
        json.dump(output, f, indent=4)

if __name__ == "__main__":
    analyze_read()
