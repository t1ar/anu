# 🃏 ANU - Absolutely Not UNO
ANU - Absolutely Not UNO adalah sebuah implementasi digital dari permainan kartu klasik UNO yang dibangun menggunakan bahasa pemrograman Python dan library **Arcade**. Game ini menghadirkan pengalaman bermain yang interaktif dengan antarmuka grafis (GUI) 2D yang mulus, sistem *bot/CPU* yang cerdas untuk mode *single-player*, serta integrasi audio dinamis yang memberikan nuansa permainan layaknya game profesional. Project ini dikembangkan sebagai bentuk implementasi nyata dari konsep *Object-Oriented Programming* (OOP) dalam pengembangan perangkat lunak.

## Anggota Kelompok
* Nikolas Tiar Banjarnahor - [25051204056]
* Muhammad Nur Fajri - [25051204016]
* Talitha Zahra Anabela Putri - [25051204064]
* Habibi - [25051204058]

## Fitur Utama
* Play Card - Pemain dapat memainkan kartu di tangan sesuai warna dan angkanya.
* Draw Card - Pemain dapat mengambil kartu di deck jika kekurangan kartu.
* Switcheroo - Pemain dapat mengganti warna kartu di secara bebas.
* Skip - Pemain dapat melompati giliran pemain setelahnya
* Reverse - Pemain dapat memutar arah giliran permainan.
* +2 dan +4 - Pemain dapat memberikan 2 atau 4 kartu kepada pemain setelahnya.

## Cara Menjalankan Project
### Prasyarat
* Python 3.12+
* pip

### Langkah-Langkah Menjalankan
* Clone/Download repository ini.
* Buka Terminal/Command Prompt dan arahkan ke folder repository.
* Buat dan aktifkan Virtual Enviroment.
    ```
    python -m venv .venv
    # Linux/macOS
    source .venv/bin/activate
    # Windows (Command Prompt)
    .venv\Scripts\activate.bat
    # Windows (Powershell)
    .venv\Scripts\Activate.ps1
    ```
* Install library Arcade.
    ```bash
    pip install arcade
    ```
* Jalankan main.py
    ```
    python main.py
    ```
## Penjelasan Implementasi OOP
### 1. Encapsulation
Encapsulation diterapkan untuk membungkus data dan menyembunyikan detail internal suatu objek agar tidak dimodifikasi secara sembarangan dari luar.

Pada project ini, enkapsulasi terlihat sangat jelas pada class Player yang mengelola ```tangan``` (kartu) pemain.
``` python
class Player:
    def __init__(self, name: str, is_human: bool):
        self.name = name
        self.is_human = is_human
        self.hand = [] # Daftar kartu dienkapsulasi

    def remove_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
```
Tujuannya adalah agar sistem game utama ```(GameplayView)``` tidak menghapus atau mengubah isi list ```hand``` secara langsung. Jika ingin membuang kartu, sistem harus meminta izin dengan memanggil method ```remove_card()```.
### 2. Inheritence
Inheritance diterapkan ketika class turunan mewarisi atribut atau method dari class induk.

Contoh penerapan pada project ini terdapat pada bagian user interface (layar game). Class GameplayView, MainMenuView, dan SettingsView mewarisi class dasar arcade.View.
``` python
class GameplayView(arcade.View):
    def __init__(self):
        super().__init__()
        self._setup()
```
Selain itu, dengan melakukan pewarisan ini, class-class tampilan tersebut otomatis mendapatkan fungsionalitas rendering grafis dan pembacaan input (seperti klik mouse dan keyboard) bawaan dari engine Arcade tanpa perlu kita buat dari awal.
### 3. Abstraction 
Abstraction diterapkan dengan menyembunyikan kompleksitas logika sistem di balik sebuah fungsi (interface) yang sederhana, sehingga bagian program lain lebih mudah menggunakannya.

Contoh penerapan pada project ini adalah logika aturan permainan UNO yang disembunyikan di dalam class Card melalui method can_play_on().
``` python
class Card:
    def can_play_on(self, top_card) -> bool:
        if self.is_wild:
            return True
        if self.color == top_card.color or self.color == top_card.chosen_color:
            return True
        if self.value == top_card.value:
            return True
        return False
```
Sistem utama tidak perlu tahu rumus rumit untuk mengecek kecocokan warna, angka, atau kartu wild. Sistem cukup bertanya "Apakah kartu ini bisa dimainkan?" dengan memanggil method tersebut, dan class Card akan mengembalikan jawaban True atau False.
### 4. Polymorphism
Polymorphism diterapkan ketika satu method yang sama dipanggil oleh sistem, namun memberikan respons atau perilaku yang berbeda tergantung pada class-nya (Banyak bentuk, satu perintah).

Pada project ini, engine Arcade selalu memanggil perintah on_key_press(). Namun, class MainMenuView dan SettingsView merespons perintah yang sama tersebut dengan perilaku yang sama sekali berbeda.
``` python
class MainMenuView(arcade.View):
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            # Polymorphism: Merespons dengan memulai game
            game_view = GameplayView()
            self.window.show_view(game_view)


class SettingsView(arcade.View):
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # Polymorphism: Merespons dengan kembali ke layar sebelumnya
            self.window.show_view(self.previous_view)
```
Meski nama fungsinya persis sama, MainMenuView menggunakannya untuk transisi layar permainan, sedangkan SettingsView menggunakannya untuk fungsi tombol kembali (back).
## Screenshots
![Main Menu.](images/1.png)
![Gameplay.](images/2.png)
![Setting.](images/3.png)