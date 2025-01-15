Türkçe:
Proje Adı: Okul Sosyal Platformu

Açıklama:
Okul Sosyal Platformu, öğrencilerin bir sosyal medya platformunda olduğu gibi gönderi paylaşmalarını, diğer gönderileri beğenmelerini ve mesajlaşmalarını sağlayan basit bir web uygulamasıdır. Flask ve SQLAlchemy kullanılarak geliştirilmiş olup, temel kullanıcı kimlik doğrulama, oturum yönetimi ve veri tabanı işlemleri içermektedir.

Özellikler:
Kullanıcı kayıt ve giriş sistemi.
Kullanıcıların gönderi oluşturması, beğenmesi ve silmesi.
Flask oturum yönetimi ile kişisel kullanıcı işlemleri.
Flask SQLAlchemy ile ilişkisel veritabanı yapısı:
Kullanıcılar ve gönderiler arasında bire çok ilişki.
Kullanıcılar ve beğeniler arasında çoktan çoğa ilişki.
Beğeni sayısını gerçek zamanlı olarak güncelleyen bir yapı.
Flash mesajlar ve AJAX tabanlı işlemlerle modern bir kullanıcı deneyimi.
Kurulum:
Projeyi klonlayın:
bash
Kodu kopyala
git clone <[REPO_URL](https://github.com/Megartlix/basitchatprogram-.git)>
cd okul-sosyal-platformu
Gerekli bağımlılıkları yükleyin:
bash
Kodu kopyala
pip install -r requirements.txt
Veritabanını oluşturun:
bash
Kodu kopyala
python -c "from app import db; db.create_all()"
Sunucuyu başlatın:
bash
Kodu kopyala
flask run
Tarayıcınızda http://127.0.0.1:5000 adresini ziyaret edin.

English:
Project Name: School Social Platform

Description:
The School Social Platform is a simple web application that allows students to share posts, like other posts, and communicate as they would on a social media platform. It is developed using Flask and SQLAlchemy, featuring basic user authentication, session management, and database operations.

Features:
User registration and login system.
Users can create, like, and delete posts.
Personalized user actions with Flask session management.
Relational database structure with Flask SQLAlchemy:
One-to-many relationship between users and posts.
Many-to-many relationship between users and likes.
Real-time like count updates.
Modern user experience with Flash messages and AJAX-based interactions.
Setup:
Clone the repository:
bash
Kodu kopyala
git clone <REPO_URL>
cd school-social-platform
Install dependencies:
bash
Kodu kopyala
pip install -r requirements.txt
Create the database:
bash
Kodu kopyala
python -c "from app import db; db.create_all()"
Start the server:
bash
Kodu kopyala
flask run
Visit http://127.0.0.1:5000 in your browser.
Future Enhancements:
Add comment and reply functionality.
Design a more modern user interface.
Implement user profile customization.
Introduce multi-language support.



