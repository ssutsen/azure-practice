import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

key = os.environ.get('FR_KEY')
endpoint = os.environ.get('FR_ENDPOINT')

# sample document
formUrl = "https://formrecognizer.appliedai.azure.com/documents/samples/prebuilt/w2-multiple.png"

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)
    
poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-tax.us.w2", formUrl)
w2s = poller.result()

for idx, w2 in enumerate(w2s.documents):
    print("--------Recognizing W-2 #{}--------".format(idx + 1))
    for name, field in w2.fields.items():
        if name == "AdditionalInfo":
            print ("W-2 Additional Info:")
            for idy, item in enumerate(field.value):
                print("...Additional Info#{}".format(idy+1))
                for item_field_name, item_field in item.value.items():
                    print("......{}: {} has confidence {}".format(
                        item_field_name, item_field.value, item_field.confidence))
        if name == "Employee":
            print ("W-2 Employee Info:")
            for i, (item_field_name, item_field) in enumerate(field.value.items()):
                print("...{}: {} has confidence {}".format(item_field_name, item_field.value, item_field.confidence))
        if name == "Employer":
            print ("W-2 Employer Info:")
            for i, (item_field_name, item_field) in enumerate(field.value.items()):
                print("...{}: {} has confidence {}".format(item_field_name, item_field.value, item_field.confidence))
        if name == "LocalTaxInfos":
            print ("W-2 Local Tax Info:")
            for idy, item in enumerate(field.value):
                print("...Local Tax Info#{}".format(idy+1))
                for item_field_name, item_field in item.value.items():
                    print("......{}: {} has confidence {}".format(
                        item_field_name, item_field.value, item_field.confidence))
        if name == "StateTaxInfos":
            print ("W-2 State Tax Info:")
            for idy, item in enumerate(field.value):
                print("...State Tax Info#{}".format(idy+1))
                for item_field_name, item_field in item.value.items():
                    print("......{}: {} has confidence {}".format(
                        item_field_name, item_field.value, item_field.confidence))
        else:
            print("{}: {} has confidence {}".format(name, field.value, field.confidence))
    print("----------------------------------------")
