// script.js
const imageContainer = document.getElementById('image-container');

fetch('http://127.0.0.1:8000/api/images/')
    .then(response => response.json())
    .then(data => {
        data.forEach(image => {
            // 이미지 요소 생성
            const imgElement = document.createElement('img');
            imgElement.src = image.image;  // 이미지 URL 설정
          

            // 이미지 요소를 컨테이너에 추가
            imageContainer.appendChild(imgElement);
        });
    })
    .catch(error => console.error('Error fetching images:', error));
