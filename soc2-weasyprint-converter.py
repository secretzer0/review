#!/usr/bin/env python3
"""
SOC2 Markdown to PDF/HTML Converter using WeasyPrint
Converts SOC2 policy markdown documents to professional PDF format with company branding
Also preserves HTML output for web serving
"""

import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


class SOC2WeasyPrintConverter:
    def __init__(self, logo_path='ovesiteai_logo.png'):
        self.logo_path = logo_path
        self.font_config = FontConfiguration()
        
    def extract_metadata(self, content):
        """Extract document metadata from markdown header"""
        metadata = {
            'title': 'Untitled Document',
            'version': '1.0',
            'effective_date': datetime.now().strftime('%B %d, %Y'),
            'last_updated': '',
            'last_reviewed': '',
            'classification': 'Internal',
            'owner': '',
            'approved_by': ''
        }
        
        # Extract main title
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
        
        # Extract metadata fields
        patterns = {
            'version': r'\*\*Document Version\*\*:\s*(.+)',
            'effective_date': r'\*\*Effective Date\*\*:\s*(.+)',
            'last_updated': r'\*\*Last Updated\*\*:\s*(.+)',
            'last_reviewed': r'\*\*Last Reviewed\*\*:\s*(.+)',
            'classification': r'\*\*Classification\*\*:\s*(.+)',
            'owner': r'\*\*Owner\*\*:\s*(.+)',
            'approved_by': r'\*\*Approved By\*\*:\s*(.+)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                metadata[key] = match.group(1).strip()
        
        return metadata
    
    def preprocess_markdown(self, content):
        """Preprocess markdown to remove metadata that will be displayed separately"""
        lines = content.split('\n')
        processed_lines = []
        i = 0
        in_toc = False
        
        while i < len(lines):
            line = lines[i]
            
            # Skip the main title (we'll add it separately in HTML)
            if i == 0 and re.match(r'^# .+$', line):
                i += 1
                continue
            
            # Skip the subtitle line (## OverSiteAI, LLC)
            if i < 3 and re.match(r'^## .+$', line) and 'OverSiteAI' in line:
                i += 1
                continue
            
            # Skip metadata lines
            if i < 20 and re.match(r'^\*\*(?:Document Version|Effective Date|Last Updated|Last Reviewed|Classification|Owner|Approved By)\*\*:', line):
                i += 1
                continue
            
            # Skip separator lines at the beginning
            if i < 20 and line.strip() == '---':
                i += 1
                continue
            
            # Process TOC to show only top-level items
            if line.strip() == "## Table of Contents" or line.strip() == "Table of Contents":
                in_toc = True
                processed_lines.append(line)
                i += 1
                continue
            
            if in_toc:
                # End of TOC when we hit the next section
                if re.match(r'^#{1,3}\s+\d+\.?\s+', line):
                    in_toc = False
                    processed_lines.append(line)
                    i += 1
                    continue
                
                # Only include top-level TOC items (starting with a number)
                if re.match(r'^\d+\.\s+\[', line):
                    processed_lines.append(line)
                    i += 1
                    continue
                
                # Skip subsection entries (starting with spaces or dashes)
                if re.match(r'^\s*-\s*\d+\.\d+', line) or line.strip().startswith('-'):
                    i += 1
                    continue
                
                # Keep empty lines and other content
                processed_lines.append(line)
                i += 1
                continue
            
            processed_lines.append(line)
            i += 1
        
        return '\n'.join(processed_lines)
    
    def generate_css(self):
        """Generate CSS for the PDF/HTML with TeX Gyre Schola font"""
        logo_url = f"file://{os.path.abspath(self.logo_path)}"
        
        css_content = """
        /* Font imports - TeX Gyre Schola (New Century Schoolbook) */
        @font-face {
            font-family: 'TeX Gyre Schola';
            src: local('TeX Gyre Schola'),
                 url('file:///usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreschola-regular.otf') format('opentype');
            font-weight: normal;
            font-style: normal;
        }
        
        @font-face {
            font-family: 'TeX Gyre Schola';
            src: local('TeX Gyre Schola Bold'),
                 url('file:///usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreschola-bold.otf') format('opentype');
            font-weight: bold;
            font-style: normal;
        }
        
        @font-face {
            font-family: 'TeX Gyre Schola';
            src: local('TeX Gyre Schola Italic'),
                 url('file:///usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreschola-italic.otf') format('opentype');
            font-weight: normal;
            font-style: italic;
        }
        
        @font-face {
            font-family: 'TeX Gyre Schola';
            src: local('TeX Gyre Schola Bold Italic'),
                 url('file:///usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreschola-bolditalic.otf') format('opentype');
            font-weight: bold;
            font-style: italic;
        }
        
        /* Page setup */
        @page {
            size: letter;
            margin: 0.75in 0.75in 1in 0.75in;  /* top right bottom left */
            
            @top-left {
                content: '';
                width: 50px;
                height: 40px;
                background-image: url('""" + logo_url + """');
                background-size: contain;
                background-repeat: no-repeat;
                background-position: left center;
                margin-top: -0.25in;
            }
            
            @top-center {
                content: 'OverSiteAI, LLC';
                font-family: 'TeX Gyre Schola', 'DejaVu Serif', 'Times New Roman', serif;
                font-weight: bold;
                font-size: 12pt;
                color: #1e3a5f;
                margin-top: -0.25in;
            }
            
            @top-right {
                content: '';
            }
            
            @bottom-center {
                content: 'Page ' counter(page) ' of ' counter(pages);
                font-family: 'TeX Gyre Schola', 'DejaVu Serif', 'Times New Roman', serif;
                font-size: 10pt;
                color: #7f8c8d;
            }
            
            @bottom-left {
                content: 'Confidential and Proprietary - © 2025 OverSiteAI, LLC';
                font-family: 'TeX Gyre Schola', 'DejaVu Serif', 'Times New Roman', serif;
                font-style: italic;
                font-size: 8pt;
                color: #7f8c8d;
            }
        }
        
        /* Keep header/footer on all pages including first */
        
        /* Base styles */
        body {
            font-family: 'TeX Gyre Schola', 'DejaVu Serif', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #2c3e50;
            text-align: justify;
            padding-top: 0.5in;
            border-top: 2px solid #1e3a5f;
        }
        
        /* Title page */
        .title-page {
            text-align: center;
            padding-top: 2in;
            page-break-after: always;
        }
        
        .document-title {
            font-size: 24pt;
            font-weight: bold;
            color: #1e3a5f;
            margin-bottom: 1in;
        }
        
        .metadata-table {
            margin: 0 auto;
            margin-top: 1in;
            border-collapse: collapse;
            text-align: left;
        }
        
        .metadata-table td {
            padding: 6px 12px;
            border: 1px solid #e1e8ed;
            background-color: #f8f9fa;
        }
        
        .metadata-table td:first-child {
            font-weight: bold;
            color: #1e3a5f;
            width: 180px;
        }
        
        .metadata-table td:last-child {
            color: #2c3e50;
            width: 300px;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'TeX Gyre Schola', 'DejaVu Serif', 'Times New Roman', serif;
            color: #1e3a5f;
            page-break-after: avoid;
        }
        
        h1 { font-size: 18pt; margin-top: 24pt; margin-bottom: 12pt; }
        h2 { font-size: 16pt; margin-top: 18pt; margin-bottom: 10pt; }
        h3 { font-size: 14pt; margin-top: 12pt; margin-bottom: 8pt; }
        
        /* TOC specific styling */
        .toc {
            page-break-after: always;
        }
        
        .toc h2 {
            text-align: left;
        }
        
        .toc ul {
            list-style: none;
            padding-left: 0;
        }
        
        .toc li {
            margin: 4pt 0;
        }
        
        .toc > ul > li {
            font-size: 11pt;
            margin: 6pt 0;
        }
        
        .toc ul ul {
            padding-left: 20pt;
        }
        
        .toc ul ul li {
            font-size: 10pt;
            color: #2c3e50;
        }
        
        .toc ul ul ul li {
            color: #7f8c8d;
        }
        
        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 12pt 0;
        }
        
        th {
            background-color: #1e3a5f;
            color: white;
            font-weight: bold;
            padding: 8pt;
            text-align: left;
        }
        
        td {
            padding: 8pt;
            border: 1px solid #e1e8ed;
        }
        
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        /* Lists */
        ul, ol {
            margin: 12pt 0;
            padding-left: 20pt;
        }
        
        li {
            margin: 6pt 0;
        }
        
        /* Code blocks */
        pre {
            background-color: #f8f9fa;
            border: 1px solid #e1e8ed;
            padding: 10pt;
            margin: 12pt 0;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            overflow-x: auto;
        }
        
        code {
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background-color: #f8f9fa;
            padding: 1pt 3pt;
        }
        
        /* Blockquotes */
        blockquote {
            border-left: 4px solid #1e3a5f;
            padding-left: 12pt;
            margin-left: 0;
            color: #555;
            font-style: italic;
        }
        
        /* Images */
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 12pt auto;
        }
        
        /* Links - for web version */
        a {
            color: #4a90e2;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        /* Page break utilities */
        .page-break {
            page-break-after: always;
        }
        
        /* Header line decoration */
        .header-line {
            border-top: 2px solid #1e3a5f;
            margin-top: 12pt;
            margin-bottom: 24pt;
        }
        """
        
        return css_content
    
    def markdown_to_html(self, markdown_content):
        """Convert markdown to HTML with metadata"""
        metadata = self.extract_metadata(markdown_content)
        processed_content = self.preprocess_markdown(markdown_content)
        
        # Configure markdown with extensions
        md = markdown.Markdown(extensions=[
            'extra',  # Tables, footnotes, etc.
            'codehilite',  # Code highlighting
            'toc',  # Table of contents
            'nl2br',  # New line to break
            'sane_lists'  # Better list handling
        ])
        
        # Convert markdown to HTML
        html_content = md.convert(processed_content)
        
        # Build complete HTML document
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata['title']} - OverSiteAI, LLC</title>
    <style>
{self.generate_css()}
    </style>
