import streamlit as st
from streamlit_option_menu import option_menu
import requests
from PIL import Image, ImageOps
from io import BytesIO
import os

# Direktori untuk menyimpan file yang diunggah
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Menyimpan data admin terdaftar
admins = {"explorewaymuli@gmail.com": "WayMuli123"}  # Admin yang terdaftar (username: password)

# Fungsi untuk memuat gambar
@st.cache_data
def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = ImageOps.exif_transpose(img)
    return img

# Fungsi untuk menampilkan gambar dan informasi
def display_images_with_data(data_list, image_urls):
    cols = st.columns(3)
    for i, (data, url) in enumerate(zip(data_list, image_urls)):
        with cols[i % 3]:
            # Menampilkan gambar dari URL base64 jika ada
            if data.get("image_url"):
                st.image(data["image_url"], use_column_width=True, caption=data["nama"])
            with st.expander(f"Detail {data['nama']}"):
                st.write(f"**Deskripsi:** {data['deskripsi']}")
                st.write(f"**Harga/Tiket:** {data['harga']}")
                st.write(f"**Kontak:** {data['kontak']}")
                # Menampilkan Link Google Maps jika ada
                if data.get("gmaps_link"):
                    st.write(f"**Lokasi di Google Maps:** [Klik untuk lihat]({data['gmaps_link']})")


import streamlit as st
import base64  # Import base64 dari pustaka standar
from PIL import Image
from io import BytesIO

# Fungsi untuk mengunggah file dan menampilkan pratinjau
def upload_new_content():
    st.markdown("## Tambahkan Informasi Baru")

    # Pilihan kategori: UMKM atau Wisata
    kategori = st.radio("Pilih Kategori", ("UMKM", "Tempat Wisata"), key="kategori_radio")

    # Unggah file gambar
    uploaded_file = st.file_uploader("Unggah Foto Baru", type=["jpg", "jpeg", "png"], key="file_uploader")
    if uploaded_file is not None:
        # Membaca gambar dari file yang diunggah
        img = Image.open(uploaded_file)

        # Menampilkan pratinjau gambar
        st.image(img, caption="Pratinjau Gambar", use_column_width=True)

        # Simpan gambar dalam memori dan tampilkan
        img_byte = BytesIO()
        img.save(img_byte, format="PNG")
        img_byte.seek(0)

        # Menggunakan base64 untuk encoding gambar
        file_url = f"data:image/png;base64,{base64.b64encode(img_byte.getvalue()).decode()}"
    else:
        file_url = None

    # Input detail informasi
    nama = st.text_input("Nama Tempat/Produk")
    deskripsi = st.text_area("Deskripsi")
    harga = st.text_input("Harga/Tiket")
    kontak = st.text_input("Kontak")

    # Input untuk link Google Maps
    gmaps_link = st.text_input("Link Lokasi di Google Maps")

    # Tambahkan data baru
    if st.button("Tambahkan"):
        if kategori == "UMKM":
            umkm_data = {
                "nama": nama,
                "deskripsi": deskripsi,
                "harga": harga,
                "kontak": kontak,
                "gmaps_link": gmaps_link,  # Menambahkan link Google Maps
                "image_url": file_url,     # Menambahkan URL gambar dalam format base64
            }
            st.session_state["umkm_data"].append(umkm_data)
            st.success(f"Data UMKM '{nama}' berhasil ditambahkan!")
        elif kategori == "Tempat Wisata":
            wisata_data = {
                "nama": nama,
                "deskripsi": deskripsi,
                "harga": harga,
                "kontak": kontak,
                "gmaps_link": gmaps_link,  # Menambahkan link Google Maps
                "image_url": file_url,     # Menambahkan URL gambar dalam format base64
            }
            st.session_state["wisata_data"].append(wisata_data)
            st.success(f"Data Tempat Wisata '{nama}' berhasil ditambahkan!")

        # Memicu refresh halaman
        st.session_state["rerun"] = True



