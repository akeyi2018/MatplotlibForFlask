document.addEventListener('DOMContentLoaded', function() {
    var dropdownToggleList = document.querySelectorAll('.dropdown-toggle');
    dropdownToggleList.forEach(function(dropdownToggle) {
        dropdownToggle.addEventListener('click', function() {
            var dropdownMenu = dropdownToggle.nextElementSibling;
            if (dropdownMenu.classList.contains('show')) {
                dropdownMenu.classList.remove('show');
            } else {
                // Close all other dropdowns
                var openDropdowns = document.querySelectorAll('.dropdown-menu.show');
                openDropdowns.forEach(function(openDropdown) {
                    if (openDropdown !== dropdownMenu) {
                        openDropdown.classList.remove('show');
                    }
                });
                dropdownMenu.classList.add('show');
            }
        });
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
        var isDropdownTarget = Array.from(dropdownToggleList).some(function(dropdownToggle) {
            return dropdownToggle.contains(event.target);
        });
        
        var dropdownMenus = document.querySelectorAll('.dropdown-menu');
        dropdownMenus.forEach(function(dropdownMenu) {
            if (!dropdownMenu.contains(event.target) && !isDropdownTarget) {
                dropdownMenu.classList.remove('show');
            }
        });
    });
  });