</head>
<body>
    <!-- Title Page -->
    <div class="title-page">
        <h1 class="document-title">{metadata['title']}</h1>
        
        <table class="metadata-table">
            <tr>
                <td>Document Version:</td>
                <td>{metadata['version']}</td>
            </tr>
            <tr>
                <td>Effective Date:</td>
                <td>{metadata['effective_date']}</td>
            </tr>
"""
        
        # Add optional metadata fields
        if metadata.get('last_updated'):
            html_template += f"""            <tr>
                <td>Last Updated:</td>
                <td>{metadata['last_updated']}</td>
            </tr>
"""
        
        if metadata.get('last_reviewed'):
            html_template += f"""            <tr>
                <td>Last Reviewed:</td>
                <td>{metadata['last_reviewed']}</td>
            </tr>
"""
        
        html_template += f"""            <tr>
                <td>Classification:</td>
                <td>{metadata['classification']}</td>
            </tr>
            <tr>
                <td>Owner:</td>
                <td>{metadata['owner']}</td>
            </tr>
            <tr>
                <td>Approved By:</td>
                <td>{metadata['approved_by']}</td>
            </tr>
        </table>
    </div>
    
    <!-- Main Content -->
    <div class="main-content">
        <div class="header-line"></div>
        {html_content}
    </div>
