/**
 * idesignweb Main JavaScript
 * Vanilla browser script for accessible interactions.
 * Zero external libraries, zero emoji, zero em dashes.
 */

document.addEventListener('DOMContentLoaded', function() {
  // Mobile Navigation Toggle
  const navToggle = document.querySelector('.mobile-nav-toggle');
  const mainNav = document.querySelector('.main-nav');
  
  if (navToggle && mainNav) {
    navToggle.addEventListener('click', function() {
      const isOpen = mainNav.classList.toggle('mobile-open');
      navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      navToggle.textContent = isOpen ? 'Close' : 'Menu';
    });
  }

  // Alert Banner Dismissal
  const dismissButtons = document.querySelectorAll('.alert-dismiss');
  dismissButtons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      const banner = btn.closest('.alert-banner');
      if (banner) {
        banner.remove();
      }
    });
  });

  // Highlight Current Navigation Link
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(function(link) {
    const href = link.getAttribute('href');
    if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
      link.classList.add('active');
    }
  });
});
