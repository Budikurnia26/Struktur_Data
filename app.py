import streamlit as st

st.set_page_config(page_title="Struktur Data - Linked List", layout="wide")

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Playlist:
    def __init__(self):
        self.head = None
        self.size = 0

    def tambah_lagu(self, lagu, posisi="akhir"):
        node_baru = Node(lagu)
        self.size += 1
        if self.head is None:
            self.head = node_baru
            return
        if posisi == "awal":
            node_baru.next = self.head
            self.head = node_baru
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node_baru

    def hapus_lagu(self, lagu):
        if self.head is None:
            return False
        if self.head.data == lagu:
            self.head = self.head.next
            self.size -= 1
            return True
        current = self.head
        while current.next:
            if current.next.data == lagu:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False

    def tampilkan(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

class BrowserHistory:
    def __init__(self, halaman_awal="Beranda"):
        self.current = Node(halaman_awal)
        self.back_stack = []
        self.forward_stack = []

    def kunjungi(self, url):
        self.back_stack.append(self.current.data)
        self.forward_stack.clear()
        self.current = Node(url)

    def back(self):
        if not self.back_stack:
            return False
        self.forward_stack.append(self.current.data)
        self.current = Node(self.back_stack.pop())
        return True

    def forward(self):
        if not self.forward_stack:
            return False
        self.back_stack.append(self.current.data)
        self.current = Node(self.forward_stack.pop())
        return True

if "playlist" not in st.session_state:
    st.session_state.playlist = Playlist()
    for lagu in ["Shape of You - Ed Sheeran", "Blinding Lights - The Weeknd", "Stay - Justin Bieber"]:
        st.session_state.playlist.tambah_lagu(lagu)

if "browser" not in st.session_state:
    st.session_state.browser = BrowserHistory("https://google.com")

if "notif" not in st.session_state:
    st.session_state.notif = {"playlist": None, "browser": None}

st.markdown("# 📚 Struktur Data – Linked List")
st.markdown("Studi Kasus: Playlist Musik Digital & Browser History")

tab1, tab2 = st.tabs(["🎵 Playlist Musik", "🌐 Browser History"])

with tab1:
    col_kiri, col_kanan = st.columns([1.2, 1])
    with col_kiri:
        st.subheader("➕ Tambah Lagu")
        nama_lagu = st.text_input("Nama lagu & artis", placeholder="Judul – Artis", key="input_lagu")
        posisi = st.radio("Tambahkan di:", ["Akhir playlist", "Awal playlist"], horizontal=True)
        if st.button("➕ Tambah Lagu", use_container_width=True):
            if nama_lagu.strip():
                pos = "akhir" if posisi == "Akhir playlist" else "awal"
                st.session_state.playlist.tambah_lagu(nama_lagu.strip(), pos)
                st.success(f'"{nama_lagu}" ditambahkan ke {pos} playlist.')
            else:
                st.error("Nama lagu tidak boleh kosong.")

        st.subheader("🗑️ Hapus Lagu")
        daftar_lagu = st.session_state.playlist.tampilkan()
        if daftar_lagu:
            pilih_hapus = st.selectbox("Pilih lagu:", daftar_lagu)
            if st.button("🗑️ Hapus", use_container_width=True):
                st.session_state.playlist.hapus_lagu(pilih_hapus)
                st.success(f'"{pilih_hapus}" dihapus.')
                st.rerun()
        else:
            st.info("Playlist kosong.")

    with col_kanan:
        st.subheader("🎶 Playlist Saat Ini")
        lagu_list = st.session_state.playlist.tampilkan()
        if lagu_list:
            for i, lagu in enumerate(lagu_list, 1):
                panah = "→" if i < len(lagu_list) else "→ NULL"
                st.markdown(f"**{i}.** {lagu} `{panah}`")
            st.caption(f"Total: {st.session_state.playlist.size} lagu")
        else:
            st.info("Belum ada lagu.")

with tab2:
    col_kiri2, col_kanan2 = st.columns([1.2, 1])
    with col_kiri2:
        st.subheader("🧭 Navigasi Browser")
        browser = st.session_state.browser
        c1, c2 = st.columns(2)
        with c1:
            if st.button("◀ Back", use_container_width=True, disabled=not browser.back_stack):
                browser.back()
                st.rerun()
        with c2:
            if st.button("Forward ▶", use_container_width=True, disabled=not browser.forward_stack):
                browser.forward()
                st.rerun()

        st.info(f"🌐 {browser.current.data}")

        url_baru = st.text_input("Kunjungi URL:", placeholder="https://contoh.com")
        if st.button("🔍 Kunjungi", use_container_width=True):
            url = url_baru.strip()
            if url:
                if not url.startswith("http"):
                    url = "https://" + url
                browser.kunjungi(url)
                st.rerun()
            else:
                st.error("URL tidak boleh kosong.")

    with col_kanan2:
        st.subheader("📋 Riwayat Kunjungan")
        browser = st.session_state.browser
        if browser.forward_stack:
            st.caption("🔵 Bisa Forward:")
            for url in reversed(browser.forward_stack):
                st.markdown(f"⬆ `{url}`")
        st.markdown(f"▶ **{browser.current.data}** ← Aktif")
        if browser.back_stack:
            st.caption("🔴 Bisa Back:")
            for url in reversed(browser.back_stack):
                st.markdown(f"⬇ `{url}`")