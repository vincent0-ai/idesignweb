/**
 * Idesignweb Main JavaScript
 * Vanilla browser script for accessible interactions and interactive studio dock.
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

  // Antigravity-Style Studio Console Tab Switcher
  const consoleTabs = document.querySelectorAll('.console-tab');
  const consolePanels = document.querySelectorAll('.console-panel');

  if (consoleTabs.length > 0 && consolePanels.length > 0) {
    consoleTabs.forEach(function(tab) {
      tab.addEventListener('click', function() {
        const targetTab = tab.getAttribute('data-tab');

        consoleTabs.forEach(function(t) {
          t.classList.remove('active');
          t.setAttribute('aria-selected', 'false');
        });

        consolePanels.forEach(function(panel) {
          panel.classList.remove('active');
        });

        tab.classList.add('active');
        tab.setAttribute('aria-selected', 'true');

        const activePanel = document.getElementById('panel-' + targetTab);
        if (activePanel) {
          activePanel.classList.add('active');
        }
      });
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

