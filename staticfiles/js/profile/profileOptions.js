const profileSettingsElement = document.getElementById('profile-settings');
profileSettingsElement.addEventListener('click', toggleSettings);

function toggleSettings(event) {
    const parentNodeElement = event.target.parentNode;
    const childrenElementsToToggle = Array.from(parentNodeElement.children).slice(7, parentNodeElement.length);

    const settingsWrapperElement = parentNodeElement.querySelectorAll('.settings-options-wrapper')[0];
    const settingsWrapperUlElement = settingsWrapperElement.children[0];

    settingsWrapperElement.style.display !== 'flex' ? displayFirst() : opacityFirst();

    function displayFirst(){
        settingsWrapperElement.style.display = 'flex';

        toggleChildrenElements();

        setTimeout(()=>{
            settingsWrapperUlElement.style.opacity == '100'
            ?
            settingsWrapperUlElement.style.opacity = '0'
            :
            settingsWrapperUlElement.style.opacity = '100';
        }, 50);
    }

    function opacityFirst(){
        settingsWrapperUlElement.style.opacity == '100'
            ?
            settingsWrapperUlElement.style.opacity = '0'
            :
            settingsWrapperUlElement.style.opacity = '100';

        setTimeout(()=>{
            settingsWrapperElement.style.display = 'none';

            toggleChildrenElements();

        }, 500);
    }

    console.log(settingsWrapperUlElement.style['opacity']);
    function toggleChildrenElements () {
        childrenElementsToToggle.forEach(el => {
            el.style['display'] === 'none' ? el.style['display'] = 'flex' : el.style['display'] = 'none';
        });
    }
}
