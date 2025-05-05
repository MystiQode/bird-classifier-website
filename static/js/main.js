document.addEventListener("DOMContentLoaded", function () {

    document.getElementById('uploadForm').addEventListener('submit', function (e) {
        e.preventDefault();

        const fileInput = document.getElementById('fileInput');
        const preview = document.getElementById('preview');
        const progressBar = document.getElementById('progressBar');
        const resultBox = document.getElementById('result');

        if (!fileInput.files.length) {
            alert('Пожалуйста, выберите изображение.');
            return;
        }

        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = function (event) {
            preview.src = event.target.result;
            preview.style.display = 'block';
            progressBar.style.width = '0%';


            resultBox.innerHTML = '';

            let width = 0;
            const interval = setInterval(() => {
                if (width >= 100) {
                    clearInterval(interval);


                    const formData = new FormData(document.getElementById('uploadForm'));

                    fetch('/predict', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => {
                        if (!response.ok) throw new Error('Ошибка сети');
                        return response.json();
                    })
                    .then(data => {
                        resultBox.innerHTML = `
                            <p>Птица: <strong>${data.result}</strong></p>
                            <p>Описание: ${data.description || 'Информация отсутствует'}</p>
                        `;
                    })
                    .catch(error => {
                        console.error('Ошибка:', error);
                        resultBox.innerHTML = `<p class="error">Ошибка: ${error.message}</p>`;
                    });
                } else {
                    width += 10;
                    progressBar.style.width = width + '%';
                }
            }, 200);
        };

        reader.readAsDataURL(file);
    });


    document.querySelectorAll('.example-img').forEach(img => {
        img.addEventListener('click', function (e) {
            try {

                const description = this.getAttribute('data-description');


                const src = this.src;
                const filename = src.substring(src.lastIndexOf('/') + 1);


                const preview = document.getElementById('preview');
                const resultBox = document.getElementById('result');
                const birdName = filename.split('.')[0].replace(/_/g, ' ').toUpperCase();

                preview.src = src;
                preview.style.display = 'block';

                resultBox.innerHTML = `
                    <p>Выбрано изображение: <strong>${birdName}</strong></p>
                    <p>Описание: ${description}</p>
                `;


                const modal = document.getElementById("modal");
                const modalImg = document.getElementById("modalImg");
                modal.style.display = "block";
                modalImg.src = src;

            } catch (error) {
                console.error("Ошибка при обработке клика на изображение:", error);
            }
        });
    });


    const modal = document.getElementById("modal");
    const modalImg = document.getElementById("modalImg");
    const closeModal = document.querySelector(".modal-close");

    closeModal.addEventListener('click', () => {
        modal.style.display = "none";
        modalImg.src = "";
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
            modalImg.src = "";
        }
    });
});