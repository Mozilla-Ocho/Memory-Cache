document.addEventListener('DOMContentLoaded', function () {
    var accordionButtons = document.querySelectorAll('.accordion-button');

    accordionButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            // This line optionally allows for closing all other accordions when one is opened.
            const currentlyActiveAccordionButton = document.querySelector('.accordion-button.active');
            if(currentlyActiveAccordionButton && currentlyActiveAccordionButton !== button) {
                currentlyActiveAccordionButton.classList.toggle('active');
                currentlyActiveAccordionButton.nextElementSibling.style.maxHeight = null;
            }

            button.classList.toggle('active');
            var accordionContent = button.nextElementSibling;
            if (accordionContent.style.maxHeight) {
                accordionContent.style.maxHeight = null;
            } else {
                accordionContent.style.maxHeight = accordionContent.scrollHeight + 30 + "px";
            }
        });
    });
});
