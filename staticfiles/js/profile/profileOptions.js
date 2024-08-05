const profileSettingsElement = document.getElementById('profile-settings');
profileSettingsElement.addEventListener('click', toggleSettings);

function toggleSettings(event) {
    const parentNodeElement = event.target.parentNode;
    const childrenElementsToToggle = Array.from(parentNodeElement.children).slice(4, parentNodeElement.length);

    const settingsWrapperElement = parentNodeElement.querySelectorAll('.settings-options-wrapper')[0];

    settingsWrapperElement.style.display !== 'flex'
        ?
        settingsWrapperElement.style.display = 'flex'
        :
        settingsWrapperElement.style.display = 'none';

    childrenElementsToToggle.forEach(el => {
        el.style['display'] === 'none' ? el.style['display'] = 'flex' : el.style['display'] = 'none';
    })
}