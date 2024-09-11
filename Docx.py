import docxtpl


    
async def create_document(table_list: list, organization_name: str, FIO: str, phone_number: str, email: str, address: str, sum: int):
    with open('templates/template.docx', 'rb') as file:
        doc = docxtpl.DocxTemplate(file)
        context = { 
            'organization_name': organization_name,
            'FIO': FIO,
            'phone_number': phone_number,
            'email': email,
            'address': address,
            'text_organization': organization_name,
            'sum': sum,
            'table_contents': table_list
        }
        doc.render(context)
        doc.save('table.docx')
        
