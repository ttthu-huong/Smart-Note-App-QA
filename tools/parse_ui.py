import xml.etree.ElementTree as ET
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for node in root.iter('node'):
            text = node.get('text', '')
            desc = node.get('content-desc', '')
            bounds = node.get('bounds', '')
            cls = node.get('class', '')
            if text or desc:
                text_clean = text.replace('\n', ' ')
                desc_clean = desc.replace('\n', ' ')
                print(f"[{cls}] text='{text_clean}' | desc='{desc_clean}' | bounds={bounds}")
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    f = sys.argv[1] if len(sys.argv) > 1 else 'ui.xml'
    parse(f)
