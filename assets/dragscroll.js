// // // // assets/dragscroll.js
// // // // alert("JavaScript is working!");

document.addEventListener('DOMContentLoaded', function() {
    // Define the target node to observe. This should be a parent element that will contain 'columns-container'.
    // For example, observing the entire body:
    const targetNode = document.body;

    // Define the configuration for the observer:
    const config = { childList: true, subtree: true };

    // Callback function to execute when mutations are observed
    const callback = (mutationsList, observer) => {
        for (let mutation of mutationsList) {
            if (mutation.type === 'childList') {
                // Check added nodes for 'columns-container'
                mutation.addedNodes.forEach(node => {
                    if (node.id === 'columns-container') {
                        initializeSlider(node);
                        // Once the slider is initialized, disconnect the observer if no longer needed
                        observer.disconnect();
                    } else if (node.querySelector && node.querySelector('#columns-container')) {
                        const slider = node.querySelector('#columns-container');
                        initializeSlider(slider);
                        observer.disconnect();
                    }
                });
            }
        }
    };

    // Create an instance of MutationObserver with the callback
    const observer = new MutationObserver(callback);

    // Start observing the target node with the specified configuration
    observer.observe(targetNode, config);

    // Optional: If 'columns-container' might already be present before MutationObserver starts
    const existingSlider = document.getElementById('columns-container');
    if (existingSlider) {
        initializeSlider(existingSlider);
        observer.disconnect();
    }

    // Function to initialize the slider functionality
    function initializeSlider(slider) {
        let isDown = false;
        let startX;
        let scrollLeft;
        console.log("JavaScript is working!");
        console.log("Slider is initializing...");

        // When mouse button is pressed
        slider.addEventListener('mousedown', (e) => {
            isDown = true;
            slider.classList.add('active');
            startX = e.pageX - slider.offsetLeft;
            scrollLeft = slider.scrollLeft;
        });

        // When mouse leaves the slider area
        slider.addEventListener('mouseleave', () => {
            isDown = false;
            slider.classList.remove('active');
        });

        // When mouse button is released
        slider.addEventListener('mouseup', () => {
            isDown = false;
            slider.classList.remove('active');
        });

        // When mouse is moved
        slider.addEventListener('mousemove', (e) => {
            if (!isDown) return; // Stop the function if mouse is not pressed
            e.preventDefault();
            const x = e.pageX - slider.offsetLeft;
            const walk = (x - startX) * 1; // Adjust the multiplier for scroll speed if needed
            slider.scrollLeft = scrollLeft - walk;
        });

        // Optional: Prevent default image dragging by adding a single listener to the slider
        slider.addEventListener('dragstart', (e) => e.preventDefault());

        console.log("Slider is ready.");
    }
});
