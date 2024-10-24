import subprocess
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# Function to run Semgrep scan on the specified directory
def run_semgrep_scan(directory):
    try:
        # Running semgrep scan and capturing output as JSON
        result = subprocess.run(
            ['semgrep', '--config', 'auto', '--json', directory],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Return the JSON result
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error running Semgrep: {e}")
        return None

# Function to create a PDF report from the semgrep results
def create_pdf_report(scan_results, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 50, "Semgrep Scan Report")

    y_position = height - 100
    c.setFont("Helvetica", 10)

    for result in scan_results.get('results', []):
        if y_position < 50:
            c.showPage()
            y_position = height - 50
        c.setFillColor(colors.red)
        c.drawString(100, y_position, f"File: {result['path']}")
        y_position -= 20
        c.setFillColor(colors.black)
        c.drawString(120, y_position, f"Rule: {result['check_id']}")
        y_position -= 20
        c.drawString(120, y_position, f"Message: {result['extra']['message']}")
        y_position -= 20
        c.drawString(120, y_position, f"Line: {result['start']['line']}")
        y_position -= 30

    c.save()
    print(f"PDF report created: {output_file}")

# Main function to run the scan and generate PDF
def main():
    # Specify the directory to scan
    directory_to_scan = input("Enter the directory to scan with Semgrep: ")
    output_pdf = "semgrep_scan_report.pdf"

    # Run the Semgrep scan
    print("Running Semgrep scan...")
    scan_results = run_semgrep_scan(directory_to_scan)

    if scan_results:
        # Create PDF report
        print("Creating PDF report...")
        create_pdf_report(scan_results, output_pdf)
    else:
        print("No results from Semgrep scan.")

if __name__ == "__main__":
    main()
