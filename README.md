# Bandung Food Quest (BFQ)

## Nama-Nama Anggota Kelompok:
- Muhammad Abyasa Pratama (2306207663)
- Raja Rafael Pangihutan Sitorus (2306244923)
- Daniel Ferdiansyah (2306275052)
- Safira Salma Humaira (2306245850)
- Evelyn Depthios (2306207543)

## Deskripsi Aplikasi:
Bandung Food Quest (BFQ) merupakan sebuah website e-commerce yang berfokus pada produk-produk kuliner khas Bandung. Website ini menyediakan platform bagi pelanggan untuk menemukan dan membeli produk makanan. Selain itu, admin dapat mengelola katalog produk secara langsung melalui fitur AJAX. Pelanggan dan admin dapat berpartisipasi dalam diskusi melalui forum komunitas, serta membaca atau menulis artikel terkait kuliner Bandung. Dengan tampilan yang responsif dan mudah digunakan, Bandung FQ bertujuan untuk memberikan pengalaman berbelanja dan berbagi informasi kuliner yang menyenangkan.

Kelompok kami memilih kota Bandung sebagai pilihan kota dikarenakan kota Bandung merupakan kota yang unggul dalam segi kulinernya. Kami ingin memajukan UMKM dengan potensi tinggi kuliner khas Bandung. Untuk itu dengan menerapkan modul-modul dalam website kami, kami ingin adanya penjualan dan interaksi antara customer dan admin.

## Daftar Modul yang Akan Diimplementasikan:
1. **Main App (Home Page)**
   - **Navbar**: Berisi menu Home, Categories (dropdown), Forum, Hello [nama user] (link ke edit user profile), dan Logout. Support mobile view.
   - **Header, Footer, Base Template**: Di folder root template, standar untuk seluruh halaman.
   - **Homepage as Admin**: Bisa menambahkan, mengedit, dan menghapus produk menggunakan AJAX.
   - **Homepage as Customer**: Menampilkan produk dalam pop-up detail menggunakan AJAX.
   - **Carousel**: Foto-foto Bandung dengan overview singkat.
   - **Product Display**: Admin dapat menambah, mengedit, dan menghapus produk. Customer hanya melihat detail produk.

2. **Categories**
   - **Kategori Produk**: Menambah field kategori ke dataset produk.
   - **Product Display by Category**: Menampilkan produk berdasarkan kategori dari navbar.

3. **Forum Diskusi**
   - **Forum**: Menampilkan postingan forum dari semua pengguna (nama dan umur ditampilkan).
   - **Tambah Topik**: Menggunakan AJAX untuk pop-up.
   - **Reply dan Edit Forum**: Edit dan hapus postingan atau reply sendiri.

4. **User Info & Authentication**
   - **Register**: Nama Lengkap, Umur, Gender, No. Telepon, Username, Password, Role.
   - **Login**: Username dan Password.
   - **User Profile**: Menampilkan profil user, edit profil menggunakan AJAX, dan ganti password.

5. **Blog/Artikel**
   - **Post Artikel**: Judul, Topik, Artikel, Penulis.
   - **Display Artikel**: Menampilkan artikel dalam bentuk preview kecil.
   - **My Article**: Lihat, edit, dan hapus artikel sendiri dengan AJAX.

## Sumber Initial Dataset:
[Initial Dataset](https://docs.google.com/spreadsheets/d/17DGOKHDmYB2t5OF1HMo6wjNFQnZkCA3M83gFQPy6X2A/edit?gid=0#gid=0)

## Role atau Peran Pengguna Beserta Deskripsinya:
1. **Admin**:
   - Mengelola produk (menambah, mengedit, menghapus) dan kategori produk.
   - Mengelola forum dan artikel (menghapus atau mengedit postingan yang tidak sesuai).
   - Memiliki akses penuh terhadap semua fitur pengelolaan dalam aplikasi.

2. **Customer**:
   - Dapat melihat produk dan kategori produk yang ditampilkan.
   - Dapat berpartisipasi dalam diskusi forum dengan membuat dan membalas topik.
   - Bisa membaca artikel kuliner serta menulis dan mengelola artikel pribadi mereka.

3. **Guest**:
   - Pengguna yang belum terdaftar hanya dapat melihat produk dan artikel, tetapi tidak dapat berinteraksi dengan forum atau menulis artikel.

## Tautan Deployment Aplikasi PWS:
[BFQ Deployment](http://daniel-ferdiansyah-bfq.pbp.cs.ui.ac.id/)
