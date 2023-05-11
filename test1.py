import json

# 載入JSON文件
with open('%E5%A4%96%E7%B1%8D%E7%9C%8B%E8%AD%B7%E5%B7%A5%E7%AE%A1%E7%90%86%E8%BE%A6%E6%B3%95.docx.pdf.json', mode='r', encoding='utf-16') as f:
        
#with open(r'%E5%A4%96%E7%B1%8D%E7%9C%8B%E8%AD%B7%E5%B7%A5%E7%AE%A1%E7%90%86%E8%BE%A6%E6%B3%95.docx.pdf.json', "r", encoding="utf-8") as f:
    json_data = json.load(f)

for page in json_data["analyzeResult"]["pages"]:
    # 提取頁面號
    page_number = page["pageNumber"]
    print(f"Page Number: {page_number}")

    # 遍歷每行
    for line in page["lines"]:
        # 提取行內容
        line_content = ""
        for word in line["words"]:
            line_content += word["content"]
        print(f"Line Content: {line_content}")
