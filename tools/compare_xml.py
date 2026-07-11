import xml.etree.ElementTree as ET

port_path = r"D:\RHOS-Matrix-V2-3.0.3.0-plato-xz-by.RHProjects\images\super_extracted\product\etc\device_features\plato.xml"
stock_path = r"D:\plato_global_images_OS2.0.207.0.VLQMIXM_20250923.0000.00_15.0_global_62eb292827\plato_global_images_OS2.0.207.0.VLQMIXM_15.0\images\super_extracted\product\etc\device_features\plato.xml"

def load_xml_features(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        features = {}
        for elem in root:
            # Handle float/bool/integer/string elements
            name = elem.attrib.get('name')
            if name:
                features[name] = elem.text.strip() if elem.text else ''
        return features
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return {}

def main():
    port_feats = load_xml_features(port_path)
    stock_feats = load_xml_features(stock_path)
    
    print("=" * 60)
    print("  Comparing plato.xml: Port vs Stock features")
    print("=" * 60)
    print()

    # Find differences
    all_keys = set(port_feats.keys()) | set(stock_feats.keys())
    
    only_in_stock = []
    only_in_port = []
    different_value = []
    
    for k in sorted(all_keys):
        in_port = k in port_feats
        in_stock = k in stock_feats
        
        if in_stock and not in_port:
            only_in_stock.append(k)
        elif in_port and not in_stock:
            only_in_port.append(k)
        else:
            val_port = port_feats[k]
            val_stock = stock_feats[k]
            if val_port != val_stock:
                different_value.append((k, val_stock, val_port))
                
    print(f"Features present ONLY in Stock ({len(only_in_stock)} items):")
    for k in only_in_stock[:20]:
        print(f"  - {k} (Value: {stock_feats[k]})")
    if len(only_in_stock) > 20:
        print(f"  ... and {len(only_in_stock) - 20} more.")
        
    print()
    print(f"Features present ONLY in Port ({len(only_in_port)} items):")
    for k in only_in_port:
        print(f"  - {k} (Value: {port_feats[k]})")
        
    print()
    print(f"Features with DIFFERENT values ({len(different_value)} items):")
    for k, val_stock, val_port in different_value:
        print(f"  - {k:40s} | Stock: {val_stock:10s} | Port: {val_port:10s}")

if __name__ == "__main__":
    main()
