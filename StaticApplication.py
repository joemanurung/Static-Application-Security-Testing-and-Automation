import os
import subprocess
import json
from fpdf import FPDF

def run_semgrep(directory):
    """
    Run Semgrep on the specified directory and return the results in JSON format.
    """
    try:
        # Run semgrep scan
        result = subprocess.run(
            ['semgrep', '--config', 'auto', '--json', directory],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            print(f"Error running semgrep: {result.stderr}")
            return None
        
        return json.loads(result.stdout)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def generate_pdf_report(vulnerabilities, output_file):
    """
    Generate a PDF report from the semgrep vulnerability results.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Static Application Security Testing (SAST) Report", ln=True, align='C')

    pdf.ln(10)  # Add space

    # Vulnerabilities Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Vulnerabilities Found:", ln=True)

    pdf.set_font("Arial", size=12)
    if not vulnerabilities:
        pdf.cell(200, 10, txt="No vulnerabilities found.", ln=True)
    else:
        for index, vuln in enumerate(vulnerabilities, start=1):
            pdf.ln(8)  # Add space between vulnerabilities
            pdf.cell(200, 10, txt=f"{index}. {vuln['check_id']}", ln=True)
            pdf.cell(200, 10, txt=f"   Severity: {vuln['extra']['severity']}", ln=True)
            pdf.cell(200, 10, txt=f"   Message: {vuln['extra']['message']}", ln=True)
            pdf.cell(200, 10, txt=f"   File: {vuln['path']}", ln=True)
            pdf.cell(200, 10, txt=f"   Line: {vuln['start']['line']}", ln=True)

    # Output the PDF
    pdf.output(output_file)

def main(directory, output_file):
    # Step 1: Run Semgrep on the specified directory
    print(f"Scanning directory: {directory}")
    scan_results = run_semgrep(directory)

    if not scan_results:
        print("No results from the scan. Exiting.")
        return

    # Step 2: Extract vulnerabilities from Semgrep results
    vulnerabilities = scan_results.get('results', [])

    # Step 3: Generate the PDF report
    print(f"Generating PDF report: {output_file}")
    generate_pdf_report(vulnerabilities, output_file)

    print(f"Report generated: {output_file}")

if __name__ == "__main__":
    directory_to_scan = input("Enter the directory to scan: ")
    output_pdf_file = input("Enter the output PDF file name (e.g., report.pdf): ")
    
    main(directory_to_scan, output_pdf_file)
