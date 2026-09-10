/**
 * idesignweb Member Portal Interactions
 * Handles deliverable status filters, approval workflow modal, and ticket updates.
 * Zero emoji, zero em dashes.
 */

document.addEventListener('DOMContentLoaded', function() {
  // Deliverable Status Filter
  const filterButtons = document.querySelectorAll('[data-filter-status]');
  const deliverableCards = document.querySelectorAll('[data-status]');

  filterButtons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      const targetStatus = btn.getAttribute('data-filter-status');
      
      filterButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      deliverableCards.forEach(function(card) {
        if (targetStatus === 'all' || card.getAttribute('data-status') === targetStatus) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // Ticket Message Quick Reply Toggle
  const replyToggle = document.getElementById('toggle-reply-form');
  const replyBox = document.getElementById('ticket-reply-container');
  if (replyToggle && replyBox) {
    replyToggle.addEventListener('click', function() {
      const isHidden = replyBox.style.display === 'none';
      replyBox.style.display = isHidden ? 'block' : 'none';
      replyToggle.textContent = isHidden ? '[ HIDE REPLY FORM ]' : '[ ADD REPLY ]';
    });
  }
});
