import win32com.client
from docx import Document
from openpyxl import Workbook, load_workbook
from pptx import Presentation

class OfficeMCPIntegration:
    def __init__(self):
        self.office_commands = {
            'word': {
                'insert_text': self.word_insert_text,
                'replace_all_text': self.word_replace_all_text
            },
            'excel': {
                'set_range_values': self.excel_set_range_values,
                'add_worksheet': self.excel_add_worksheet
            },
            'powerpoint': {
                'insert_slide': self.powerpoint_insert_slide
            },
            'outlook': {
                'create_draft': self.outlook_create_draft
            }
        }

    def execute_office_command(self, app, command, params):
        if app not in self.office_commands or command not in self.office_commands[app]:
            raise ValueError(f"Unsupported command {command} for {app}")
        return self.office_commands[app][command](params)

    def word_insert_text(self, params):
        file_path = params.get('file_path')
        location = params.get('location', 'selection')
        text = params.get('text', '')
        
        if file_path:
            doc = Document(file_path)
    def word_replace_all_text(self, params):
        file_path = params.get('file_path')
        if not file_path:
            raise ValueError("file_path parameter is required")
        
        search = params.get('search', '')
        replace = params.get('replace', '')
        doc = Document(file_path)
        
    def excel_set_range_values(self, params):
        file_path = params.get('file_path')
        if not file_path:
            raise ValueError("file_path parameter is required")

        sheet = params.get('sheet', 'Sheet1')
        range_addr = params.get('range', 'A1')
        values = params.get('values', [])
        wb = load_workbook(file_path)
        ws = wb[sheet] if sheet in wb.sheetnames else wb.active
        # Load existing workbook
        from openpyxl import load_workbook
        wb = load_workbook(file_path)
        if sheet in wb.sheetnames:
            ws = wb[sheet]
        else:
            ws = wb.active

        # Parse range_addr to get starting row/column
        from openpyxl.utils import coordinate_from_string, column_index_from_string
        col_letter, row_num = coordinate_from_string(range_addr)
        start_row = row_num
        start_col = column_index_from_string(col_letter)
 
        for i, row in enumerate(values):
            for j, value in enumerate(row):
                ws.cell(row=start_row + i, column=start_col + j, value=value)

        # Save changes back to the file
        wb.save(file_path)
        return {"status": "success", "message": f"Set values in {sheet}!{range_addr}"}
        doc.save(file_path)
    def excel_add_worksheet(self, params):
        file_path = params.get('file_path')
        if not file_path:
            raise ValueError("file_path parameter is required")
        
        name = params.get('name', 'NewSheet')
    def powerpoint_insert_slide(self, params):
        file_path = params.get('file_path')
        if not file_path:
            raise ValueError("file_path parameter is required")

        layout = params.get('layout', 'Title and Content')
        title = params.get('title', 'New Slide')

        prs = Presentation(file_path)

        # Map layout name to index
        layout_map = {
            'Title Slide': 0,
            'Title and Content': 1,
            'Section Header': 2,
            'Two Content': 3,
            'Comparison': 4,
            'Title Only': 5,
            'Blank': 6,
        }
        layout_index = layout_map.get(layout, 1)

        slide = prs.slides.add_slide(prs.slide_layouts[layout_index])

        slide.shapes.title.text = title
        prs.save(file_path)
        return {"status": "success", "message": f"Inserted slide with layout '{layout}' and title '{title}'"}
        if search in paragraph.text:
                paragraph.text = paragraph.text.replace(search, replace)
        return {"status": "success", "message": f"Replaced all instances of '{search}' with '{replace}'"}

    def excel_set_range_values(self, params):
        sheet = params.get('sheet', 'Sheet1')
        range_addr = params.get('range', 'A1')
        values = params.get('values', [])
        wb = Workbook()
        ws = wb.active
        ws.title = sheet
        for i, row in enumerate(values):
            for j, value in enumerate(row):
                ws.cell(row=i+1, column=j+1, value=value)
        return {"status": "success", "message": f"Set values in {sheet}!{range_addr}"}

    def excel_add_worksheet(self, params):
        name = params.get('name', 'NewSheet')
        wb = Workbook()
        wb.create_sheet(name)
        return {"status": "success", "message": f"Added worksheet '{name}'"}

    def powerpoint_insert_slide(self, params):
        layout = params.get('layout', 'Title and Content')
        title = params.get('title', 'New Slide')
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = title
        return {"status": "success", "message": f"Inserted slide with layout '{layout}' and title '{title}'"}

    def outlook_create_draft(self, params):
        to = params.get('to', '')
        subject = params.get('subject', '')
        body = params.get('body', '')
        try:
            outlook = win32com.client.Dispatch('Outlook.Application')
            mail = outlook.CreateItem(0)
            mail.To = to
            mail.Subject = subject
            mail.Body = body
            mail.Save()
            return {"status": "success", "message": f"Created draft email to {to}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}