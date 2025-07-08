import json
import os

def create_cik_ticker_map(cik_list_path):
    cik_to_ticker = {}
    
    with open(cik_list_path, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
    
    for item in data_list:
        try:
            cik_code, ticker = item.split(',')
            
            cik_to_ticker[cik_code.strip()] = ticker.strip()
        except ValueError:
            print(f"Peringatan: Melewatkan baris dengan format tidak valid: '{item}'")
            
    return cik_to_ticker

def process_json_files(json_folder, output_folder, cik_to_ticker):

    os.makedirs(output_folder, exist_ok=True)

    all_files = os.listdir(json_folder)
    print(f"Jumlah file JSON yang ditemukan: {len(all_files)}")

    if not all_files:
        print(f"Peringatan: Folder '{json_folder}' kosong atau tidak ada file JSON yang ditemukan.")
        return
    
    print(f"Memproses file dari: {json_folder}")
    
    if not os.listdir(json_folder):
        print(f"Peringatan: Folder '{json_folder}' kosong.")
        return
        
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(json_folder, filename)
            
            try:
                cik_code = filename.split('_')[0]
            except IndexError:
                print(f"Nama file tidak valid (tidak ada '_'): {filename}")
                continue

            ticker = cik_to_ticker.get(cik_code, f"CIK_{cik_code}_NOT_FOUND")
            
            new_filename_base = filename.replace(f"{cik_code}_", f"{ticker}_", 1).replace('.json', '.txt')
            output_path = os.path.join(output_folder, new_filename_base)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f_in:
                    data = json.load(f_in)
                    
                content = data.get('part_1_item_2', 'Konten untuk "part_1_item_2" tidak ditemukan.')
                
                with open(output_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(content)
                    
                print(f"Berhasil diekstrak: {filename} -> {new_filename_base}")
                
            except Exception as e:
                print(f"Terjadi kesalahan saat memproses {filename}: {e}")

CIK_LIST_FILE = 'cik_list.json'

JSON_SOURCE_FOLDER = '/Users/jezzen145/Downloads/10Q-Analyzer2/datasets/EXTRACTED_FILINGS/10-Q' 

# Folder untuk menyimpan hasil file .txt
TXT_OUTPUT_FOLDER = '/Users/jezzen145/Downloads/10Q-Analyzer2/datasets/EXTRACTED_FILLINGS_TXT'

try:
    cik_ticker_map = create_cik_ticker_map(CIK_LIST_FILE)
    
    process_json_files(JSON_SOURCE_FOLDER, TXT_OUTPUT_FOLDER, cik_ticker_map)
    
    print(f"\nProses selesai. File teks disimpan di folder: {TXT_OUTPUT_FOLDER}")
    
except FileNotFoundError:
    print(f"Error: Pastikan file '{CIK_LIST_FILE}' dan folder '{JSON_SOURCE_FOLDER}' ada di direktori yang benar.")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")