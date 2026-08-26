/* ==========================================================================
   AuthorWings — Author Websites page
   --------------------------------------------------------------------------
   Two small enhancements, both optional: the page is fully readable and
   usable with this file removed. The FAQ is native <details>, so it needs no
   script at all.
   ========================================================================== */
(function () {
	'use strict';

	var root = document.querySelector('.aw-ws');
	if (!root) return;

	var wantsMotion = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

	/* --- Scroll reveal -------------------------------------------------- */
	var revealables = root.querySelectorAll('.ws-reveal');

	if (!wantsMotion || !('IntersectionObserver' in window)) {
		// Show everything at once rather than leaving it invisible.
		root.classList.add('no-reveal');
	} else {
		var observer = new IntersectionObserver(function (entries) {
			entries.forEach(function (entry) {
				if (!entry.isIntersecting) return;
				entry.target.classList.add('is-in');
				observer.unobserve(entry.target);
			});
		}, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

		Array.prototype.forEach.call(revealables, function (el) {
			observer.observe(el);
		});
	}

	/* --- Sticky bar shadow ---------------------------------------------- */
	var bar = document.getElementById('ws-bar');
	if (bar) {
		var sentinel = document.createElement('div');
		sentinel.setAttribute('aria-hidden', 'true');
		sentinel.style.cssText = 'position:absolute;top:0;height:1px;width:1px';
		bar.parentNode.insertBefore(sentinel, bar);

		if ('IntersectionObserver' in window) {
			new IntersectionObserver(function (entries) {
				bar.classList.toggle('is-stuck', !entries[0].isIntersecting);
			}).observe(sentinel);
		}
	}

	/* --- Smooth in-page links, when motion is welcome -------------------- */
	if (wantsMotion) {
		root.addEventListener('click', function (event) {
			var link = event.target.closest('a[href^="#"]');
			if (!link) return;

			var id = link.getAttribute('href');
			if (id === '#' || id.length < 2) return;

			var target = document.querySelector(id);
			if (!target) return;

			event.preventDefault();
			target.scrollIntoView({ behavior: 'smooth', block: 'start' });
			// Keep keyboard focus in step with the scroll position.
			target.setAttribute('tabindex', '-1');
			target.focus({ preventScroll: true });
			history.replaceState(null, '', id);
		});
	}
})();
