import json
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# use your `key` and `endpoint` environment variables
endpoint = "https://bebe.cognitiveservices.azure.com/"
key = "d7f41d8401d74f87bd368ed2db20333c"

# formatting function
def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])


def analyze_read():
    # sample form document
    formUrl = "https://bebe.blob.core.windows.net/bebe/中越版照顧服務員工作職責.docx.pdf"

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_analysis_client.begin_analyze_document_from_url(
        "prebuilt-read", formUrl
    )
    result = poller.result()

    # Convert the result to a dictionary
    output = {
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
                
            }
            for page in result.pages
        ],
    }

    # Write the dictionary to a JSON file
    with open("中越版照顧服務員工作職責.json", "w", encoding = "utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    analyze_read()
