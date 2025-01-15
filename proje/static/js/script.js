function gonderiSil(gonderiId) {
    if (!confirm('Bu gönderiyi silmek istediğinizden emin misiniz?')) {
        return;
    }

    fetch(`/gonderi-sil/${gonderiId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.querySelector(`.post[data-gonderi-id="${gonderiId}"]`).remove();
        } else {
            alert(data.error || 'Bir hata oluştu');
        }
    })
    .catch(error => {
        console.error('Hata:', error);
        alert('Bir hata oluştu');
    });
}

function gonderiLike(gonderiId) {
    fetch(`/gonderi-begen/${gonderiId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const likeBtn = document.querySelector(`.post[data-gonderi-id="${gonderiId}"] .like-btn`);
            const likeCount = likeBtn.querySelector('.like-count');
            
            if (data.begeni_durumu) {
                likeBtn.classList.add('liked');
            } else {
                likeBtn.classList.remove('liked');
            }
            
            likeCount.textContent = data.begeni_sayisi;
        } else {
            alert(data.error || 'Bir hata oluştu');
        }
    })
    .catch(error => {
        console.error('Hata:', error);
        alert('Bir hata oluştu');
    });
}