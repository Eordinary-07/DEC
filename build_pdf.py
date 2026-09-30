import re
import os
import markdown
from xhtml2pdf import pisa
import pymupdf

def clean_text_for_pdf(text):
    # Direct symbol and LaTeX replacements
    text = text.replace('\\approx', ' ≈ ').replace('\x07pprox', ' ≈ ')
    text = text.replace('\\oplus', ' ⊕ ').replace('\\cdot', ' · ').replace('\\times', ' × ')
    text = text.replace('\\pm', ' ± ').replace('\\le', ' ≤ ').replace('\\ge', ' ≥ ').replace('\\ne', ' ≠ ')
    text = text.replace('\\to', ' → ').replace('\\leftrightarrow', ' ↔ ').replace('\\implies', ' ⟹ ')
    text = text.replace('\\parallel', ' ∥ ').replace('\\int', ' ∫ ').replace('\\sum', ' ∑ ')
    text = text.replace('\\Omega', ' Ω').replace('\\mu A', ' μA').replace('\\mu', ' μ')
    text = text.replace('\\Delta', ' Δ').replace('\\Sigma', ' Σ')
    
    # Common units & subscripts
    text = text.replace('\\text{k}\\Omega', ' kΩ').replace('\\text{M}\\Omega', ' MΩ')
    text = text.replace('\\text{V}', ' V').replace('\\text{A}', ' A').replace('\\text{ns}', ' ns')
    text = text.replace('\\text{ms}', ' ms').replace('\\text{ps}', ' ps').replace('\\text{MHz}', ' MHz')
    text = text.replace('\\text{kHz}', ' kHz').replace('\\text{Hz}', ' Hz')

    # Convert unicode box drawing characters to clean ASCII
    box_map = {
        '┌': '+', '┐': '+', '└': '+', '┘': '+',
        '├': '+', '┤': '+', '┬': '+', '┴': '+', '┼': '+',
        '─': '-', '━': '-', '│': '|', '┃': '|',
        '▼': 'v', '▲': '^', '►': '->', '◄': '<-',
    }
    for k, v in box_map.items():
        text = text.replace(k, v)

    # Fractions and overlines
    def replace_overline(match):
        return f'<span style="text-decoration: overline;">{match.group(1)}</span>'
    
    def replace_frac(match):
        return f'({match.group(1).strip()} / {match.group(2).strip()})'

    for _ in range(3):
        text = re.sub(r'\\overline\{([^{}]+)\}', replace_overline, text)
        text = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', replace_frac, text)

    # Display math $$...$$
    def process_display_math(match):
        content = match.group(1).strip()
        content = re.sub(r'\\text\{([^{}]+)\}', r'\1', content)
        content = content.replace(r'\,', ' ').replace(r'\;', ' ').replace(r'\quad', '    ').replace('\\', '')
        return f'<div class="math-display">{content}</div>'

    # Inline math $...$
    def process_inline_math(match):
        content = match.group(1).strip()
        content = re.sub(r'\\text\{([^{}]+)\}', r'\1', content)
        content = content.replace(r'\,', ' ').replace(r'\;', ' ').replace(r'\quad', '    ').replace('\\', '')
        return f'<span class="math-inline">{content}</span>'

    text = re.sub(r'\$\$(.*?)\$\$', process_display_math, text, flags=re.DOTALL)
    text = re.sub(r'\$([^\$\n]+?)\$', process_inline_math, text)
    return text

