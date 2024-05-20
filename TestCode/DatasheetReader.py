import requests



def PDFread(Link):
    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    file = requests.get(Link, headers=HEADERS)
    print(file.status_code)
    pdf = open("pdfTest.pdf", 'wb')
    pdf.write(file.content)
    pdf.close()


if __name__ == "__main__":
    PDFread(r'https://www.tdk-electronics.tdk.com/inf/80/db/fer/r_6_30_3_80_2_50.pdf')