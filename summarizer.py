import google.generativeai as genai
from dotenv import load_dotenv
import os
import time


load_dotenv('.env')
gemini_api_key = os.getenv('GEMINI_API_KEY')

MODEL_NAME = "gemini-2.5-pro"

#(Folder Sumber, Folder Hasil)
DOCUMENT_TYPES = {
    "10-Q (MDA)": (
        'D:/10Q-Analyzer/datasets/EXTRACTED_FILLINGS_10Q(MDA)_TXT',  
        'D:/10Q-Analyzer/data-summary/SUMMARY_FILLINGS_10Q(MDA)_TXT'  
    ),
    "10-Q (RF)": (
        'D:/10Q-Analyzer/datasets/EXTRACTED_FILLINGS_10Q(RF)_TXT',   
        'D:/10Q-Analyzer/data-summary/SUMMARY_FILLINGS_10Q(RF)_TXT'    
    ),
    "8-K": (
        'D:/10Q-Analyzer/datasets/EXTRACTED_FILLINGS_8K_TXT',       
        'D:/10Q-Analyzer/data-summary/SUMMARY_FILLINGS_8k_TXT'        
    )
}

#Summarize 10Q MDA
def summarize_10Q_MDA(text_content):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""
        Anda adalah seorang analis keuangan. Diberikan file teks yang berisi bagian "Management’s Discussion and Analysis (MD&A)".
        Tolong ringkas poin-poin kunci dari laporan tersebut. Fokus pada metrik keuangan utama, kinerja setiap segmen bisnis, prospek perusahaan, tantangan yang dihadapi, perubahan operasional yang signifikan, dan strategi alokasi modal.

        Struktur ringkasan Anda harus sama persis dengan contoh di bawah ini.

        ---
        CONTOH
        ---
        Teks MD&A Contoh Perusahaan (ABC Corp): 
        (Teks laporan fiktif ABC Corp)

        Ringkasan MD&A Contoh Perusahaan (ABC Corp):
        * **Ringkasan Eksekutif:** ABC Corp melaporkan pertumbuhan pendapatan yang kuat didorong oleh segmen Teknologi, namun menghadapi tantangan di pasar internasional karena tekanan kurs mata uang asing.
        * **Kinerja Keuangan Utama:**
            * Pendapatan: $100 juta (naik 10% YoY).
            * Laba Bersih: $15 juta (naik 5% YoY).
            * Arus Kas dari Operasi: $20 juta.
        * **Kinerja per Segmen Bisnis:**
            * Segmen Teknologi: Pendapatan naik 20% berkat peluncuran produk baru.
            * Segmen Manufaktur: Pendapatan turun 5% akibat kendala rantai pasok.
        * **Prospek dan Tantangan:**
            * Prospek: Optimis dengan rencana ekspansi ke pasar baru pada semester kedua.
            * Tantangan: Persaingan yang semakin ketat dan kenaikan harga bahan baku.
        * **Inisiatif Strategis & Perubahan Operasional:**
            * Restrukturisasi: Melakukan program efisiensi yang diharapkan menghemat $5 juta per tahun.
            * Perubahan Segmen: Tidak ada perubahan signifikan.
        * **Alokasi Modal:**
            * Dividen: Membayar dividen sebesar $5 juta.
            * Pembelian Kembali Saham: Membeli kembali saham senilai $2 juta.
        ---
        SELESAI CONTOH
        ---

        Teks MD&A Agilent Technologies:
        {text_content}

        Ringkasan MD&A Agilent Technologies:
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"    -> ERROR saat memanggil API untuk 10-Q (MDA): {e}")
        return None

#Summarize 10Q RF
def summarize_10Q_RF(text_content):

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""
        Anda adalah seorang analis risiko profesional. Diberikan file teks yang berisi bagian "ITEM 1A. RISK FACTORS".
        Tugas Anda adalah membaca, mengkategorikan, dan meringkas semua risiko yang dijelaskan. Kelompokkan risiko yang serupa ke dalam kategori yang logis dan jelaskan setiap risiko secara singkat dalam format poin-poin.

        Gunakan struktur yang sama persis dengan contoh di bawah ini.

        ---
        CONTOH
        ---
        Teks Faktor Risiko Contoh Perusahaan (TechGlobal Inc.): 
        (Teks laporan fiktif TechGlobal Inc.)

        Ringkasan Faktor Risiko Utama dari Laporan 10-Q TechGlobal Inc.:
        * **Risiko Bisnis dan Strategis:**
            * **Kondisi Ekonomi:** Perlambatan ekonomi dapat mengurangi belanja pelanggan.
            * **Persaingan:** Persaingan ketat dari pemain baru dapat menekan margin keuntungan.
        * **Risiko Operasional:**
            * **Rantai Pasok:** Ketergantungan pada satu pemasok untuk komponen kunci dapat menyebabkan gangguan produksi.
            * **Keamanan Siber:** Pelanggaran sistem TI dapat mengakibatkan kehilangan data dan kerusakan reputasi.
        * **Risiko Regulasi, Hukum, dan Kepatuhan:**
            * **Privasi Data:** Undang-undang privasi baru memerlukan investasi signifikan dalam kepatuhan dan membawa risiko denda.
            * **Kekayaan Intelektual:** Ada risiko litigasi dari pihak ketiga yang mengklaim pelanggaran paten.
        * **Risiko Keuangan dan Pajak:**
            * **Utang:** Tingkat utang yang tinggi membatasi fleksibilitas dan memerlukan porsi arus kas yang signifikan untuk pembayaran bunga.
            * **Perubahan Pajak:** Perubahan peraturan pajak dapat meningkatkan beban pajak secara keseluruhan.
        ---
        SELESAI CONTOH
        ---

        Teks Faktor Risiko Agilent Technologies:
        {text_content}

        Ringkasan Faktor Risiko Utama dari Laporan 10-Q Agilent Technologies:
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"    -> ERROR saat memanggil API untuk 10-Q (RF): {e}")
        return None

