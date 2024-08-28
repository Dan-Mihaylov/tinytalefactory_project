const totalStoriesCountEl = document.getElementById('total-stories-count');
const totalPublicStoriesCountEl = document.getElementById('total-public-stories-count');
const totalUsersCountEl = document.getElementById('total-users-count');

const browseStoriesEl = document.querySelector('.section-browse-stories');

const siteEl = document.querySelector('.section-main').children[0];


document.onload = pageLoadingFunctionality();


function pageLoadingFunctionality() {
    getBaseStats();
    siteElOpacityRegulator();
    setTimeout(displayStoryCards, 2000);
}
function siteElOpacityRegulator() {
    siteEl.style.display = 'none';
    siteEl.style.opacity = 0;
    setTimeout(() => siteEl.style.display = 'block', 500);
    siteEl.style.transition = 'opacity 1s linear';
    setTimeout(() => siteEl.style.opacity = '1', 1000);
}

async function displayStoryCards() {
    try {
        const response = await fetch(apiSampleStoriesUrl);
        const data = await response.json();

        if (!response.ok) {
            throw Error('There was a problem getting the sample stories.')
        }

        function getCardDataAndGenerateCards(n){
            if (n === data.length) {
                return;
            }

            const object = data[n];
            const imageUrl = object['info']['urls'][0];
            const title = object['title'];
            const slug = object['slug'];

            generateCard(imageUrl, title, slug);

            setTimeout(() => getCardDataAndGenerateCards(n + 1), 500)
        }

        getCardDataAndGenerateCards(0);

    } catch (error) {
        console.error(error);
    }
}

function generateCard(url, title, slug) {
    const aCardEl = document.createElement('a');
    aCardEl.classList.add('browse-story-card');
    aCardEl.setAttribute('href', baseViewStoryUrl.replace('placeholder', slug));

    const mediaDivEl = document.createElement('div');
    mediaDivEl.classList.add('browse-story-media-container');
    aCardEl.append(mediaDivEl);

    const imgEl = document.createElement('img');
    imgEl.classList.add('browse-story-image');
    imgEl.setAttribute('src', url);
    mediaDivEl.append(imgEl);

    const titleEl = document.createElement('h4');
    titleEl.textContent = title;
    aCardEl.append(titleEl);

    const overlayEl = document.createElement('div');
    overlayEl.classList.add('card-overlay');
    aCardEl.append(overlayEl);

    const pClickHereEl = document.createElement('p');
    pClickHereEl.textContent = 'Click here to view story';
    overlayEl.append(pClickHereEl);

    browseStoriesEl.append(aCardEl);
}

// Fetch the stats and increment the elements animated

async function getBaseStats() {
    try {
        const response = await fetch(apiBaseStatsUrl);
        const data = await response.json();
        
        animateCountObject(totalStoriesCountEl, data.total_stories);
        animateCountObject(totalPublicStoriesCountEl, data.public_stories);
        animateCountObject(totalUsersCountEl, data.total_users);
        
    } catch (error) {
        console.error(error);
    }
}

function animateCountObject(object, total) {
    const number = Number(total);
    let timeout;

    if (number <= 10) {
        timeout = 150;
    } else if (number <= 50) {
        timeout = 50;
    } else {
        timeout = 40
    }

    function recurse(n) {
        if (n === number) {
            return;
        }

        object.textContent = n;
        setTimeout(() => recurse(n + 1), timeout);
    }

    recurse(0);
}