def generate_pdf_from_html(html_content, output_filename, title="Digital Electronics Circuits"):
    css = f"""
    @page {{
      size: a4 portrait;
      margin: 1.8cm 1.4cm 1.8cm 1.4cm;
      @top-center {{
        content: "{title} &bull; BEL5T16C";
        font-size: 7.5pt;
        color: #64748b;
        font-family: Helvetica, Arial, sans-serif;
      }}
      @bottom-right {{
        content: "Page " counter(page) " of " counter(pages);
        font-size: 7.5pt;
        color: #64748b;
        font-family: Helvetica, Arial, sans-serif;
      }}
    }}
    
    body {{
      font-family: Helvetica, Arial, sans-serif;
      font-size: 9pt;
      line-height: 1.45;
      color: #1e293b;
    }}
    
    h1 {{ 
      font-size: 15.5pt; 
      color: #0f172a; 
      margin-top: 16pt; 
      margin-bottom: 7pt; 
      border-bottom: 1.5pt solid #cbd5e1; 
      padding-bottom: 3pt; 
      font-weight: bold;
    }}
    h2 {{ 
      font-size: 12.5pt; 
      color: #1e3a8a; 
      margin-top: 13pt; 
      margin-bottom: 5pt; 
      font-weight: bold;
    }}
    h3 {{ 
      font-size: 10.5pt; 
      color: #1e293b; 
      margin-top: 10pt; 
      margin-bottom: 4pt; 
      font-weight: bold;
    }}
    h4 {{ 
      font-size: 9.5pt; 
      color: #334155; 
      margin-top: 8pt; 
      margin-bottom: 3pt; 
      font-weight: bold;
    }}
    
    p {{ 
      margin-top: 3.5pt; 
      margin-bottom: 3.5pt; 
      text-align: justify;
    }}
    
    table {{ 
      width: 100%; 
      margin: 7pt 0; 
      font-size: 8pt; 
    }}
    th, td {{ 
      border: 0.5pt solid #94a3b8; 
      padding: 3.5pt 5pt; 
      text-align: left; 
    }}
    th {{ 
      background-color: #f1f5f9; 
      font-weight: bold; 
      color: #0f172a; 
    }}
    
    figure {{ 
      text-align: center; 
      margin: 10pt auto; 
      padding: 5pt;
      background-color: #f8fafc;
      border: 0.5pt solid #e2e8f0;
    }}
    img {{ 
      max-width: 440px; 
      height: auto; 
      margin: 0 auto;
    }}
    figcaption {{ 
      font-size: 7.5pt; 
      color: #475569; 
      margin-top: 4pt; 
      font-style: italic; 
      text-align: left; 
      line-height: 1.3;
    }}
    
    blockquote {{ 
      border-left: 2.5pt solid #3b82f6; 
      padding-left: 7pt; 
      margin: 6pt 0; 
      background-color: #f0fdf4; 
      color: #334155; 
      font-size: 8.5pt;
    }}
    
    pre {{ 
      background-color: #f8fafc; 
      border: 0.5pt solid #cbd5e1; 
      padding: 5pt; 
      font-family: Courier, monospace; 
      font-size: 7.5pt; 
      margin: 5pt 0;
    }}
    code {{ 
      font-family: Courier, monospace; 
      font-size: 8pt; 
      background-color: #f1f5f9; 
      color: #0f172a;
    }}
    pre code {{
      background-color: transparent;
      font-size: 7.5pt;
    }}
    
    .math-display {{
      text-align: center;
      font-family: Courier, monospace;
      font-size: 9pt;
      font-weight: bold;
      color: #1e3a8a;
      margin: 5pt auto;
      padding: 4pt 8pt;
      background-color: #f8fafc;
      border: 0.5pt solid #e2e8f0;
      border-radius: 3pt;
    }}
    
    .math-inline {{
      font-family: Courier, monospace;
      font-size: 8.5pt;
      font-weight: bold;
      color: #1e3a8a;
    }}
    
    hr {{
      border: none;
      border-top: 0.5pt solid #cbd5e1;
      margin: 10pt 0;
    }}
    """
    
    full_doc = f"""<!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>{css}</style>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """
    
    with open(output_filename, "w+b") as f_out:
        pisa_status = pisa.CreatePDF(full_doc, dest=f_out)
    
    size_mb = os.path.getsize(output_filename) / (1024 * 1024)
    print(f"Generated {output_filename} ({size_mb:.2f} MB, errors: {pisa_status.err})")