# Fungsi login admin
def admin_login():
    st.markdown("## Login Admin")
    
    # Input username dan password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Validasi login
    if st.button("Login"):
        if username in admins and admins[username] == password:
            st.session_state.is_admin = True
            st.success("Login berhasil!")
            st.session_state["rerun"] = True  # Trigger halaman refresh setelah login
        else:
            st.error("Username atau password salah!")

# Inisialisasi data
if "umkm_data" not in st.session_state:
    st.session_state["umkm_data"] = []

if "wisata_data" not in st.session_state:
    st.session_state["wisata_data"] = []

# Jika admin sudah login
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# Header Halaman
st.markdown(
    """
    <div style='display: flex; justify-content: space-between; align-items: center; background-color: #FFA500; padding: 20px; border-radius: 10px;'>
        <div>
            <h1 style='font-size: 3.5em; color: white; font-weight: bold;'>EXPLORE DESA WAY MULI</h1>
            <p style='font-size: 1.5em; color: white;'>Jelajahi Keindahan Wisata & Dukungan untuk Produk Lokal</p>
            <p style='font-size: 1.2em; color: #f0f0f0;'>Destinasi sempurna untuk menikmati alam, budaya, dan cita rasa khas desa</p>
        </div>
        <div>
            <img src="https://drive.google.com/uc?export=view&id=1JLOQBwAgx0fmi3W1OyTIKU4zdw5NzFpw" alt="Logo" style="height: 100px; border-radius: 50%;">
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Menu Navigasi
def streamlit_menu():
    selected = option_menu(
        menu_title=None,
        options=["Home", "UMKM", "Tempat Wisata", "Contact Us", "Tambah Konten"],
        icons=["house-door", "shop", "map", "envelope", "plus-circle"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#144259"},
            "icon": {"color": "#ffa500", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "color": "#fff",
                "--hover-color": "#ffa500",
                "border-radius": "5px",
            },
            "nav-link-selected": {"background-color": "#ffa500"},
        },
    )
    return selected

menu = streamlit_menu()

# Menampilkan halaman sesuai menu
if menu == "Home":
    st.markdown("<h1 style='text-align: center; color: #144259;'>Tentang Kami</h1>", unsafe_allow_html=True)
    st.markdown(
        """<div style="text-align: justify; font-size: 1.2em; line-height: 1.8;">
        Desa Way Muli adalah pusat keindahan alam dan budaya di Lampung. Kami menawarkan 
        <b>pesona wisata alam</b> seperti pantai dan pegunungan, serta produk-produk lokal unggulan dari UMKM.
        Mari jelajahi keunikan Way Muli dan dukung pengembangan ekonomi lokal kami untuk masa depan yang lebih baik!
        </div>""",
        unsafe_allow_html=True,
    )

elif menu == "UMKM":
    st.markdown("<h1 style='text-align: center; color: #144259;'>Produk Lokal UMKM</h1>", unsafe_allow_html=True)
    data_list = st.session_state["umkm_data"]
    display_images_with_data(data_list, data_list)  # Menggunakan data_list untuk gambar

elif menu == "Tempat Wisata":
    st.markdown("<h1 style='text-align: center; color: #144259;'>Tempat Wisata</h1>", unsafe_allow_html=True)
    data_list = st.session_state["wisata_data"]
    display_images_with_data(data_list, data_list)  # Menggunakan data_list untuk gambar

elif menu == "Tambah Konten":
    if st.session_state.is_admin:
        upload_new_content()
    else:
        admin_login()

elif menu == "Contact Us":
    st.markdown("<h1 style='text-align: center; color: #144259;'>Hubungi Kami</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style="font-size: 1.2em; line-height: 1.8;">
        Untuk informasi lebih lanjut atau pertanyaan, silakan hubungi kami melalui:
        </p>
        <ul>
            <li><b>Email:</b> info@waymuli.com</li>
            <li><b>Telepon:</b> +62 812 3456 7890</li>
            <li><b>Alamat:</b> Jl. Way Muli No. 123, Lampung</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )
