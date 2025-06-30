#!/usr/bin/env python3
"""
SOC2 Markdown to PDF Converter
Converts SOC2 policy markdown documents to professional PDF format with company branding
"""

import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import Image, KeepTogether, ListFlowable, ListItem, Preformatted
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from PIL import Image as PILImage


class NumberedCanvas(canvas.Canvas):
    """Custom canvas to add headers and footers with page numbers"""
    
    def __init__(self, *args, **kwargs):
        self.logo_path = kwargs.pop('logo_path', None)
        self.company_name = kwargs.pop('company_name', 'OverSiteAI, LLC')
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        """Add headers and footers to each page"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
        
    def draw_header_footer(self, page_count):
        """Draw header with logo and company name, and footer with page number"""
        self.saveState()
        
        # Header
        header_y = letter[1] - 0.5 * inch
        
        # Add logo if available
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                # Load logo with PIL to handle transparency
                img = PILImage.open(self.logo_path)
                
                # Convert RGBA to RGB with white background if needed
                if img.mode in ('RGBA', 'LA'):
                    # Create a white background
                    background = PILImage.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
                    else:
                        background.paste(img, mask=img.split()[1])
                    img = background
                
                # Calculate dimensions
                aspect = img.width / img.height
                logo_height = 0.4 * inch
                logo_width = logo_height * aspect
                
                # Save to BytesIO
                img_buffer = BytesIO()
                img.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                
                # Draw logo using ImageReader for better handling
                img_reader = ImageReader(img_buffer)
                self.drawImage(img_reader, 0.75 * inch, header_y - logo_height/2, 
                             width=logo_width, height=logo_height, preserveAspectRatio=True)
                
                # Company name centered - try to use serif font
                try:
                    self.setFont("DejaVuSerif-Bold", 12)
                except:
                    self.setFont("Helvetica-Bold", 12)
                    
                self.setFillColor(colors.HexColor('#1e3a5f'))
                self.drawCentredString(letter[0] / 2.0, header_y - 0.1 * inch, 
                              self.company_name)
            except Exception as e:
                print(f"Warning: Could not load logo: {e}")
                # Fall back to text only centered
                try:
                    self.setFont("DejaVuSerif-Bold", 14)
                except:
                    self.setFont("Helvetica-Bold", 14)
                self.setFillColor(colors.HexColor('#1e3a5f'))
                self.drawCentredString(letter[0] / 2.0, header_y, self.company_name)
        else:
            # Text only header - centered
            try:
                self.setFont("DejaVuSerif-Bold", 14)
            except:
                self.setFont("Helvetica-Bold", 14)
            self.setFillColor(colors.HexColor('#1e3a5f'))
            self.drawCentredString(letter[0] / 2.0, header_y, self.company_name)
        
        # Header line
        self.setStrokeColor(colors.HexColor('#1e3a5f'))
        self.setLineWidth(2)
        self.line(0.75 * inch, header_y - 0.3 * inch, letter[0] - 0.75 * inch, header_y - 0.3 * inch)
        
        # Footer
        footer_y = 0.5 * inch
        page_num = self._pageNumber
        
        # Page number
        try:
            self.setFont("DejaVuSerif", 10)
        except:
            self.setFont("Helvetica", 10)
        self.setFillColor(colors.HexColor('#7f8c8d'))
        page_text = f"Page {page_num} of {page_count}"
        self.drawCentredString(letter[0] / 2.0, footer_y, page_text)
        
        # Footer line
        self.setStrokeColor(colors.HexColor('#e1e8ed'))
        self.setLineWidth(1)
        self.line(0.75 * inch, footer_y + 0.3 * inch, letter[0] - 0.75 * inch, footer_y + 0.3 * inch)
        
        # Confidentiality notice
        try:
            self.setFont("DejaVuSerif-Italic", 8)
        except:
            self.setFont("Helvetica-Oblique", 8)
        self.drawCentredString(letter[0] / 2.0, footer_y - 0.2 * inch, 
                             "Confidential and Proprietary - © 2025 OverSiteAI, LLC")
        
        self.restoreState()


class SOC2PDFConverter:
    def __init__(self, logo_path='ovesiteai_logo.png'):
        self.logo_path = logo_path
        self._register_fonts()
        self.styles = self._create_styles()
    
    def _register_fonts(self):
        """Register custom fonts with ReportLab"""
        # Try to find and register DejaVu Serif fonts (usually available on most systems)
        font_paths = [
            # Common Linux paths
            '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf',
            # Alternative paths
            '/usr/share/fonts/dejavu/DejaVuSerif.ttf',
            '/usr/share/fonts/dejavu/DejaVuSerif-Bold.ttf',
            '/usr/share/fonts/dejavu/DejaVuSerif-Italic.ttf',
            '/usr/share/fonts/dejavu/DejaVuSerif-BoldItalic.ttf',
        ]
        
        registered = False
        for i in range(0, len(font_paths), 4):
            if os.path.exists(font_paths[i]):
                try:
                    pdfmetrics.registerFont(TTFont('DejaVuSerif', font_paths[i]))
                    if os.path.exists(font_paths[i+1]):
                        pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', font_paths[i+1]))
                    if os.path.exists(font_paths[i+2]):
                        pdfmetrics.registerFont(TTFont('DejaVuSerif-Italic', font_paths[i+2]))
                    if os.path.exists(font_paths[i+3]):
                        pdfmetrics.registerFont(TTFont('DejaVuSerif-BoldItalic', font_paths[i+3]))
                    
                    # Register font family
                    from reportlab.pdfbase.pdfmetrics import registerFontFamily
                    registerFontFamily('DejaVuSerif',
                                     normal='DejaVuSerif',
                                     bold='DejaVuSerif-Bold',
                                     italic='DejaVuSerif-Italic',
                                     boldItalic='DejaVuSerif-BoldItalic')
                    registered = True
                    break
                except Exception as e:
                    print(f"Warning: Could not register DejaVu Serif fonts: {e}")
        
        if not registered:
            print("Info: Using default Helvetica fonts (DejaVu Serif not found)")
        
    def _create_styles(self):
        """Create custom styles for PDF generation"""
        styles = getSampleStyleSheet()
        
        # Determine font family to use
        try:
            # Test if DejaVuSerif was registered
            pdfmetrics.getFont('DejaVuSerif')
            font_family = 'DejaVuSerif'
            heading_font = 'DejaVuSerif'
        except:
            # Fall back to Times-Roman which is similar to Century Schoolbook
            font_family = 'Times-Roman'
            heading_font = 'Times-Bold'
        
        # Title style
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Title'],
            fontName=heading_font,
            fontSize=24,
            textColor=colors.HexColor('#1e3a5f'),
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        # Subtitle style
        styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=styles['Title'],
            fontName=font_family,
            fontSize=18,
            textColor=colors.HexColor('#4a90e2'),
            spaceAfter=24,
            alignment=TA_CENTER
        ))
        
        # Heading styles
        styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=styles['Heading1'],
            fontName=heading_font,
            fontSize=18,
            textColor=colors.HexColor('#1e3a5f'),
            spaceBefore=24,
            spaceAfter=12,
            keepWithNext=True
        ))
        
        styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=styles['Heading2'],
            fontName=heading_font,
            fontSize=16,
            textColor=colors.HexColor('#1e3a5f'),
            spaceBefore=18,
            spaceAfter=10,
            keepWithNext=True
        ))
        
        styles.add(ParagraphStyle(
            name='CustomHeading3',
            parent=styles['Heading3'],
            fontName=heading_font,
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceBefore=12,
            spaceAfter=8,
            keepWithNext=True
        ))
        
        # Body text style
        styles.add(ParagraphStyle(
            name='CustomBodyText',
            parent=styles['BodyText'],
            fontName=font_family,
            fontSize=11,
            textColor=colors.HexColor('#2c3e50'),
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16
        ))
        
        # Metadata style
        styles.add(ParagraphStyle(
            name='Metadata',
            parent=styles['Normal'],
            fontName=font_family,
            fontSize=10,
            textColor=colors.HexColor('#7f8c8d'),
            spaceAfter=6
        ))
        
        # Code style
        styles.add(ParagraphStyle(
            name='CustomCode',
            parent=styles['Code'],
            fontSize=9,
            leftIndent=20,
            rightIndent=20,
            backColor=colors.HexColor('#f8f9fa'),
            borderColor=colors.HexColor('#e1e8ed'),
            borderWidth=1,
            borderPadding=10,
            spaceAfter=12
        ))
        
        # List styles
        styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=styles['Normal'],
            fontName=font_family,
            fontSize=11,
            textColor=colors.HexColor('#2c3e50'),
            leftIndent=20,
            spaceAfter=6
        ))
        
        # TOC styles
        styles.add(ParagraphStyle(
            name='TOCLevel1',
            parent=styles['Normal'],
            fontName=font_family,
            fontSize=11,
            textColor=colors.HexColor('#2c3e50'),
            leftIndent=0,
            spaceAfter=6
        ))
        
        styles.add(ParagraphStyle(
            name='TOCLevel2',
            parent=styles['Normal'],
            fontName=font_family,
            fontSize=10,
            textColor=colors.HexColor('#2c3e50'),
            leftIndent=20,
            spaceAfter=4
        ))
        
        styles.add(ParagraphStyle(
            name='TOCLevel3',
            parent=styles['Normal'],
            fontName=font_family,
            fontSize=10,
            textColor=colors.HexColor('#7f8c8d'),
            leftIndent=40,
            spaceAfter=4
        ))
        
        return styles
    
    def extract_metadata(self, content):
        """Extract document metadata from markdown header"""
        metadata = {
            'title': 'Untitled Document',
            'subtitle': '',
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
        
        # Extract subtitle
        subtitle_match = re.search(r'^## (.+)$', content, re.MULTILINE)
        if subtitle_match and subtitle_match.start() < 100:  # Near the top
            subtitle = subtitle_match.group(1).strip()
            # Fix company name capitalization
            subtitle = subtitle.replace('OversiteAI', 'OverSiteAI')
            metadata['subtitle'] = subtitle
        
        # Extract metadata fields - updated to match the standardized format
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
    
    def parse_toc_from_markdown(self, content):
        """Parse Table of Contents directly from markdown"""
        story = []
        lines = content.split('\n')
        
        in_toc = False
        toc_items = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Check for TOC start
            if line == "Table of Contents" or line == "## Table of Contents":
                story.append(Paragraph("Table of Contents", self.styles['CustomHeading2']))
                in_toc = True
                i += 1
                continue
            
            # Process TOC entries
            if in_toc and line:
                # Check if we've reached the end of TOC (next heading)
                if re.match(r'^#{1,3}\s+\d+\.?\s+', line) or (not line.startswith(('-', ' ', '\t', '1', '2', '3', '4', '5', '6', '7', '8', '9'))):
                    in_toc = False
                    # Add space after TOC
                    story.append(Spacer(1, 0.3 * inch))
                    continue
                
                # Parse TOC entry
                # Level 1: "1. [Title](#anchor)"
                match1 = re.match(r'^(\d+)\.\s*\[([^\]]+)\]', line)
                if match1:
                    story.append(Paragraph(f"{match1.group(1)}. {match1.group(2)}", self.styles['TOCLevel1']))
                    i += 1
                    continue
                
                # Level 2: "- 1.1 [Title](#anchor)" or "  - 1.1 [Title](#anchor)"
                match2 = re.match(r'^\s*-\s*(\d+\.\d+)\s*\[([^\]]+)\]', line)
                if match2:
                    story.append(Paragraph(f"{match2.group(1)} {match2.group(2)}", self.styles['TOCLevel2']))
                    i += 1
                    continue
                
                # Level 3: "  - 1.1.1 [Title](#anchor)"
                match3 = re.match(r'^\s*-\s*(\d+\.\d+\.\d+)\s*\[([^\]]+)\]', line)
                if match3:
                    story.append(Paragraph(f"{match3.group(1)} {match3.group(2)}", self.styles['TOCLevel3']))
                    i += 1
                    continue
            
            i += 1
        
        return story, in_toc
    
    def markdown_to_pdf_elements(self, markdown_content):
        """Convert markdown content to PDF elements"""
        story = []
        
        # Extract metadata
        metadata = self.extract_metadata(markdown_content)
        
        # Add title page elements
        story.append(Paragraph(metadata['title'], self.styles['CustomTitle']))
        
        story.append(Spacer(1, 0.5 * inch))
        
        # Add metadata table
        metadata_data = [
            ['Document Version:', metadata['version']],
            ['Effective Date:', metadata['effective_date']],
            ['Classification:', metadata['classification']],
            ['Owner:', metadata['owner']],
            ['Approved By:', metadata['approved_by']]
        ]
        
        # Add Last Updated and Last Reviewed if they exist
        if metadata.get('last_updated'):
            metadata_data.insert(2, ['Last Updated:', metadata['last_updated']])
        if metadata.get('last_reviewed'):
            metadata_data.insert(3 if metadata.get('last_updated') else 2, ['Last Reviewed:', metadata['last_reviewed']])
        
        # Determine table font
        try:
            pdfmetrics.getFont('DejaVuSerif-Bold')
            table_font_bold = 'DejaVuSerif-Bold'
            table_font = 'DejaVuSerif'
        except:
            table_font_bold = 'Helvetica-Bold'
            table_font = 'Helvetica'
        
        metadata_table = Table(metadata_data, colWidths=[2.5 * inch, 4 * inch])
        metadata_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), table_font_bold, 10),
            ('FONT', (1, 0), (1, -1), table_font, 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1e3a5f')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e1e8ed')),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa'))
        ]))
        
        story.append(metadata_table)
        story.append(PageBreak())
        
        # Parse TOC first
        toc_elements, _ = self.parse_toc_from_markdown(markdown_content)
        story.extend(toc_elements)
        
        # Add page break after TOC
        if toc_elements:
            story.append(PageBreak())
        
        # Process the rest of the markdown content
        story.extend(self._parse_markdown_content(markdown_content))
        
        return story
    
    def _parse_markdown_content(self, content):
        """Parse markdown content directly to PDF elements"""
        story = []
        lines = content.split('\n')
        
        i = 0
        in_toc = False
        in_code_block = False
        code_lines = []
        in_list = False
        list_items = []
        in_table = False
        table_rows = []
        
        while i < len(lines):
            line = lines[i]
            
            # Skip title and subtitle at the beginning (already handled separately)
            if i == 0 and re.match(r'^# .+$', line):
                i += 1
                continue
            if i == 1 and re.match(r'^## .+$', line):
                i += 1
                continue
            
            # Skip metadata lines at the beginning
            if i < 20 and re.match(r'^\*\*(?:Document Version|Effective Date|Last Updated|Last Reviewed|Classification|Owner|Approved By)\*\*:', line):
                i += 1
                continue
            
            # Skip separator lines at the beginning
            if i < 20 and line.strip() == '---':
                i += 1
                continue
            
            # Skip TOC section
            if line.strip() == "Table of Contents" or line.strip() == "## Table of Contents":
                in_toc = True
                i += 1
                continue
            
            if in_toc:
                # Skip until we hit a numbered heading
                if re.match(r'^#{1,3}\s+\d+\.?\s+', line):
                    in_toc = False
                else:
                    i += 1
                    continue
            
            # Code blocks
            if line.strip().startswith('```'):
                if in_code_block:
                    # End code block
                    if code_lines:
                        code_text = '\n'.join(code_lines)
                        story.append(Preformatted(code_text, self.styles['CustomCode']))
                    code_lines = []
                    in_code_block = False
                else:
                    # Start code block
                    in_code_block = True
                i += 1
                continue
            
            if in_code_block:
                code_lines.append(line)
                i += 1
                continue
            
            # Headers
            if line.startswith('#'):
                # Process any pending list
                if list_items:
                    story.extend(self._create_list_items(list_items))
                    list_items = []
                    in_list = False
                
                # Parse header
                header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
                if header_match:
                    level = len(header_match.group(1))
                    text = header_match.group(2).strip()
                    
                    if level == 1:
                        story.append(Paragraph(text, self.styles['CustomHeading1']))
                    elif level == 2:
                        story.append(Paragraph(text, self.styles['CustomHeading2']))
                    elif level == 3:
                        story.append(Paragraph(text, self.styles['CustomHeading3']))
                    else:
                        story.append(Paragraph(f"<b>{text}</b>", self.styles['CustomBodyText']))
                
                i += 1
                continue
            
            # Lists
            list_match = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.+)$', line)
            if list_match:
                indent = len(list_match.group(1))
                marker = list_match.group(2)
                text = list_match.group(3)
                
                # Convert markdown formatting
                text = self._process_inline_markdown(text)
                
                list_items.append({
                    'indent': indent,
                    'marker': marker,
                    'text': text,
                    'ordered': marker[0].isdigit()
                })
                in_list = True
                i += 1
                continue
            
            # Empty line
            if not line.strip():
                # Process any pending list
                if list_items:
                    story.extend(self._create_list_items(list_items))
                    list_items = []
                    in_list = False
                # Process any pending table
                if table_rows and len(table_rows) > 1:
                    story.append(self._create_table(table_rows))
                    table_rows = []
                    in_table = False
                i += 1
                continue
            
            # Tables
            if '|' in line and not in_code_block:
                # Check if it's a table row
                parts = [p.strip() for p in line.split('|')]
                if len(parts) > 2:  # At least one cell
                    # Check if it's a separator row
                    if all(p.replace('-', '').replace(':', '').strip() == '' for p in parts[1:-1]):
                        # It's a separator, skip it
                        i += 1
                        continue
                    else:
                        # It's a data row
                        row_data = parts[1:-1]  # Remove empty first and last
                        table_rows.append(row_data)
                        in_table = True
                        i += 1
                        continue
            
            # Regular paragraph
            if not in_list and not in_table:
                # Process any pending list
                if list_items:
                    story.extend(self._create_list_items(list_items))
                    list_items = []
                    in_list = False
                
                # Process any pending table
                if table_rows and len(table_rows) > 1:
                    story.append(self._create_table(table_rows))
                    table_rows = []
                    in_table = False
                
                # Check for images first
                image_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', line.strip())
                if image_match:
                    alt_text = image_match.group(1)
                    image_path = image_match.group(2)
                    
                    # Handle relative paths - assume images are in same directory as markdown
                    if not os.path.isabs(image_path):
                        # Get the directory of the markdown file being processed
                        md_dir = os.path.dirname(os.path.abspath(self.current_input_file)) if hasattr(self, 'current_input_file') else '.'
                        image_path = os.path.join(md_dir, image_path)
                    
                    if os.path.exists(image_path):
                        try:
                            # Create image element
                            img = Image(image_path, width=5*inch, height=3*inch, kind='proportional')
                            story.append(img)
                            # Add caption if alt text exists
                            if alt_text:
                                caption_style = ParagraphStyle(
                                    'ImageCaption',
                                    parent=self.styles['Metadata'],
                                    alignment=TA_CENTER,
                                    fontSize=9,
                                    textColor=colors.HexColor('#7f8c8d')
                                )
                                story.append(Paragraph(f"<i>{alt_text}</i>", caption_style))
                            story.append(Spacer(1, 0.2*inch))
                        except Exception as e:
                            print(f"Warning: Could not load image {image_path}: {e}")
                            # Add placeholder text
                            story.append(Paragraph(f"[Image: {alt_text or os.path.basename(image_path)}]", 
                                                 self.styles['CustomBodyText']))
                    else:
                        print(f"Warning: Image not found: {image_path}")
                        # Add placeholder text
                        story.append(Paragraph(f"[Missing Image: {alt_text or os.path.basename(image_path)}]", 
                                             self.styles['CustomBodyText']))
                else:
                    # Process regular paragraph
                    para_text = line.strip()
                    if para_text and not para_text.startswith('---'):
                        para_text = self._process_inline_markdown(para_text)
                        story.append(Paragraph(para_text, self.styles['CustomBodyText']))
            
            i += 1
        
        # Process any remaining list items
        if list_items:
            story.extend(self._create_list_items(list_items))
        
        return story
    
    def _create_table(self, rows):
        """Create a table from markdown table rows"""
        if not rows:
            return None
        
        # Determine column widths
        num_cols = len(rows[0])
        col_widths = [6.5 * inch / num_cols] * num_cols
        
        # Create style for table cells
        cell_style = ParagraphStyle(
            'TableCell',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2c3e50'),
            alignment=TA_LEFT,
            leading=12
        )
        
        header_style = ParagraphStyle(
            'TableHeader',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.white,
            alignment=TA_LEFT,
            leading=13
        )
        
        # Convert all cells to Paragraph objects for proper text wrapping
        table_data = []
        for row_idx, row in enumerate(rows):
            para_row = []
            for cell in row:
                # Process the cell text to handle markdown formatting
                cell_text = self._process_inline_markdown(str(cell))
                # Use header style for first row, regular style for others
                style = header_style if row_idx == 0 else cell_style
                para = Paragraph(cell_text, style)
                para_row.append(para)
            table_data.append(para_row)
        
        # Create table with Paragraph objects
        table = Table(table_data, colWidths=col_widths)
        
        # Determine table font
        try:
            pdfmetrics.getFont('DejaVuSerif-Bold')
            table_font_bold = 'DejaVuSerif-Bold'
            table_font = 'DejaVuSerif'
        except:
            table_font_bold = 'Helvetica-Bold'
            table_font = 'Helvetica'
        
        # Apply table style (no font commands needed since we're using Paragraphs)
        style_commands = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a5f')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e1e8ed')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)
        ]
        
        table.setStyle(TableStyle(style_commands))
        return table
    
    def _process_inline_markdown(self, text):
        """Convert inline markdown to ReportLab formatting"""
        # Bold
        text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__([^_]+)__', r'<b>\1</b>', text)
        
        # Italic - just remove the formatting since fonts might not be available
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        
        # Code
        text = re.sub(r'`([^`]+)`', r'<font face="Courier">\1</font>', text)
        
        # Links - just show the text
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        
        return text
    
    def _create_list_items(self, items):
        """Create properly formatted list items"""
        story = []
        
        for item in items:
            indent_level = item['indent'] // 2  # Convert spaces to levels
            base_indent = 20 + (indent_level * 20)
            
            if item['ordered']:
                bullet = f"{item['marker']} "
            else:
                bullet = "• " if indent_level == 0 else "- "
            
            style = ParagraphStyle(
                'ListItem',
                parent=self.styles['CustomBullet'],
                leftIndent=base_indent,
                firstLineIndent=-15
            )
            
            para = Paragraph(f"{bullet}{item['text']}", style)
            story.append(para)
        
        return story
    
    def convert_file(self, input_file, output_file=None):
        """Convert a single markdown file to PDF"""
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        if not input_path.suffix.lower() == '.md':
            raise ValueError(f"Input file must be a markdown file (.md): {input_file}")
        
        # Store current input file for image path resolution
        self.current_input_file = str(input_path)
        
        # Read markdown content
        with open(input_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Generate output filename if not provided
        if output_file is None:
            output_file = input_path.with_suffix('.pdf')
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_file),
            pagesize=letter,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=1 * inch,
            bottomMargin=1 * inch
        )
        
        # Build PDF with custom canvas
        story = self.markdown_to_pdf_elements(markdown_content)
        
        # Build PDF with custom canvas for headers/footers
        doc.build(
            story,
            canvasmaker=lambda filename, *args, **kwargs: NumberedCanvas(
                filename, *args,
                logo_path=self.logo_path,
                company_name='OverSiteAI, LLC',
                **{k: v for k, v in kwargs.items() if k not in ['logo_path', 'company_name']}
            )
        )
        
        return output_file


def main():
    parser = argparse.ArgumentParser(
        description='Convert SOC2 markdown documents to professional PDF format with company branding'
    )
    parser.add_argument(
        'input',
        help='Input markdown file or directory containing markdown files'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output PDF file or directory (default: same name with .pdf extension)'
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
    
    converter = SOC2PDFConverter(logo_path=logo_path)
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        # Convert single file
        try:
            output_file = converter.convert_file(input_path, args.output)
            print(f"✅ Converted: {input_path} → {output_file}")
        except Exception as e:
            print(f"❌ Error converting {input_path}: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    elif input_path.is_dir() and args.all:
        # Convert all markdown files in directory
        output_dir = Path(args.output) if args.output else input_path
        output_dir.mkdir(exist_ok=True)
        
        success_count = 0
        error_count = 0
        
        for md_file in sorted(input_path.glob('*.md')):
            # Skip certain files
            if md_file.name.startswith('README') or md_file.name.startswith('.'):
                continue
            
            output_file = output_dir / md_file.with_suffix('.pdf').name
            try:
                converter.convert_file(md_file, output_file)
                print(f"✅ Converted: {md_file.name} → {output_file.name}")
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
