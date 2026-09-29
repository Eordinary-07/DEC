import os, sys, pymupdf, re

os.makedirs('images', exist_ok=True)

doc_kumar = pymupdf.open('fundementals-of-digital-circuits-fourthnbsped-9788120352681.pdf')
doc_floyd = pymupdf.open('Digital Fundamentals A Systems Approach 1_E -- Thomas L_ Floyd -- 1_E, 2013 -- 540c3c483a52758ca159df438d2eecd8 -- Anna’s Archive.pdf')
doc_mano  = pymupdf.open('Digital Design Global Edition by M. Morris Mano, Michael Ciletti.pdf')

figures_manifest = []

def extract_kumar_fig(pdf_page, fig_id, out_name, y_offset_top=15, y_offset_bottom=10, x_pad=12):
    p = doc_kumar[pdf_page - 1]
    blocks = p.get_text('blocks')
    cap_block = None
    for b in blocks:
        lines = b[4].strip().split('\n')
        if lines and lines[0].strip().startswith(fig_id):
            cap_block = b
            break
    
    if not cap_block:
        print(f"FAILED to find caption for {fig_id} on page {pdf_page}")
        return False

    cap_rect = pymupdf.Rect(cap_block[:4])
    drawings = p.get_drawings()
    
    # Check if caption is at the bottom or top of the figure
    # In Kumar, captions are almost always below the figure
    rel_drawings = [d for d in drawings if d['rect'].y1 <= cap_rect.y1 + 10 and d['rect'].y0 >= cap_rect.y0 - 550]
    
    if rel_drawings:
        fig_rect = rel_drawings[0]['rect']
        for d in rel_drawings:
            fig_rect = fig_rect | d['rect']
        full_rect = fig_rect | cap_rect
    else:
        full_rect = cap_rect

    # Expand horizontally to include diagram labels
    # diagram text blocks inside the vertical span
    for b in blocks:
        b_rect = pymupdf.Rect(b[:4])
        if b_rect.y0 >= full_rect.y0 - 10 and b_rect.y1 <= full_rect.y1 + 5:
            if (b_rect.x1 - b_rect.x0) < 380: # not a full-width paragraph
                full_rect = full_rect | b_rect

    # Add margins
    crop_rect = pymupdf.Rect(full_rect.x0 - x_pad, full_rect.y0 - y_offset_top, full_rect.x1 + x_pad, full_rect.y1 + y_offset_bottom)
    crop_rect = crop_rect & p.rect

    pix = p.get_pixmap(clip=crop_rect, dpi=200)
    out_path = os.path.join('images', out_name)
    pix.save(out_path)
    
    cap_text = cap_block[4].strip().replace('\n', ' ')
    printed_page = pdf_page - 32 # Anand Kumar front matter offset
    figures_manifest.append({
        'id': fig_id,
        'filename': out_name,
        'book': 'A. Anand Kumar, Fundamentals of Digital Circuits (4th Ed.)',
        'pdf_page': pdf_page,
        'printed_page': printed_page,
        'caption': cap_text,
        'rect': [crop_rect.x0, crop_rect.y0, crop_rect.x1, crop_rect.y1]
    })
    print(f"Extracted {fig_id} -> {out_name} (p. {pdf_page}, printed {printed_page}): {cap_text[:60]}")
    return True

print("Extract function defined.")
