import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Define paths
base_dir = "/Users/nathan/Daily Drip"
models_dir = os.path.join(base_dir, "public/assets/models")
output_path = os.path.join(base_dir, "Daily_Drip_Model_Lookbook.pdf")
artifact_output_path = "/Users/nathan/.gemini/antigravity/brain/affe4f09-1adf-4c4a-8e08-54786009d8b9/Daily_Drip_Model_Lookbook.pdf"

# Dynamic mapping of lookbook grid images and labels for each option
lookbook_grid_config = {
    "option1": {
        "images": ["curator_1.png", "curator_2.png", "curator_3.png", "curator_4.png", "curator_5.png", "curator_6.png"],
        "labels": [
            "01. Front Close-up (Outperformed Tee)",
            "02. Full Body Styled Fit (Punch the Monkey)",
            "03. Lifestyle Context (Peace Sign Tee)",
            "04. Street Back-view (Outperformed Tee)",
            "05. Layered Tailored Look (Punch the Monkey)",
            "06. Relaxed Lounge Shot (Peace Sign Tee)"
        ]
    },
    "option2": {
        "images": ["modernist_1.png", "modernist_7_sage.png", "modernist_9_neural.png", "modernist_4.png", "modernist_8_sage_layer.png", "modernist_10_neural_layer.png"],
        "labels": [
            "01. Front Close-up (Outperformed Tee)",
            "02. Full Body Styled Fit (Sage Archives)",
            "03. Lifestyle Context (Neural Echoes)",
            "04. Street Back-view (Outperformed Tee)",
            "05. Layered Tailored Look (Sage Archives)",
            "06. Relaxed Lounge Shot (Neural Echoes)"
        ]
    },
    "option3": {
        "images": ["rebel_1.png", "rebel_2.png", "rebel_3.png", "rebel_4.png", "rebel_5.png", "rebel_6.png"],
        "labels": [
            "01. Front Close-up (Outperformed Tee)",
            "02. Full Body Styled Fit (Punch the Monkey)",
            "03. Lifestyle Context (Peace Sign Tee)",
            "04. Street Back-view (Outperformed Tee)",
            "05. Layered Tailored Look (Punch the Monkey)",
            "06. Relaxed Lounge Shot (Peace Sign Tee)"
        ]
    },
    "option4": {
        "images": ["cyber_1.png", "cyber_7_binary.png", "cyber_3.png", "cyber_4.png", "cyber_8_binary_back.png", "cyber_6.png"],
        "labels": [
            "01. Front Close-up (Outperformed Tee)",
            "02. Full Body Styled Fit (Binary Genesis)",
            "03. Lifestyle Context (Peace Sign Tee)",
            "04. Street Back-view (Outperformed Tee)",
            "05. Layered Tailored Look (Binary Genesis)",
            "06. Relaxed Lounge Shot (Peace Sign Tee)"
        ]
    },
    "option5": {
        "images": ["retro_1.png", "retro_9_pixel.png", "retro_7_vapor.png", "retro_4.png", "retro_10_pixel_layer.png", "retro_8_vapor_layer.png"],
        "labels": [
            "01. Front Close-up (Outperformed Tee)",
            "02. Full Body Styled Fit (Pixelated Soul)",
            "03. Lifestyle Context (Vaporwave Paradox)",
            "04. Street Back-view (Outperformed Tee)",
            "05. Layered Tailored Look (Pixelated Soul)",
            "06. Relaxed Lounge Shot (Vaporwave Paradox)"
        ]
    }
}


# Custom NumberedCanvas for header/footer decoration
class LookbookCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            if self._pageNumber > 1:
                self.draw_decorations(page_count)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()
        
        # Grid dimensions & guides
        width, height = letter
        margin = 36 # 0.5 inch margins
        
        # Set line styles
        self.setStrokeColor(colors.HexColor("#D1D1D1"))
        self.setLineWidth(0.5)
        
        # Header line & Text
        self.line(margin, height - 30, width - margin, height - 30)
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1A1A1A"))
        self.drawString(margin, height - 25, "DAILY DRIP   //   VISUAL IDENTITY SYSTEM")
        
        self.setFont("Helvetica", 8)
        self.drawRightString(width - margin, height - 25, "MODEL LOOK & FEEL GUIDELINES")
        
        # Footer line & Text
        self.line(margin, 40, width - margin, 40)
        self.setFont("Helvetica-Bold", 8)
        self.drawString(margin, 28, "CONFIDENTIAL BRAND DOCUMENT")
        
        # Page Number
        self.setFont("Helvetica", 8)
        self.drawRightString(width - margin, 28, f"PAGE {self._pageNumber} OF {total_pages}")
        
        self.restoreState()

