document.addEventListener('DOMContentLoaded', () => {
  // Get references to elements
  const MenuToggler = document.getElementById('MenuToggler');
  const MenuScreenBlur = document.getElementById('MenuScreenBlur');
  const MenuItems = document.getElementById('MenuItems');
  const CloseMenu = document.getElementById('CloseMenu');

  // Function to show the sidebar and overlay
  function showSidebar() {
    MenuScreenBlur.classList.remove('d-none');
    MenuItems.style.transform = 'translateX(0)';
  }

  // Function to hide the sidebar and overlay
  function hideSidebar() {
    MenuScreenBlur.classList.add('d-none');
    MenuItems.style.transform = 'translateX(-100%)';
  }

  // Add event listeners
  MenuToggler.addEventListener('click', showSidebar);
  CloseMenu.addEventListener('click', hideSidebar);

  // Handle sidebar navigation link clicks
  document.querySelectorAll('#MenuItems .nav-link').forEach(link => {
    link.addEventListener('click', function (e) {
      // Check if the link is not a dropdown toggle
      if (!this.classList.contains('dropdown-toggle-link')) {
        e.preventDefault();
        const url = this.getAttribute('href'); // URL from href attribute

        fetch(url)
          .then(response => response.text())
          .then(html => {
            console.log('Page loaded:', html);
            document.getElementById('SinglePageApplicationRoot').innerHTML = html;
            hideSidebar(); // Hide sidebar after loading content
          })
          .catch(error => {
            console.error('Error loading the page:', error);
          });
      }
    });
  });
});