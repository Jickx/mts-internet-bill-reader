from re import findall
import pdfplumber
from datetime import datetime

with pdfplumber.open(r'example.pdf') as pdf:

    current_date = 0
    overall_kBytes_int = 0
    overall = []
    overall_month = {}
    total_pages = len(pdf.pages)
    print(f"Total pages: {total_pages}")

    for pages in range(total_pages):

        page = pdf.pages[pages]
        text = page.extract_text()
        lines = text.split('\n')

        for i in range(len(lines)):
            line = lines[i]

            if "Kb " in line:
                kBytes_in_line = findall(r'\w*Kb', line)[0]
                kBytes_int = int(kBytes_in_line.replace("Kb", ""))

                date = findall(r"\d{2}\.\d{2}\.\d{4}", line)[0]

                date = datetime.strptime(date, '%d.%m.%Y')

                date_in_line = date.strftime("%B %Y")

                if current_date == 0:
                    overall_kBytes_int = kBytes_int
                    current_date = date_in_line

                elif current_date == date_in_line:
                    overall_kBytes_int += kBytes_int
                    # print(overall_kBytes_int)

                elif current_date != date_in_line:
                    overall_month[current_date] = overall_kBytes_int
                    overall.append(overall_month.copy())
                    # print(f"iterator is {i}")

                    current_date = date_in_line
                    overall_kBytes_int = kBytes_int
                    overall_month.clear()

overall_month[current_date] = overall_kBytes_int
overall.append(overall_month.copy())

print(overall)

result = 0

for elm in overall:
    for k, v in elm.items():
        result += v

print(result)
