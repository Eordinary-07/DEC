# builder/assemble_all.py

import os
import re
from section_map import get_frontmatter_and_map
from section_prereq import get_prerequisites
from section_u1 import get_unit1
from section_u2 import get_unit2
from section_u3 import get_unit3
from section_u4 import get_unit4
from section_u5 import get_unit5
from section_exam_problems import get_exam_problems
from section_appendix import get_appendix

def assemble():
    parts = [
        get_frontmatter_and_map(),
        get_prerequisites(),
        get_unit1(),
        get_unit2(),
        get_unit3(),
        get_unit4(),
        get_unit5(),
        get_exam_problems(),
        get_appendix()
    ]
    
    full_text = "\n\n".join(parts)
    
    output_path = "/home/user/DEC/DEC_Complete_Notes.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    
    print(f"Successfully assembled master notes at: {output_path}")
    
    # Statistics
    words = len(full_text.split())
    lines = len(full_text.splitlines())
    print(f"Total Words: {words:,}")
    print(f"Total Lines: {lines:,}")
    print(f"Total Characters: {len(full_text):,}")
    
    # Check all images referenced exist on disk
    img_refs = re.findall(r'src=["\'](images/[^"\']+)["\']', full_text)
    print(f"\nTotal image references: {len(img_refs)}")
    missing = []
    seen = set()
    for ref in img_refs:
        path = os.path.join("/home/user/DEC", ref)
        if not os.path.exists(path):
            missing.append(ref)
        else:
            if ref not in seen:
                size_kb = os.path.getsize(path) / 1024
                print(f"  [OK] {ref} ({size_kb:.1f} KB)")
                seen.add(ref)
            
    if missing:
        print(f"\n[ERROR] Missing images: {missing}")
    else:
        print(f"\nAll {len(seen)} unique image references successfully verified on disk!")

if __name__ == '__main__':
    assemble()
