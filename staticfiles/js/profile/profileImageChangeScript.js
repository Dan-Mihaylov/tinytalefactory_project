const imgEl = document.querySelector('.profile-image-container img');

imgEl.addEventListener('click', (e) => changeImage(e));

const imageUrls = [
    'https://res.cloudinary.com/dh7ur0uv3/image/upload/t_profile-pic-ttf/v1731072029/cat1_wl5bfj.webp',
    'https://res.cloudinary.com/dh7ur0uv3/image/upload/t_profile-pic-ttf/v1731072370/cat2_arnkxb.webp',
    'https://res.cloudinary.com/dh7ur0uv3/image/upload/t_profile-pic-ttf/v1731072371/cat3_dxr6ek.webp',
    'https://res.cloudinary.com/dh7ur0uv3/image/upload/t_profile-pic-ttf/v1731072371/cat4_s6nwvb.jpg',
    'https://res.cloudinary.com/dh7ur0uv3/image/upload/t_profile-pic-ttf/v1731072405/cat5_xmxrvm.webp',
]

function changeImage(e) {
    const max = imageUrls.length - 1;
    const min = 0;
    const randomIndex = Math.floor(Math.random() * (max - min + 1)) + min;

    imgEl.setAttribute('src', imageUrls[randomIndex]);
}

changeImage();

