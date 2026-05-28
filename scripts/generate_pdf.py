import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def create_onboarding_pdf(output_path):
    # Setup document geometry with 0.75-inch (54pt) margins
    margin = 54
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )
    
    styles = getSampleStyleSheet()
    
    # ----------------------------------------------------
    # BRAND STYLE DEFINITIONS (The Daily Drip Earth Tones)
    # ----------------------------------------------------
    SAGE_GREEN = colors.HexColor('#a6b89c')
    FOREST_GREEN = colors.HexColor('#2e4a29')
    DEEP_CHARCOAL = colors.HexColor('#1c241b')
    OFF_WHITE = colors.HexColor('#f8faf7')
    LIGHT_GREY = colors.HexColor('#e8eae7')
    CODE_BG = colors.HexColor('#f3f5f2')
    BORDER_COLOR = colors.HexColor('#d5dad4')
    
    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=FOREST_GREEN,
        alignment=TA_LEFT
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=SAGE_GREEN,
        alignment=TA_LEFT
    )
    
    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=FOREST_GREEN,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=DEEP_CHARCOAL,
        spaceAfter=8
    )
    
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    code_style = ParagraphStyle(
        'CodeText',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#091208')
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    story = []
    
    # ----------------------------------------------------
    # HEADER SECTION
    # ----------------------------------------------------
    # Add a thin colored top bar
    header_table = Table([['']], colWidths=[504], rowHeights=[4])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), FOREST_GREEN),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 15))
    
    # Document Title and Metadata
    story.append(Paragraph("THE DAILY DRIP", subtitle_style))
    story.append(Paragraph("Collaborator Onboarding & Setup Guide", title_style))
    story.append(Spacer(1, 4))
    
    # Thin divider line
    div_table = Table([['']], colWidths=[504], rowHeights=[1])
    div_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BORDER_COLOR),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(div_table)
    story.append(Spacer(1, 15))
    
    # Welcome intro
    intro_text = (
        "Welcome to <b>The Daily Drip</b> streetwear catalog project. This workspace consists of two integrated "
        "components: a highly aesthetic, clean, earth-tone minimal React storefront, and a Python CLI Automation "
        "Suite designed to manage product syncs via Printify and schedule campaigns via Meta Ads. "
        "Use this guide to grant your developer, <b>Alby</b>, full access to collaborate, run the server, and sync mockups."
    )
    story.append(Paragraph(intro_text, body_style))
    story.append(Spacer(1, 10))
    
    # ----------------------------------------------------
    # STEP 1: NATHAN'S ACTIONS (GITHUB SETUP)
    # ----------------------------------------------------
    story.append(Paragraph("Step 1: Nathan Pushes the Code to GitHub", h1_style))
    story.append(Paragraph(
        "To allow Alby to collaborate, Nathan must first upload the local workspace directory to a private GitHub "
        "repository and invite Alby as a collaborator. Run these commands in your local machine terminal:",
        body_style
    ))
    
    step1_code = (
        "# 1. Initialize local git repository and commit current files<br/>"
        "git init<br/>"
        "git add .<br/>"
        "git commit -m \"feat: initial storefront release with sage earth-tone layout\"<br/>"
        "<br/>"
        "# 2. Link your local project to your newly created GitHub repository<br/>"
        "git remote add origin https://github.com/nathandcook10/daily-drip.git<br/>"
        "git branch -M main<br/>"
        "git push -u origin main"
    )
    
    # Embed Code Block in a Table for standard styling (width = 504)
    code_table_1 = Table([[Paragraph(step1_code, code_style)]], colWidths=[504])
    code_table_1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(code_table_1)
    
    note_text = (
        "<b>Important Note:</b> Go to repository <b>Settings</b> &rarr; <b>Collaborators</b> on github.com, click "
        "<b>Add People</b>, enter Alby's GitHub username or email, and invite him to the repository."
    )
    story.append(Spacer(1, 8))
    story.append(Paragraph(note_text, bullet_style))
    story.append(Spacer(1, 15))
    
    # ----------------------------------------------------
    # STEP 2: ALBY'S ACTIONS (CLONE & RUN STOREFRONT)
    # ----------------------------------------------------
    story.append(Paragraph("Step 2: Alby Clones & Launches the Storefront", h1_style))
    story.append(Paragraph(
        "Once invited to the private repository, Alby should open his terminal and run the following commands "
        "to install dependencies and boot up the high-aesthetic storefront locally:",
        body_style
    ))
    
    step2_code = (
        "# 1. Clone the repository and navigate into the project directory<br/>"
        "git clone https://github.com/nathandcook10/daily-drip.git<br/>"
        "cd daily-drip<br/>"
        "<br/>"
        "# 2. Install dependencies (React, Vite, Lucide-React, Framer Motion)<br/>"
        "npm install<br/>"
        "<br/>"
        "# 3. Start the local hot-reloading development server<br/>"
        "npm run dev"
    )
    
    code_table_2 = Table([[Paragraph(step2_code, code_style)]], colWidths=[504])
    code_table_2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(code_table_2)
    story.append(Spacer(1, 8))
    
    launch_note = "<b>Local Access:</b> The dev server will launch at: <font color='#2e4a29'><b>http://localhost:5173</b></font>. Alby can view, navigate, and edit storefront code in real-time."
    story.append(Paragraph(launch_note, bullet_style))
    
    # Page Break for a clean multi-page document layout
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 2: STEP 3 & COMPONENT SETUP
    # ----------------------------------------------------
    story.append(header_table)
    story.append(Spacer(1, 15))
    story.append(Paragraph("THE DAILY DRIP", subtitle_style))
    story.append(Paragraph("Collaborator Onboarding & Setup Guide (Cont.)", title_style))
    story.append(Spacer(1, 4))
    story.append(div_table)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Step 3: Alby Manages Visual Designs & Drops", h1_style))
    story.append(Paragraph(
        "Alby can expand the storefront, load active t-shirt drops, and run automated scripts easily:",
        body_style
    ))
    
    story.append(Paragraph(
        "&bull; <b>Visual Mockups:</b> Drop custom design flat-lays or artwork PNGs into <code>public/assets/</code> inside the codebase. These will be referenced in the catalog.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Product Catalog updates:</b> Open <code>src/components/ProductList.jsx</code> and edit/add product catalog entries to live-update the pricing, mockups, and descriptions.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Automated Drops:</b> To run the Printify and Meta program automated suite, add credentials to <code>scripts/.env</code> and execute the manager:",
        bullet_style
    ))
    story.append(Spacer(1, 5))
    
    step3_code = (
        "# Run the automated CLI to create a product on Printify & publish Meta Ads<br/>"
        "python3 scripts/daily_drip_manager.py --image \"design.png\" --title \"Sage Streetwear\" --price 29.99"
    )
    
    code_table_3 = Table([[Paragraph(step3_code, code_style)]], colWidths=[504])
    code_table_3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(code_table_3)
    story.append(Spacer(1, 15))
    
    # ----------------------------------------------------
    # DEVELOPMENT CHEAT SHEET
    # ----------------------------------------------------
    story.append(Paragraph("Quick Command Cheat Sheet", h1_style))
    
    commands_data = [
        [Paragraph("<b>Command</b>", body_bold), Paragraph("<b>Description</b>", body_bold)],
        [Paragraph("<code>npm run dev</code>", body_style), Paragraph("Starts the React development server locally at <code>localhost:5173</code>.", body_style)],
        [Paragraph("<code>npm run build</code>", body_style), Paragraph("Compiles high-performance static HTML/JS/CSS assets to <code>/dist</code>.", body_style)],
        [Paragraph("<code>python3 scripts/daily_drip_manager.py test</code>", body_style), Paragraph("Runs a connection health check against Meta Ads and Printify API services.", body_style)]
    ]
    
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_GREY),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ])
    
    commands_table = Table(commands_data, colWidths=[180, 324])
    commands_table.setStyle(table_style)
    story.append(commands_table)
    story.append(Spacer(1, 15))
    
    # ----------------------------------------------------
    # ENVIRONMENT CONFIGURATION
    # ----------------------------------------------------
    story.append(Paragraph("Environment Setup (.env)", h1_style))
    story.append(Paragraph(
        "Copy <code>scripts/.env.example</code> to <code>scripts/.env</code> and populate it to initialize external services:",
        body_style
    ))
    
    env_content = (
        "# PRINTIFY CREDS<br/>"
        "PRINTIFY_API_KEY=your_printify_personal_access_token<br/>"
        "PRINTIFY_SHOP_ID=your_printify_shop_id<br/>"
        "<br/>"
        "# META ADS CREDS<br/>"
        "META_ACCESS_TOKEN=your_meta_system_user_access_token<br/>"
        "META_AD_ACCOUNT_ID=act_your_ad_account_id<br/>"
        "META_PAGE_ID=your_facebook_page_id"
    )
    
    code_table_4 = Table([[Paragraph(env_content, code_style)]], colWidths=[504])
    code_table_4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(code_table_4)
    story.append(Spacer(1, 15))
    
    # Footer Note
    footer_text = "<i>The Daily Drip is styled using HSL-based organic light palettes matching the Shopify storefront design. For help or adjustments, review the README.md in the root workspace.</i>"
    story.append(Paragraph(footer_text, ParagraphStyle('FooterNote', parent=body_style, fontSize=8.5, textColor=colors.HexColor('#666666'))))
    
    doc.build(story)
    print(f"PDF Successfully written to {output_path}")

if __name__ == "__main__":
    output_pdf = "/Users/nathan/Daily Drip/Alby_Onboarding_Guide.pdf"
    create_onboarding_pdf(output_pdf)