</body>
</html>"""
        
        return html_template
    
    def convert_file(self, input_file, output_pdf=None, output_html=None):
        """Convert a markdown file to PDF and HTML"""
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        if not input_path.suffix.lower() == '.md':
            raise ValueError(f"Input file must be a markdown file (.md): {input_file}")
        
        # Read markdown content
        with open(input_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Generate output filenames if not provided
        if output_pdf is None:
            output_pdf = input_path.with_suffix('.pdf')
        if output_html is None:
            output_html = input_path.with_suffix('.html')
        
        # Convert markdown to HTML
        html_content = self.markdown_to_html(markdown_content)
        
        # Save HTML file
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Generate PDF from HTML
        HTML(string=html_content, base_url=str(input_path.parent)).write_pdf(
            str(output_pdf),
            font_config=self.font_config
        )
        
        return output_pdf, output_html


def main():
    parser = argparse.ArgumentParser(
        description='Convert SOC2 markdown documents to PDF and HTML using WeasyPrint'
    )
    parser.add_argument(
        'input',
        help='Input markdown file or directory containing markdown files'
    )
    parser.add_argument(
        '-p', '--pdf',
        help='Output PDF file (default: same name with .pdf extension)'
    )
    parser.add_argument(
        '-w', '--html',
        help='Output HTML file (default: same name with .html extension)'
    )
    parser.add_argument(
        '-l', '--logo',
        default='ovesiteai_logo.png',
        help='Path to company logo (default: ovesiteai_logo.png)'
    )
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='Convert all .md files in directory'
    )
    
    args = parser.parse_args()
    
    # Check logo path
    logo_path = args.logo
    if not os.path.isabs(logo_path):
        # Try to find logo in script directory
        script_dir = Path(__file__).parent
        if (script_dir / logo_path).exists():
            logo_path = str(script_dir / logo_path)
    
    converter = SOC2WeasyPrintConverter(logo_path=logo_path)
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        # Convert single file
        try:
            output_pdf, output_html = converter.convert_file(
                input_path, 
                args.pdf, 
                args.html
            )
            print(f"✅ Converted: {input_path}")
            print(f"   PDF: {output_pdf}")
            print(f"   HTML: {output_html}")
        except Exception as e:
            print(f"❌ Error converting {input_path}: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    elif input_path.is_dir() and args.all:
        # Convert all markdown files in directory
        output_dir = input_path
        
        success_count = 0
        error_count = 0
        
        for md_file in sorted(input_path.glob('*.md')):
            # Skip certain files
            if md_file.name.startswith('README') or md_file.name.startswith('.'):
                continue
            
            try:
                output_pdf, output_html = converter.convert_file(md_file)
                print(f"✅ Converted: {md_file.name}")
                print(f"   PDF: {output_pdf.name}")
                print(f"   HTML: {output_html.name}")
                success_count += 1
            except Exception as e:
                print(f"❌ Error converting {md_file.name}: {e}")
                error_count += 1
        
        print(f"\n📊 Summary: {success_count} successful, {error_count} failed")
    
    else:
        print(f"Error: {input_path} is not a valid file or --all flag not specified for directory")
        sys.exit(1)


if __name__ == '__main__':
    main()