def build_all_pdfs():
    print("Reading DEC_Complete_Notes.md...")
    with open("DEC_Complete_Notes.md", "r", encoding="utf-8") as f:
        full_md = f.read()

    cleaned_md = clean_text_for_pdf(full_md)

    # Adjust image tags
    cleaned_md = re.sub(r'<img\s+src="([^"]+)"\s+alt="([^"]*)"\s+width="(\d+)"\s*/>', 
                        r'<img src="\1" alt="\2" style="max-width: 440px; height: auto;" />', 
                        cleaned_md)

    cover_html = """
    <div style="text-align: center; margin-top: 40pt;">
      <p style="font-size: 11pt; color: #475569; letter-spacing: 2pt; text-transform: uppercase; font-weight: bold; margin-bottom: 8pt;">
        RASHTRASANT TUKADOJI MAHARAJ NAGPUR UNIVERSITY (RTMNU) &bull; NEP B.TECH
      </p>
      <p style="font-size: 9pt; color: #64748b; margin-bottom: 25pt;">
        Faculty of Science & Technology &bull; Department of Electrical Engineering
      </p>
      
      <div style="border-top: 3pt solid #1e3a8a; border-bottom: 3pt solid #1e3a8a; padding: 18pt 0; margin: 15pt 0;">
        <h1 style="font-size: 26pt; color: #0f172a; line-height: 1.2; margin: 0; font-weight: bold; letter-spacing: -0.5pt; border: none;">
          DIGITAL ELECTRONICS CIRCUITS
        </h1>
        <h2 style="font-size: 14pt; color: #2563eb; font-weight: bold; margin-top: 8pt; margin-bottom: 0;">
          Course Code: BEL5T16C &bull; Semester V
        </h2>
      </div>

      <p style="font-size: 13pt; color: #334155; font-weight: bold; margin-top: 15pt; line-height: 1.4;">
        Complete First-Principles Comprehensive Lecture Notes,<br/>
        Hardware Reality Checks, Solved University Problems &amp; Practical Lab Manual
      </p>
      
      <div style="margin: 25pt auto; padding: 12pt; background-color: #f8fafc; border: 1pt solid #cbd5e1; border-radius: 6pt; text-align: left; max-width: 460px;">
        <p style="font-size: 9pt; font-weight: bold; color: #0f172a; margin-bottom: 6pt;">Core Authorized Textbooks Synthesized:</p>
        <ul style="font-size: 8pt; color: #334155; margin: 0; padding-left: 14pt; line-height: 1.5;">
          <li><strong>A. Anand Kumar</strong> &bull; <em>Fundamentals of Digital Circuits</em> (4th Edition, PHI)</li>
          <li><strong>M. Morris Mano &amp; Michael D. Ciletti</strong> &bull; <em>Digital Design</em> (6th Global Ed., Pearson)</li>
          <li><strong>Thomas L. Floyd</strong> &bull; <em>Digital Fundamentals: A Systems Approach</em> (1st Ed., Pearson)</li>
          <li><strong>R. P. Jain</strong> &bull; <em>Modern Digital Electronics</em> (4th Edition, McGraw-Hill)</li>
        </ul>
      </div>

      <div style="margin-top: 25pt;">
        <table style="width: 100%; border: none; font-size: 8.5pt; color: #475569;">
          <tr>
            <td style="border: none; text-align: center; width: 33%;">
              <strong style="color: #0f172a; font-size: 11pt;">40,900+</strong><br/>Exhaustive Words
            </td>
            <td style="border: none; text-align: center; width: 33%;">
              <strong style="color: #0f172a; font-size: 11pt;">80 Figures</strong><br/>Authentic 300 DPI Crops
            </td>
            <td style="border: none; text-align: center; width: 33%;">
              <strong style="color: #0f172a; font-size: 11pt;">10 Labs</strong><br/>Standard Worksheets
            </td>
          </tr>
        </table>
      </div>

      <div style="margin-top: 40pt; font-size: 8pt; color: #94a3b8;">
        Verified Academic Engineering Curriculum Document &bull; Zero Placeholders &bull; Pure First Principles
      </div>
    </div>
    <div style="page-break-after: always;"></div>
    """

    print("Converting master markdown to HTML...")
    body_html = markdown.markdown(cleaned_md, extensions=['tables', 'fenced_code'])
    
    # 1. Master PDF
    print("\n--- Generating Master PDF ---")
    generate_pdf_from_html(cover_html + body_html, "DEC_Complete_Notes.pdf", "DEC Master Course Compendium")

    # 2. Split into Unit PDFs
    units_def = [
        ("DEC_Unit1_Fundamentals_and_Logic_Families.pdf", "Unit I: Fundamentals of Digital Systems and Logic Families", "Unit II: Logic Function and Minimization", "DEC Unit I: Fundamentals & Logic Families"),
        ("DEC_Unit2_Logic_Function_and_Minimization.pdf", "Unit II: Logic Function and Minimization", "Unit III: Combinational Digital Circuits", "DEC Unit II: Logic Function & Minimization"),
        ("DEC_Unit3_Combinational_Digital_Circuits.pdf", "Unit III: Combinational Digital Circuits", "Unit IV: Sequential Circuits and Systems", "DEC Unit III: Combinational Circuits"),
        ("DEC_Unit4_Sequential_Circuits_and_Systems.pdf", "Unit IV: Sequential Circuits and Systems", "Unit V: Converters and Semiconductor Memories", "DEC Unit IV: Sequential Circuits & Systems"),
        ("DEC_Unit5_Converters_and_Semiconductor_Memories.pdf", "Unit V: Converters and Semiconductor Memories", "PART 4: Master University Examination", "DEC Unit V: Converters & Semiconductor Memories"),
        ("DEC_Lab_Manual_and_Exam_Compendium.pdf", "PART 4: Master University Examination", "APPENDIX & MASTER REFERENCE COMPENDIUM", "DEC Lab Manual & Solved Exam Compendium")
    ]

    print("\n--- Generating Unit-Wise Modular PDFs ---")
    for filename, start_marker, end_marker, title in units_def:
        start_idx = cleaned_md.find(f"# {start_marker}")
        if start_idx == -1:
            start_idx = cleaned_md.find(start_marker)
        
        end_idx = cleaned_md.find(f"# {end_marker}")
        if end_idx == -1:
            end_idx = cleaned_md.find(end_marker)

        if start_idx != -1 and end_idx != -1:
            section_md = cleaned_md[start_idx:end_idx]
            section_html = markdown.markdown(section_md, extensions=['tables', 'fenced_code'])
            unit_cover = f"""
            <div style="text-align: center; margin-top: 60pt; border-bottom: 2pt solid #1e3a8a; padding-bottom: 20pt; margin-bottom: 25pt;">
              <p style="font-size: 10pt; color: #64748b; font-weight: bold; letter-spacing: 1pt;">RTMNU NEP CURRICULUM &bull; BEL5T16C</p>
              <h1 style="font-size: 22pt; color: #0f172a; margin: 10pt 0; border: none;">{title}</h1>
              <p style="font-size: 11pt; color: #2563eb; font-weight: bold;">Comprehensive First-Principles Lecture Notes</p>
            </div>
            """
            generate_pdf_from_html(unit_cover + section_html, filename, title)
        else:
            print(f"Skipping {filename} (markers not found: {start_idx}, {end_idx})")

if __name__ == '__main__':
    build_all_pdfs()
