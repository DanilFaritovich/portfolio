import pandas as pd

def convert_csv_to_xlsx(file):
    csv = pd.read_csv(file)
    head = (csv.columns.values[0] + ';Total').split(';')
    values = [(i[0] + ';' + str((int(i[0].split(';')[3]) * int(i[0].split(';')[5])))).split(';')
              for i in csv.values]

    a = pd
    df = a.DataFrame(values, columns=head)
    writer = a.ExcelWriter(file.replace('.csv', '.xlsx'), engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Worksheet', index=False)
    worksheet = writer.sheets['Worksheet']
    writer.save()
    return file.replace('.csv', '.xlsx')

file = '2 (1).csv'
file = convert_csv_to_xlsx(file)
df = csv = pd.read_excel(file)
print(file)
exit()

csv = pd.read_csv('1 (1).csv')
head = (csv.columns.values[0] + ';Total').split(';')
values = [(i[0] + ';' + str((int(i[0].split(';')[3]) * int(i[0].split(';')[5])))).split(';')
          for i in csv.values]

a = pd
df = a.DataFrame(values, columns=head)
writer = a.ExcelWriter('test.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Лист 1', index=False)
worksheet = writer.sheets['Лист 1']
print(worksheet)
worksheet.set_column('A:C', 20)
writer.save()

df = csv = pd.read_excel('test.xlsx')