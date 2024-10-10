// Document Ready
$(document).ready(function () {
  // Initial page setup
  initPage();

  // Handle page navigation links (Inicio, Servicios, etc.)
  $('.tm-page-link').on('click', function (event) {
    event.preventDefault();
    const targetPage = $(this.hash); // Get the target page by hash
    // Highlight the selected menu item
    highlightMenu($(this));
    // Show the correct page and hide the rest
    showPage(targetPage);
  });

  // Handle tab navigation within the food section (Restaurantes, Bares, Cafeterías)
  $('.tm-tab-link').on('click', function (event) {
    event.preventDefault();
    openTab($(this).data('id'));
  });

  // Search filtering logic (para todas las categorías)
  $('#search-input').on('input', function () {
    const searchText = $(this).val().toLowerCase();

    // Mostrar todas las categorías cuando hay texto en la barra de búsqueda
    if (searchText !== "") {
      $('.tm-tab-content').show(); // Muestra todas las categorías
    }

    // Filtrar elementos en todas las categorías por nombre, tipo o palabras clave
    $('.tm-list-item').each(function () {
      const placeName = $(this).find('.tm-list-item-name').text().toLowerCase();
      const placeTypes = $(this).data('types') ? $(this).data('types').toLowerCase() : '';
      const placeKeywords = $(this).data('keywords') ? $(this).data('keywords').toLowerCase() : '';

      // Mostrar el elemento si coincide con el nombre, tipo de comida o palabra clave
      $(this).toggle(
        placeName.includes(searchText) || placeTypes.includes(searchText) || placeKeywords.includes(searchText)
      );
    });

    // Si la búsqueda está vacía, mostrar solo la categoría seleccionada
    if (searchText === "") {
      const activeTabId = $('.tm-tab-link.active').data('id');
      $('.tm-tab-content').hide();  // Oculta todas las categorías
      $('#' + activeTabId).show();  // Muestra solo la categoría activa
    }
  });

  // Manejar el clic en el botón de filtro de ciudad
  $('#city-filter-btn').on('click', function () {
    document.getElementById('city-splash').style.display = 'flex';
  });

  // Cerrar el splash de ciudad
  $('#close-splash').on('click', function () {
    document.getElementById('city-splash').style.display = 'none';
  });

/*
  // Manejar el dropdown de categorías (Restaurantes, Bares, Cafeterías)
  const dropdownBtn = document.querySelector('.tm-dropdown-btn');
  const dropdownOptions = document.getElementById('dropdown-options');
  const dropdownIcon = dropdownBtn.querySelector('i');

  // Toggle visibility of dropdown options and arrow direction on button click
  dropdownBtn.addEventListener('click', function () {
    const isVisible = dropdownOptions.style.display === 'block';
    dropdownOptions.style.display = isVisible ? 'none' : 'block';
    dropdownIcon.classList.toggle('fa-chevron-up', !isVisible);
    dropdownIcon.classList.toggle('fa-chevron-down', isVisible);
  });

  // Close the dropdown when an option is selected
  document.querySelectorAll('#dropdown-options a').forEach(function (link) {
    link.addEventListener('click', function () {
      dropdownOptions.style.display = 'none';
      dropdownIcon.classList.remove('fa-chevron-up');
      dropdownIcon.classList.add('fa-chevron-down');
    });
  });*/
});

$('.tm-dropdown-btn').on('click', function () {
  const dropdownOptions = $('#dropdown-options');
  const dropdownIcon = $(this).find('i');
  dropdownOptions.toggle(); // Alternar visibilidad del dropdown
  dropdownIcon.toggleClass('fa-chevron-up fa-chevron-down');
});

$('#dropdown-options a').on('click', function () {
  $('#dropdown-options').hide();
  $('.tm-dropdown-btn i').removeClass('fa-chevron-up').addClass('fa-chevron-down');
});

function initPage() {
  // Ocultar todo el contenido de las páginas excepto la página de inicio
  $('.tm-page-content').hide();
  $('#food').show(); // Mostrar la sección de Gula Maps

  // Inicializar las pestañas de Gula Maps
  $('.tm-tab-content').hide(); // Ocultar todas las categorías
  $('#resta').show(); // Mostrar Restaurantes por defecto
  $('.tm-tab-link').removeClass('active');
  $('.tm-tab-link[data-id="resta"]').addClass('active');
}

function openTab(id) {
  // Hide all tab content
  $('.tm-tab-content').hide();
  // Show the selected tab content
  $('#' + id).show();
  // Deactivate all tabs and activate the selected one
  $('.tm-tab-link').removeClass('active');
  $('.tm-tab-link[data-id="' + id + '"]').addClass('active');
}

function highlightMenu(menuItem) {
  // Deactivate all menu items and activate the selected one
  $('.tm-page-link').removeClass('active');
  menuItem.addClass('active');
}

function showPage(page) {
  // Ocultar todas las secciones
  $('.tm-page-content').hide(); // Oculta todo el contenido de la página
  $('.tm-tab-content').hide();  // Oculta las categorías de Gula Maps

  // Verificar si la página actual es "Gula Maps"
  if (page.attr('id') === 'food') {
    // Mostrar Gula Maps y la primera categoría (restaurantes)
    $('#food').show();
    $('#resta').show();
    $('.tm-tab-link').removeClass('active');
    $('.tm-tab-link[data-id="resta"]').addClass('active');
  } else {
    // Mostrar la página seleccionada (Servicios, Contacto, etc.)
    page.show();
  }
}