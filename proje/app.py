from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli-anahtar-buraya'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///okul_sosyal.db'
db = SQLAlchemy(app)

# Beğeni tablosu (many-to-many ilişki)
begeni = db.Table('begeni',
    db.Column('kullanici_id', db.Integer, db.ForeignKey('kullanici.id')),
    db.Column('gonderi_id', db.Integer, db.ForeignKey('gonderi.id'))
)

class Kullanici(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kullanici_adi = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    parola_hash = db.Column(db.String(120), nullable=False)
    mesajlar = db.relationship('Mesaj', backref='yazar', lazy=True)
    gonderiler = db.relationship('Gonderi', backref='yazar', lazy=True)
    begenilen_gonderiler = db.relationship('Gonderi', secondary=begeni, backref=db.backref('begenenler', lazy='dynamic'))

class Mesaj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icerik = db.Column(db.Text, nullable=False)
    tarih = db.Column(db.DateTime, nullable=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('kullanici.id'), nullable=False)

class Gonderi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(100), nullable=False)
    icerik = db.Column(db.Text, nullable=False)
    tarih = db.Column(db.DateTime, nullable=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('kullanici.id'), nullable=False)

@app.route('/')
def ana_sayfa():
    if 'kullanici_id' not in session:
        return redirect(url_for('giris'))
    gonderiler = Gonderi.query.order_by(Gonderi.tarih.desc()).all()
    return render_template('ana_sayfa.html', gonderiler=gonderiler)

@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
    if request.method == 'POST':
        kullanici_adi = request.form.get('kullanici_adi')
        email = request.form.get('email')
        parola = request.form.get('parola')

        kullanici = Kullanici(
            kullanici_adi=kullanici_adi,
            email=email,
            parola_hash=generate_password_hash(parola)
        )

        db.session.add(kullanici)
        db.session.commit()
        flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.')
        return redirect(url_for('giris'))

    return render_template('kayit.html')

@app.route('/giris', methods=['GET', 'POST'])
def giris():
    if request.method == 'POST':
        kullanici_adi = request.form.get('kullanici_adi')
        parola = request.form.get('parola')

        kullanici = Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first()

        if kullanici and check_password_hash(kullanici.parola_hash, parola):
            session['kullanici_id'] = kullanici.id
            return redirect(url_for('ana_sayfa'))

        flash('Kullanıcı adı veya parola hatalı!')

    return render_template('giris.html')

@app.route('/cikis')
def cikis():
    session.pop('kullanici_id', None)
    return redirect(url_for('giris'))

@app.route('/yeni-gonderi', methods=['POST'])
def yeni_gonderi():
    if 'kullanici_id' not in session:
        return redirect(url_for('giris'))

    baslik = request.form.get('baslik')
    icerik = request.form.get('icerik')

    if not baslik or not icerik:
        flash('Başlık ve içerik alanları zorunludur!')
        return redirect(url_for('ana_sayfa'))

    yeni_gonderi = Gonderi(
        baslik=baslik,
        icerik=icerik,
        tarih=datetime.now(),
        kullanici_id=session['kullanici_id']
    )

    db.session.add(yeni_gonderi)
    db.session.commit()

    flash('Gönderi başarıyla oluşturuldu!')
    return redirect(url_for('ana_sayfa'))

@app.route('/gonderi-sil/<int:gonderi_id>', methods=['POST'])
def gonderi_sil(gonderi_id):
    if 'kullanici_id' not in session:
        return jsonify({'success': False, 'error': 'Giriş yapmalısınız'})

    gonderi = Gonderi.query.get_or_404(gonderi_id)

    if gonderi.kullanici_id != session['kullanici_id']:
        return jsonify({'success': False, 'error': 'Bu gönderiyi silme yetkiniz yok'})

    db.session.delete(gonderi)
    db.session.commit()

    return jsonify({'success': True})

@app.route('/gonderi-begen/<int:gonderi_id>', methods=['POST'])
def gonderi_begen(gonderi_id):
    if 'kullanici_id' not in session:
        return jsonify({'success': False, 'error': 'Giriş yapmalısınız'})

    kullanici = Kullanici.query.get(session['kullanici_id'])
    gonderi = Gonderi.query.get_or_404(gonderi_id)

    if gonderi in kullanici.begenilen_gonderiler:
        kullanici.begenilen_gonderiler.remove(gonderi)
        begeni_durumu = False
    else:
        kullanici.begenilen_gonderiler.append(gonderi)
        begeni_durumu = True

    db.session.commit()

    return jsonify({
        'success': True, 
        'begeni_durumu': begeni_durumu,
        'begeni_sayisi': gonderi.begenenler.count()
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
