import re

paths = [
    r'D:\plato_global_images_OS2.0.207.0.VLQMIXM_20250923.0000.00_15.0_global_62eb292827\plato_global_images_OS2.0.207.0.VLQMIXM_15.0\images\super_extracted\product\etc\permissions\privapp-permissions-miui-product.xml',
    r'D:\plato_global_images_OS2.0.207.0.VLQMIXM_20250923.0000.00_15.0_global_62eb292827\plato_global_images_OS2.0.207.0.VLQMIXM_15.0\images\super_extracted\product\etc\permissions\privapp-permissions-product.xml'
]

for p in paths:
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if 'extraphoto' in content or 'ExtraPhoto' in content:
            print(f'Found in: {p}')
            # Look for privapp-permissions package block
            # Package might be com.miui.extraphoto or similar
            blocks = re.findall(r'<privapp-permissions package="[^"]+">(?:(?!</privapp-permissions>).)*?extraphoto.*?</privapp-permissions>', content, re.DOTALL | re.IGNORECASE)
            for b in blocks:
                print(b)
            # General block matching package
            for m in re.finditer(r'<privapp-permissions package="([^"]+)">', content):
                pkg = m.group(1)
                if 'extraphoto' in pkg or 'photo' in pkg:
                    # extract block
                    start = m.start()
                    end = content.find('</privapp-permissions>', start)
                    print(content[start:end+len('</privapp-permissions>')])
    except Exception as e:
        print(f"Error {p}: {e}")
