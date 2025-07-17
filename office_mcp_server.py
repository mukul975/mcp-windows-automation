#!/usr/bin/env python3
"""
Microsoft Office MCP Integration Server
Integrates Office.js with MCP for Microsoft 365 Desktop Apps
"""

import json
import subprocess
import time
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("office-mcp-server")

class OfficeMCPIntegration:
    def __init__(self):
        self.office_commands = {
            "Word": {
                "InsertText": self.word_insert_text,
                "ReplaceAllText": self.word_replace_all_text,
                "GetSelection": self.word_get_selection,
                "InsertParagraph": self.word_insert_paragraph,
                "SetDocumentTitle": self.word_set_document_title
            },
            "Excel": {
                "SetRangeValues": self.excel_set_range_values,
                "GetRangeValues": self.excel_get_range_values,
                "AddWorksheet": self.excel_add_worksheet,
                "CreateChart": self.excel_create_chart,
                "FormatRange": self.excel_format_range
            },
            "PowerPoint": {
                "InsertSlide": self.powerpoint_insert_slide,
                "DeleteSlide": self.powerpoint_delete_slide,
                "SetSlideTitle": self.powerpoint_set_slide_title,
                "AddTextBox": self.powerpoint_add_textbox
            },
            "Outlook": {
                "CreateDraft": self.outlook_create_draft,
                "SendEmail": self.outlook_send_email,
                "GetCurrentMessage": self.outlook_get_current_message,
                "AddAttachment": self.outlook_add_attachment
            }
        }
    
    def create_office_js_script(self, app: str, command: str, params: Dict[str, Any]) -> str:
        """Generate Office.js script based on app, command, and parameters"""
        
        if app == "Word":
            return self._generate_word_script(command, params)
        elif app == "Excel":
            return self._generate_excel_script(command, params)
        elif app == "PowerPoint":
            return self._generate_powerpoint_script(command, params)
        elif app == "Outlook":
            return self._generate_outlook_script(command, params)
        else:
            raise ValueError(f"Unsupported Office app: {app}")
    
    def _generate_word_script(self, command: str, params: Dict[str, Any]) -> str:
        """Generate Word-specific Office.js script"""
        
        if command == "InsertText":
            return f"""
            Office.onReady(function() {{
                Word.run(async function (context) {{
                    const range = context.document.getSelection();
                    range.insertText("{params.get('text', '')}", Word.InsertLocation.replace);
                    await context.sync();
                    return {{ status: "success", message: "Text inserted successfully" }};
                }}).catch(function (error) {{
                    console.error("Error: " + error);
                    return {{ status: "error", message: error.message }};
                }});
            }});
            """
        
        elif command == "ReplaceAllText":
            return f"""
            Office.onReady(function() {{
                Word.run(async function (context) {{
                    const searchResults = context.document.body.search("{params.get('search', '')}", {{matchCase: false}});
                    context.load(searchResults, 'items');
                    await context.sync();
                    
                    for (let i = 0; i < searchResults.items.length; i++) {{
                        searchResults.items[i].insertText("{params.get('replace', '')}", Word.InsertLocation.replace);
                    }}
                    
                    await context.sync();
                    return {{ status: "success", message: "Text replaced successfully", count: searchResults.items.length }};
                }}).catch(function (error) {{
                    console.error("Error: " + error);
                    return {{ status: "error", message: error.message }};
                }});
            }});
            """
        
        elif command == "InsertParagraph":
            return f"""
            Office.onReady(function() {{
                Word.run(async function (context) {{
                    const body = context.document.body;
                    body.insertParagraph("{params.get('text', '')}", Word.InsertLocation.end);
                    await context.sync();
                    return {{ status: "success", message: "Paragraph inserted successfully" }};
                }}).catch(function (error) {{
                    console.error("Error: " + error);
                    return {{ status: "error", message: error.message }};
                }});
            }});
            """
        
        return ""
    
    def _generate_excel_script(self, command: str, params: Dict[str, Any]) -> str:
        """Generate Excel-specific Office.js script"""
        
        if command == "SetRangeValues":
            values_json = json.dumps(params.get('values', []))
            return f"""
            Office.onReady(function() {{
                Excel.run(async function (context) {{
                    let sheet = context.workbook.worksheets.getItem("{params.get('sheet', 'Sheet1')}");
                    let range = sheet.getRange("{params.get('range', 'A1')}");
                    range.values = {values_json};
                    await context.sync();
                    return {{ status: "success", message: "Range values set successfully" }};
                }}).catch(function (error) {{
                    console.error("Error: " + error);
                    return {{ status: "error", message: error.message }};
                }});
            }});
            """
        
        elif command == "AddWorksheet":
            return f"""
            Office.onReady(function() {{
                Excel.run(async function (context) {{
                    let sheet = context.workbook.worksheets.add("{params.get('name', 'NewSheet')}");
                    sheet.activate();
                    await context.sync();
                    return {{ status: "success", message: "Worksheet added successfully" }};
                }}).catch(function (error) {{
                    console.error("Error: " + error);
                    return {{ status: "error", message: error.message }};
                }});
            }});
            """
        
        elif command == "GetRangeValues":
            return f"""
            Office.onReady(function() {{
                Excel.run(async function (context) {{
                    let sheet = context.workbook.worksheets.getItem("{params.get('sheet', 'Sheet1')}");
                    let range = sheet.getRange("{params.get('range', 'A1')}");
                    range.load("values");
                    await context.sync();
                    return {{ status: "success", values: range.values }};
                }}).catch(function (error) {{
                    console.error("Error: " + error);
                    return {{ status: "error", message: error.message }};
                }});
            }});
            """
        
        return ""
    
    def _generate_powerpoint_script(self, command: str, params: Dict[str, Any]) -> str:
        """Generate PowerPoint-specific Office.js script"""
        
        if command == "InsertSlide":
            return f"""
            Office.onReady(function() {{
                PowerPoint.run(async function (context) {{
                    const slide = context.presentation.slides.add();
                    
                    // Try to set title if provided
                    if ("{params.get('title', '')}") {{
                        // Add title placeholder logic here
                        const titleShape = slide.shapes.getItemOrNullObject("Title 1");
                        if (!titleShape.isNullObject) {{
                            titleShape.textFrame.textRange.text = "{params.get('title', '')}";
                        }}
                    }}
                    
                    await context.sync();
                    return {{ status: "success", message: "Slide inserted successfully" }};
                }}).catch(function (error) {{
                    console.error("Error: " + error);
                    return {{ status: "error", message: error.message }};
                }});
            }});
            """
        
        elif command == "DeleteSlide":
            return f"""
            Office.onReady(function() {{
                PowerPoint.run(async function (context) {{
                    const slide = context.presentation.slides.getItemAt({params.get('index', 0)});
                    slide.delete();
                    await context.sync();
                    return {{ status: "success", message: "Slide deleted successfully" }};
                }}).catch(function (error) {{
                    console.error("Error: " + error);
                    return {{ status: "error", message: error.message }};
                }});
            }});
            """
        
        return ""
    
    def _generate_outlook_script(self, command: str, params: Dict[str, Any]) -> str:
        """Generate Outlook-specific Office.js script"""
        
        if command == "CreateDraft":
            return f"""
            Office.onReady(function() {{
                if (Office.context.mailbox.item) {{
                    const item = Office.context.mailbox.item;
                    
                    // Set subject
                    item.subject.setAsync("{params.get('subject', '')}", function(result) {{
                        if (result.status === Office.AsyncResultStatus.Failed) {{
                            console.error("Failed to set subject: " + result.error.message);
                        }}
                    }});
                    
                    // Set body
                    item.body.setAsync("{params.get('body', '')}", {{coercionType: Office.CoercionType.Text}}, function(result) {{
                        if (result.status === Office.AsyncResultStatus.Failed) {{
                            console.error("Failed to set body: " + result.error.message);
                        }}
                    }});
                    
                    // Set recipients
                    item.to.setAsync([{{emailAddress: "{params.get('to', '')}"}}], function(result) {{
                        if (result.status === Office.AsyncResultStatus.Failed) {{
                            console.error("Failed to set recipients: " + result.error.message);
                        }}
                    }});
                    
                    return {{ status: "success", message: "Draft created successfully" }};
                }} else {{
                    return {{ status: "error", message: "No mail item context available" }};
                }}
            }});
            """
        
        return ""
    
    def execute_office_command(self, app: str, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Office.js command via JavaScript injection"""
        
        try:
            # Generate Office.js script
            script = self.create_office_js_script(app, command, params)
            
            if not script:
                return {"status": "error", "message": f"Unsupported command: {command} for {app}"}
            
            # Create temporary HTML file with Office.js script
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <script src="https://appsforoffice.microsoft.com/lib/1/hosted/office.js"></script>
            </head>
            <body>
                <script>
                    {script}
                </script>
            </body>
            </html>
            """
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(html_content)
                temp_file = f.name
            
            # For demonstration, we'll return a simulated response
            # In a real implementation, you'd need to inject this into the Office application
            return {
                "status": "success",
                "message": f"Office.js command prepared for {app}",
                "command": command,
                "params": params,
                "script_file": temp_file
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # Individual command handlers
    def word_insert_text(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("Word", "InsertText", params)
    
    def word_replace_all_text(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("Word", "ReplaceAllText", params)
    
    def word_get_selection(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("Word", "GetSelection", params)
    
    def word_insert_paragraph(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("Word", "InsertParagraph", params)
    
    def word_set_document_title(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("Word", "SetDocumentTitle", params)
    
    def excel_set_range_values(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("Excel", "SetRangeValues", params)
    
    def excel_get_range_values(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("Excel", "GetRangeValues", params)
    
    def excel_add_worksheet(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("Excel", "AddWorksheet", params)
    
    def excel_create_chart(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("Excel", "CreateChart", params)
    
    def excel_format_range(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("Excel", "FormatRange", params)
    
    def powerpoint_insert_slide(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("PowerPoint", "InsertSlide", params)
    
    def powerpoint_delete_slide(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("PowerPoint", "DeleteSlide", params)
    
    def powerpoint_set_slide_title(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("PowerPoint", "SetSlideTitle", params)
    
    def powerpoint_add_textbox(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("PowerPoint", "AddTextBox", params)
    
    def outlook_create_draft(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("Outlook", "CreateDraft", params)
    
    def outlook_send_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("Outlook", "SendEmail", params)
    
    def outlook_get_current_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("Outlook", "GetCurrentMessage", params)
    
    def outlook_add_attachment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.execute_office_command("Outlook", "AddAttachment", params)

# Global instance
office_integration = OfficeMCPIntegration()

# ==============================================================================
# MCP TOOLS FOR OFFICE INTEGRATION
# ==============================================================================

@mcp.tool()
async def office_execute_command(app: str, command: str, params_json: str) -> str:
    """Execute Office.js command for Microsoft 365 apps"""
    try:
        params = json.loads(params_json)
        result = office_integration.execute_office_command(app, command, params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error executing Office command: {str(e)}"

@mcp.tool()
async def word_insert_text(location: str = "selection", text: str = "Hello from MCP!") -> str:
    """Insert text at the current selection in Word"""
    try:
        params = {"location": location, "text": text}
        result = office_integration.word_insert_text(params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error inserting text in Word: {str(e)}"

@mcp.tool()
async def word_replace_all_text(search: str, replace: str) -> str:
    """Find and replace all instances of text in Word"""
    try:
        params = {"search": search, "replace": replace}
        result = office_integration.word_replace_all_text(params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error replacing text in Word: {str(e)}"

@mcp.tool()
async def excel_set_range_values(sheet: str = "Sheet1", range_addr: str = "A1", values: str = "[[\"Hello\", \"World\"]]") -> str:
    """Set values in an Excel range"""
    try:
        values_array = json.loads(values)
        params = {"sheet": sheet, "range": range_addr, "values": values_array}
        result = office_integration.excel_set_range_values(params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error setting Excel range values: {str(e)}"

@mcp.tool()
async def excel_add_worksheet(name: str = "NewSheet") -> str:
    """Add a new worksheet to Excel"""
    try:
        params = {"name": name}
        result = office_integration.excel_add_worksheet(params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error adding Excel worksheet: {str(e)}"

@mcp.tool()
async def powerpoint_insert_slide(layout: str = "Title and Content", title: str = "New Slide") -> str:
    """Insert a new slide in PowerPoint"""
    try:
        params = {"layout": layout, "title": title}
        result = office_integration.powerpoint_insert_slide(params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error inserting PowerPoint slide: {str(e)}"

@mcp.tool()
async def outlook_create_draft(to: str, subject: str, body: str) -> str:
    """Create a new email draft in Outlook"""
    try:
        params = {"to": to, "subject": subject, "body": body}
        result = office_integration.outlook_create_draft(params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error creating Outlook draft: {str(e)}"

@mcp.tool()
async def office_get_supported_commands() -> str:
    """Get list of all supported Office commands"""
    try:
        commands = {}
        for app, app_commands in office_integration.office_commands.items():
            commands[app] = list(app_commands.keys())
        
        return json.dumps({
            "supported_apps": list(commands.keys()),
            "commands": commands,
            "total_commands": sum(len(cmds) for cmds in commands.values())
        }, indent=2)
    except Exception as e:
        return f"Error getting supported commands: {str(e)}"

@mcp.tool()
async def office_create_manifest() -> str:
    """Create a basic Office Add-in manifest template"""
    try:
        manifest_content = """<?xml version="1.0" encoding="UTF-8"?>
<OfficeApp xmlns="http://schemas.microsoft.com/office/appforoffice/1.1"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:type="ContentApp">
  <Id>12345678-1234-1234-1234-123456789012</Id>
  <Version>1.0.0.0</Version>
  <ProviderName>MCP Office Integration</ProviderName>
  <DefaultLocale>en-US</DefaultLocale>
  <DisplayName DefaultValue="MCP Office Integration"/>
  <Description DefaultValue="Model Context Protocol integration for Office"/>
  <Hosts>
    <Host Name="Document"/>
    <Host Name="Workbook"/>
    <Host Name="Presentation"/>
    <Host Name="Mailbox"/>
  </Hosts>
  <Requirements>
    <Sets>
      <Set Name="WordApi" MinVersion="1.1"/>
      <Set Name="ExcelApi" MinVersion="1.1"/>
      <Set Name="PowerPointApi" MinVersion="1.1"/>
      <Set Name="Mailbox" MinVersion="1.1"/>
    </Sets>
  </Requirements>
  <DefaultSettings>
    <SourceLocation DefaultValue="https://localhost:3000/index.html"/>
  </DefaultSettings>
  <Permissions>ReadWriteDocument</Permissions>
</OfficeApp>"""
        
        # Save manifest to file
        manifest_file = "office_mcp_manifest.xml"
        with open(manifest_file, 'w') as f:
            f.write(manifest_content)
        
        return f"Office Add-in manifest created: {manifest_file}"
    except Exception as e:
        return f"Error creating manifest: {str(e)}"

if __name__ == "__main__":
    mcp.run()