#Summarize 8K
def summarize_8K(text_content):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""
        Tujuan Anda adalah meringkas peristiwa paling penting dari laporan 8-K untuk investor.
        Fokus pada informasi material seperti perubahan manajemen, akuisisi, atau perjanjian penting.

        Sebutkan:
        - Apa peristiwa utamanya?
        - Siapa pihak yang terlibat?
        - Kapan peristiwa itu terjadi?
        - Apa dampak finansial atau syarat utamanya (contoh: nilai kesepakatan, biaya, atau rincian kompensasi)?

        Sajikan ringkasan dalam 3-7 kalimat menggunakan bahasa Anda sendiri (abstraktif). Hindari detail yang tidak penting.

        ---
        CONTOH
        ---
        Teks Laporan 8-K Fiktif:
        (Teks laporan fiktif mengenai akuisisi)

        Ringkasan Laporan 8-K Fiktif:
        Pada 1 Juli 2025, Global Tech menyelesaikan akuisisinya terhadap Innovate Solutions. Akuisisi ini merupakan transaksi tunai senilai sekitar $500 juta. Langkah strategis ini diharapkan dapat memperluas pangsa pasar Global Tech di sektor perangkat lunak enterprise.
        ---
        SELESAI CONTOH
        ---

        Teks Laporan 8-K Agilent Technologies:
        {text_content}

        Ringkasan Laporan 8-K Agilent Technologies:
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"ERROR saat memanggil API untuk 8-K: {e}")
        return None

#Process Files
def process_files(doc_type, source_folder, output_folder, summary_function):

    print(f"\n Memulai Proses untuk Tipe Dokumen: {doc_type} ---")
    
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        all_files = [f for f in os.listdir(source_folder) if f.endswith('.txt')]
        print(f"Ditemukan {len(all_files)} file .txt di '{source_folder}'.")
    except FileNotFoundError:
        print(f"Error: Folder sumber tidak ditemukan di '{source_folder}'.")
        return

    for i, filename in enumerate(all_files):
        print(f"[{i+1}/{len(all_files)}] Memproses: {filename}")
        
        source_path = os.path.join(source_folder, filename)
        summary_path = os.path.join(output_folder, filename)
        
        if os.path.exists(summary_path):
            print("Ringkasan sudah ada, file dilewati.")
            continue
        
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                print("File kosong, dilewati.")
                continue
                
            print("Mengirim ke Gemini API...")
            summary = summary_function(content) 
            
            if summary:
                with open(summary_path, 'w', encoding='utf-8') as f:
                    f.write(summary)
                print(f" Ringkasan berhasil disimpan.")
            else:
                print(f" Gagal membuat ringkasan untuk {filename}.")

            time.sleep(1.5) 

        except Exception as e:
            print(f" Terjadi kesalahan: {e}")

def main():

    try:
        genai.configure(api_key=gemini_api_key)
        print("Konfigurasi Gemini API berhasil.")
    except Exception as e:
        print(f"Gagal mengonfigurasi API. Pastikan API Key Anda valid. Error: {e}")
        return
        
    function_map = {
        "10-Q-MDA": summarize_10Q_MDA,
        "10-Q-RF": summarize_10Q_RF,
        "8-K": summarize_8K
    }
    
    for doc_type, (source, output) in DOCUMENT_TYPES.items():
        summary_func = function_map.get(doc_type)
        if summary_func:
            process_files(doc_type, source, output, summary_func)
        else:
            print(f"Peringatan: Tidak ditemukan fungsi ringkasan untuk tipe '{doc_type}'.")

    print("\nSemua proses telah selesai!")

if __name__ == "__main__":
    main()