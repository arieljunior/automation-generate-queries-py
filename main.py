import pyperclip

CONFIG = {
    "column_name_group_id": "field_group",
    "column_single_id": "field_id",
    "table_name_select": "Campaigns",
    "table_name_insert": "Tickets"
}

def get_data_from_csv():
    values = []
    with open('data.csv', 'r', encoding='utf8') as file:
        count = 0
        for line in file:
            if count == 0:
                count +=1
            else:
                utm_campaign, orderId = line.split(",")[:2]
                values.append({
                    "utm_campaign": utm_campaign,
                    "orderId": orderId
                })

    return values

def copy_to_clipboard_and_show(value_copy):
    if len(value_copy) > 0:
        pyperclip.copy(value_copy)
        print(f""" 
        copied to clipboard successfully = {value_copy}
        """)

def extract_data():
    values = get_data_from_csv()
    result = {}
    
    column_group_name = CONFIG['column_name_group_id']
    column_single_id = CONFIG['column_single_id']
     

    for value in values:
        utm_campaign = value[column_single_id]
        orderId = value['orderId'].strip().replace(".", "")


        if utm_campaign not in result:
            copy_to_clipboard_and_show(f"select campaignId from {CONFIG['table_name_select']} as c where c.campaign = '{utm_campaign}';")
            campaingId = input("campaingId: ").strip().replace(".", "")
            result[utm_campaign] = {
                "campaignId": campaingId,
                column_group_name: [orderId]
            }
        else:
            result[utm_campaign][column_group_name].append(orderId)

    return result

def generate_content(extracted_data):
    content = ""
    for key in extracted_data:
        content += f"#{key}\n"
        campaingId = extracted_data[key]['campaignId']

        for orderId in extracted_data[key][CONFIG['column_name_group_id']]:
            query = f"INSERT INTO {CONFIG['table_name_insert']} (orderId, cupomId, campaignId) VALUES('{orderId}', null, '{campaingId}');\n"
            content += query

        content += "\n"
    return content

def main():
    print("""
    GENERATE QUERIES TO INSERT TABLE
    """)

    extracted_data = extract_data()
    content = generate_content(extracted_data)
    
    if len(content) > 0:
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(content)
        print("file output.txt created successfully")
    else:
        print("nothing result")



if __name__ == "__main__":
    main()