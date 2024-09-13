const notificationEl = document.getElementById('notification');
const notificationCountEl = document.querySelector('.notification-count');
const headerEl = document.querySelector('header');
const toggleNotificationsEl = document.getElementById('toggle-notifications');
const bodyEl = document.querySelector('body');


toggleNotificationsEl.addEventListener('click', toggleNotifications);

// You got access to variable notificationsURL

async function getNotifications() {
    try {
        const response = await fetch(notificationsURL);
        const data = await response.json();

        if (!response.status === 200) {
            throw new Error('Something went wrong with fetching your notifications');
        }
        console.log(data);
        const dataArray = [...data];

        createNotificationElements(dataArray);

    } catch (error) {
        console.error(error)
    }
}

getNotifications().then(data => console.log(data));

function createNotificationElements(notificationsArray) {
    let count = 0;

    const notificationDataEl = document.createElement('div');
    notificationDataEl.classList.add('notification-data');
    notificationDataEl.style.display = 'none';
    headerEl.append(notificationDataEl);

    notificationsArray.forEach(notificationData => {
        const notification = createNotification(notificationData);
        notificationDataEl.append(notification);
        if (!notificationData.seen) {
            count += 1;
        }
    })

    if (count > 0) {
        notificationCountEl.textContent = count;
        notificationCountEl.style.display = 'flex';
    } else {
        notificationCountEl.style.display = 'none';
    }
}

function createNotification(data) {
    console.log('DATAA:', data.__str__)
    let [date, time] = data.created_at.split('T');
    time = time.split('.')[0];

    const notificationContainerEl = document.createElement('a');
    notificationContainerEl.classList.add('notification-container');
    notificationContainerEl.setAttribute('data-pk',  data.pk);
    notificationContainerEl.addEventListener('click', changeNotificationStatus);

    const content = document.createElement('p');
    content.textContent = data['__str__'];
    notificationContainerEl.append(content);
    if (data.seen === false) {
        notificationContainerEl.classList.add('not-seen');
    } else {
        notificationContainerEl.classList.remove('not-seen');
    }

    const auditInfoEl = document.createElement('p');
    auditInfoEl.classList.add('audit-info')
    auditInfoEl.textContent = `${date} at ${time}`;
    notificationContainerEl.append(auditInfoEl);

    return notificationContainerEl;
}


async function changeNotificationStatus(event) {
    event.preventDefault();
    const target = event.target;
    const pk = target.parentNode.getAttribute('data-pk');

    if (!target.parentNode.classList.contains('not-seen')) {
        return;
    }

    try {
        const options = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRFTokenValue,
            },
            method: 'PUT',
            body: JSON.stringify({
                'seen': true
            })
        }
        const response = await fetch(baseNotificationSeenURL + pk + '/', options);
        const data = await response.json()

        if (!response.status === 200) {
            throw Error('Something went wrong changing the status of your notification.')
        }

        target.parentNode.classList.remove('not-seen');
        await getNotifications();

        console.log(data);

    } catch (error) {
        console.error(error)
    }
}

function toggleNotifications(event) {
    event.preventDefault();
    try {
        const notificationDataEl = document.querySelector('.notification-data');
        notificationDataEl.style.display === 'none' ? notificationDataEl.style.display = 'flex' : notificationDataEl.style.display = 'none';

        if (notificationDataEl.style.display === 'none') {
            notificationDataEl.style.maxHeight = '0.2rem';
            bodyEl.removeEventListener('click', clickOutsideNotifications);

        } else if (notificationDataEl.style.display === 'flex') {
            setTimeout(() => notificationDataEl.style.maxHeight = '92vh', 10);
            setTimeout(() => bodyEl.addEventListener('click', clickOutsideNotifications), 20);

        }
    } catch (error) {
        console.error(error, 'An Error occurred!');
    }
}

function clickOutsideNotifications(event) {
    const notificationDataEl = document.querySelector('.notification-data');
    console.log('CLICK', event.target);
    if (
        notificationDataEl !== event.target
        &&
        event.target.parentNode !== notificationDataEl
        &&
        event.target.parentNode.parentNode !== notificationDataEl
    ) {
        toggleNotificationsEl.click();
    }

    console.log('IS SAME: ', notificationDataEl === event.target)
}