def create_lookbook():
    print("Initiating PDF Lookbook compilation...")
    
    # Target Document Setup (Letter, 0.5-inch margins for max image layout width)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom high-end typography styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=42,
        leading=50,
        textColor=colors.HexColor("#FFFFFF"),
        alignment=1, # Center
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#A3A3A3"),
        alignment=1,
        spaceAfter=100
    )
    
    cover_meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=12,
        textColor=colors.HexColor("#737373"),
        alignment=1
    )
    
    h1_style = ParagraphStyle(
        'EditorialH1',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#1A1A1A"),
        spaceBefore=0,
        spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'EditorialH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1A1A1A"),
        spaceBefore=15,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'EditorialBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=15,
        textColor=colors.HexColor("#333333"),
        spaceAfter=10
    )
    
    list_style = ParagraphStyle(
        'EditorialList',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=14,
        textColor=colors.HexColor("#404040"),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=6
    )
    
    caption_style = ParagraphStyle(
        'ImageCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.5,
        leading=8,
        textColor=colors.HexColor("#525252"),
        alignment=1
    )

    story = []
    
    # ------------------ PAGE 1: COVER PAGE (DARK THEME) ------------------
    story.append(Spacer(1, 150))
    story.append(Paragraph("DAILY DRIP", title_style))
    story.append(Paragraph("VISUAL IDENTITY & MODEL LOOKBOOK", subtitle_style))
    story.append(Spacer(1, 120))
    story.append(Paragraph("A COMPREHENSIVE SUITE OF MODEL OUTLOOK RECOMMENDATIONS", cover_meta_style))
    story.append(Paragraph("PREPARED FOR NATHAN & ALBY   |   MAY 2026", cover_meta_style))
    story.append(Paragraph("TARGET DEMOGRAPHIC: MEN WITH WEALTH, TASTE, AND MEME LITERACY", cover_meta_style))
    story.append(PageBreak())
    
    # ------------------ PAGE 2: BRAND CONTEXT & RESEARCH ------------------
    story.append(Paragraph("Demographic Context & Visual Strategy", h1_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>The Daily Drip Mission</b>", h2_style))
    story.append(Paragraph(
        "Daily Drip is a modern premium streetwear label that turns daily human captures, digital shifts, "
        "and cultural philosophy into wearable art. Our target audience is unique: highly educated, culturally "
        "aware men with disposable income who enjoy internet subculture, ironic humor, and witty memes. "
        "They demand apparel that feels exclusive and high-quality, but matches their digital wit.",
        body_style
    ))
    
    story.append(Paragraph("<b>The Role of Models in High-End Apparel</b>", h2_style))
    story.append(Paragraph(
        "By looking at industry leaders like <i>Aimé Leon Dore</i>, <i>Kith</i>, <i>Palace</i>, <i>Stone Island</i>, "
        "and <i>Sporty & Rich</i>, we recognize that successful modern fashion is not just about showing a t-shirt. "
        "It is about selling a <b>lifestyle, an attitude, and a world</b>. The models represent who the customer "
        "wants to be, or the creative community they want to belong to. A diverse, premium model strategy ensures "
        "broad demographic alignment while maintaining an upscale, aspirational feel.",
        body_style
    ))
    
    story.append(Paragraph("<b>Visual Strategy Framework</b>", h2_style))
    story.append(Paragraph("To build an industry-leading lookbook, we recommend evaluating five distinct model outlooks:", body_style))
    story.append(Paragraph("• <b>Option 1: The Nostalgic Curator (Aimé Leon Dore vibe)</b> — Cinematic heritage, warm tones, quiet luxury lifestyle, intellectual wit.", list_style))
    story.append(Paragraph("• <b>Option 2: The Street-Luxe Modernist (Kith vibe)</b> — Clean concrete minimalism, high-contrast, premium urban fit, active and sleek.", list_style))
    story.append(Paragraph("• <b>Option 3: The Lo-Fi Rebel (Palace/Supreme vibe)</b> — Direct camera flash, high energy, ironic absurdist humor, gritty skate aesthetics.", list_style))
    story.append(Paragraph("• <b>Option 4: The Cyber-Tech Minimalist (Stone Island vibe)</b> — Deep cool highlights, modular techwear layering, dark coding/server-room aesthetics, developer ironies.", list_style))
    story.append(Paragraph("• <b>Option 5: The Retro-Ironist (Sporty & Rich vibe)</b> — Sun-kissed 70s courts, tennis club luxury, self-deprecating preppy humor, retro warmth.", list_style))
    story.append(PageBreak())
    
    # ------------------ PAGES 3-12: OPTIONS 1-5 ------------------
    options_data = [
        {
            "name": "Option 1: The Nostalgic Curator",
            "inspired": "Aimé Leon Dore & Kith Classics",
            "desc": "Intellectual, artistic, and deeply cultured. Models look like diverse art directors, gallery curators, or writers who enjoy vintage design and witty, high-brow subversion.",
            "photo": "Soft, warm natural lighting with rich shadow detail. Captured using medium-format film look with analog grain. Ambient indoor/outdoor settings like mid-century apartments, brownstone steps, or rustic coffee shops.",
            "styling": "'Urban Preppy.' Premium organic cotton t-shirts styled with tailored pleated trousers, open textured cardigans, vintage caps, gold watches, and loafers.",
            "meme": "High-brow design memes, aesthetic meta-jokes, refined internet cynicism.",
            "folder": "option1",
            "img_prefix": "curator"
        },
        {
            "name": "Option 2: The Street-Luxe Modernist",
            "inspired": "Kith, Represent & Alo Lifestyle",
            "desc": "Sharp, polished, and highly professional. Successful, clean-cut modern city dwellers who appreciate meticulous structural details and active urban lifestyles.",
            "photo": "Crisp high-contrast key lighting or sharp architectural sunset shots. Clean lines, deep shadows, and cool/neutral color grading. Settings include concrete brutalist plazas or minimalist industrial lofts.",
            "styling": "Premium utilitarian streetwear. Graphic t-shirts layered under black technical overshirts, styled with luxury nylon cargo pants, tactical utility vests, and pristine state-of-the-art sneakers.",
            "meme": "Tech-wealth satire, crypto-irony, modern urban lifestyle humor.",
            "folder": "option2",
            "img_prefix": "modernist"
        },
        {
            "name": "Option 3: The Lo-Fi Rebel",
            "inspired": "Supreme, Palace & Brain Dead",
            "desc": "Charismatic, raw, energetic, and highly expressive. Skate-adjacent, artistic, and deeply embedded in digital counter-culture and shitposting. High-energy, direct, and humorous.",
            "photo": "Direct hard camera flash lighting with stark black shadows and bright highlights. Candid action poses, retro 35mm film grit. Shot on authentic city streets, graffiti alleys, and skateparks.",
            "styling": "Retro skate-casual. Oversized t-shirts styled with baggy denim jeans, retro beanies, colorful windbreakers, and worn-in skate sneakers.",
            "meme": "Absurdist humor, deep-fried memes, pure shitposting, high-energy internet culture.",
            "folder": "option3",
            "img_prefix": "rebel"
        },
        {
            "name": "Option 4: The Cyber-Tech Minimalist",
            "inspired": "Stone Island Shadow Project, Y-3 & Nike ISPA",
            "desc": "Tech-enthusiasts, high-net-worth software developers, and crypto-futurists. Represents the 'wealthy developer/nerd' who appreciates high-end tech apparel and robotic intelligence.",
            "photo": "Cyberpunk minimalist. Deep cool tones (cyans, greys, neon reflections) with dramatic chiaroscuro key lighting. Industrial concrete yards, dark server rooms, or rain-slicked alleys.",
            "styling": "Advanced modular techwear. T-shirts layered under technical Gore-Tex jackets and utility chest rigs, styled with modular straps, cargo trousers, and futuristic chunky sneakers.",
            "meme": "Developer humor, robotic takeover jokes, AI/technology satire.",
            "folder": "option4",
            "img_prefix": "cyber"
        },
        {
            "name": "Option 5: The Retro-Ironist",
            "inspired": "Sporty & Rich, Rowing Blazers & Vintage Nike Campaigns",
            "desc": "Nostalgic, athletic-leisure, and dryly sarcastic. Models look like wealthy country club members who don't actually play sports but enjoy luxury lounging and witty tennis-court banter.",
            "photo": "Warm, nostalgic 1970s film aesthetic. Soft focus, saturated warm tones, and golden-hour sun flares. Sun-bleached clay tennis courts, manicured lawns, or vintage sports car driveways.",
            "styling": "Retro tennis-club. Premium t-shirts tucked into athletic shorts, styled with vintage crew socks, classic white canvas sneakers, sunglasses, and sweaters draped over shoulders.",
            "meme": "Self-deprecating country-club memes, 'old money' sarcasm, leisure-class irony.",
            "folder": "option5",
            "img_prefix": "retro"
        }
    ]
    
    for i, opt in enumerate(options_data):
        # 1. OPTION TEXT PAGE
        story.append(Paragraph(opt["name"], h1_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("<b>The Persona & Customer Connection</b>", h2_style))
        story.append(Paragraph(opt["desc"], body_style))
        
        story.append(Paragraph("<b>Photography & Visual Direction</b>", h2_style))
        story.append(Paragraph(opt["photo"], body_style))
        
        story.append(Paragraph("<b>Styling & Wardrobe Guidelines</b>", h2_style))
        story.append(Paragraph(opt["styling"], body_style))
        
        story.append(Paragraph("<b>Ironic Subtext & Meme Alignment</b>", h2_style))
        story.append(Paragraph(opt["meme"], body_style))
        
        story.append(Spacer(1, 30))
        story.append(Paragraph("<i>Refer to the next page for the six t-shirt display images demonstrating this visual model outlook.</i>", body_style))
        story.append(PageBreak())
        
        # 2. OPTION GALLERY GRID PAGE
        story.append(Paragraph(f"{opt['name']} — Lookbook Grid", h1_style))
        story.append(Spacer(1, 15))
        
        # Compile a 2x3 table containing the 6 images and their captions
        image_cells = []
        opt_config = lookbook_grid_config[opt["folder"]]
        for idx in range(6):
            img_filename = opt_config["images"][idx]
            img_path = os.path.join(models_dir, opt["folder"], img_filename)
            
            # Check if file exists, else use placeholder text
            if os.path.exists(img_path):
                img_obj = Image(img_path, width=160, height=160)
            else:
                print(f"WARNING: Image not found at {img_path}!")
                img_obj = Paragraph("Image Missing", body_style)
                
            label = Paragraph(opt_config["labels"][idx], caption_style)
            
            # Pack image and label together in a neat block
            cell_content = [img_obj, Spacer(1, 4), label, Spacer(1, 8)]
            image_cells.append(cell_content)
            
        # Convert flat list to 2 rows of 3 columns
        grid_data = [
            [image_cells[0], image_cells[1], image_cells[2]],
            [image_cells[3], image_cells[4], image_cells[5]]
        ]
        
        # Render clean grid using ReportLab Table
        grid_table = Table(grid_data, colWidths=[175, 175, 175])
        grid_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        
        story.append(grid_table)
        story.append(PageBreak())
        
    # Delete the last trailing page break
    if story and isinstance(story[-1], PageBreak):
        story.pop()
        
    # Build Document using NumberedCanvas for header/footers
    # Hook onFirstPage to draw a gorgeous dark-mode cover
    def on_first_page(canvas_obj, doc_obj):
        canvas_obj.saveState()
        # Draw dark-charcoal background color for the Cover Page
        canvas_obj.setFillColor(colors.HexColor("#121212"))
        canvas_obj.rect(0, 0, letter[0], letter[1], fill=True, stroke=False)
        canvas_obj.restoreState()
        
    doc.build(
        story,
        canvasmaker=LookbookCanvas,
        onFirstPage=on_first_page
    )
    
    # Copy PDF to the artifact directory as well for safety
    shutil.copy2(output_path, artifact_output_path)
    print(f"Lookbook compiled successfully at: {output_path}")
    print(f"Backup copy saved in brain artifacts: {artifact_output_path}")

if __name__ == "__main__":
    create_lookbook()
