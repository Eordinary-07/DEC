import os, sys, pymupdf, re

doc_kumar = pymupdf.open('fundementals-of-digital-circuits-fourthnbsped-9788120352681.pdf')
doc_floyd = pymupdf.open('Digital Fundamentals A Systems Approach 1_E -- Thomas L_ Floyd -- 1_E, 2013 -- 540c3c483a52758ca159df438d2eecd8 -- Anna’s Archive.pdf')
doc_mano  = pymupdf.open('Digital Design Global Edition by M. Morris Mano, Michael Ciletti.pdf')

def find_true_caption_kumar(pno, fignum):
    p = doc_kumar[pno - 1]
    for b in p.get_text('blocks'):
        lines = b[4].strip().split('\n')
        if len(lines) > 0 and re.match(r'^Figure\s+' + re.escape(fignum) + r'(\s|$)', lines[0].strip()):
            if len(lines[0].strip()) < 25 and not lines[0].strip().endswith('.'):
                return b
            elif len(lines[0].strip()) < 40 and ('shows' not in lines[0] and 'illustrates' not in lines[0]):
                return b
    return None

def crop_and_save_kumar(pno, fignum, out_name, y_pad_top=15, y_pad_bot=10, x_pad=12):
    b = find_true_caption_kumar(pno, fignum)
    if not b:
        print(f"FAILED to find true caption for Figure {fignum} on page {pno}")
        return False
    p = doc_kumar[pno - 1]
    cap_rect = pymupdf.Rect(b[:4])
    drawings = p.get_drawings()
    rel_drawings = [d for d in drawings if d['rect'].y1 <= cap_rect.y1 + 10 and d['rect'].y0 >= cap_rect.y0 - 550]
    
    if rel_drawings:
        fig_rect = rel_drawings[0]['rect']
        for d in rel_drawings: fig_rect = fig_rect | d['rect']
        full_rect = fig_rect | cap_rect
    else:
        full_rect = cap_rect

    # diagram text labels
    for blk in p.get_text('blocks'):
        b_rect = pymupdf.Rect(blk[:4])
        if b_rect.y0 >= full_rect.y0 - 15 and b_rect.y1 <= full_rect.y1 + 10:
            if (b_rect.x1 - b_rect.x0) < 380:
                full_rect = full_rect | b_rect

    crop_rect = pymupdf.Rect(full_rect.x0 - x_pad, full_rect.y0 - y_pad_top, full_rect.x1 + x_pad, full_rect.y1 + y_pad_bot) & p.rect
    pix = p.get_pixmap(clip=crop_rect, dpi=200)
    out_path = os.path.join('images', out_name)
    pix.save(out_path)
    print(f"Fixed {fignum} -> images/{out_name} [{pix.width}x{pix.height}] (p. {pno})")
    return True

# Fix CMOS Inverter
crop_and_save_kumar(921, '16.23', 'fig_u1_cmos_inverter.png')
# Fix CMOS NAND
crop_and_save_kumar(922, '16.24', 'fig_u1_cmos_nand.png')
# Fix CMOS NOR
crop_and_save_kumar(923, '16.25', 'fig_u1_cmos_nor.png')
# Fix Sequential block diag
crop_and_save_kumar(578, '10.1', 'fig_u4_sequential_block_diag.png')
# Fix SIPO register
crop_and_save_kumar(641, '11.7', 'fig_u4_sipo_register.png')
# Fix Dual-slope ADC
crop_and_save_kumar(964, '17.23', 'fig_u5_dual_slope_adc.png')
# Fix SAR ADC
crop_and_save_kumar(965, '17.24', 'fig_u5_sar_adc.png', x_pad=20)
# Fix PLD configurations
crop_and_save_kumar(499, '8.7', 'fig_u5_pld_configurations.png')

