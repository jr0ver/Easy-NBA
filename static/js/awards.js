document.addEventListener('DOMContentLoaded', () => {
    // get the awards data from the data attribute
    const awardsContainer = document.getElementsByClassName('awards')[0];
    const awardsData = awardsContainer.getAttribute('data-awards'); // Get the JSON string

    let awards;
    try {
        awards = JSON.parse(awardsData);
    } catch (error) {
        console.error('Error parsing awards data:', error);
        return;
    }

    if (Array.isArray(awards)) {
        awards.forEach(award => {
            const banner = document.createElement('div'); 
            banner.className = 'award';

            // svg for icons?
            // const svg = `<svg width="24" height="24" xmlns="http://www.w3.org/2000/svg">
            //                 <circle cx="12" cy="12" r="10" fill="#007BFF" />
            //              </svg>`; // Example SVG (blue circle)

            const textElement = document.createElement('p');
            textElement.innerText = award;
            textElement.className = 'award-text';

            // banner.innerHTML = svg;
            banner.appendChild(textElement);

            awardsContainer.appendChild(banner); // add the banner to the awards container
        });
    } else {
        console.error('Awards data is not an array or is undefined');
    }
});
