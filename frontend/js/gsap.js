function initGSAPAnimations() {
  if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;

  gsap.registerPlugin(ScrollTrigger);

  gsap.utils.toArray('.fade-up').forEach((el) => {
    gsap.to(el, {
      scrollTrigger: {
        trigger: el,
        start: 'top 85%',
        toggleActions: 'play none none none',
      },
      y: 0,
      opacity: 1,
      duration: 0.8,
      ease: 'power3.out',
    });
  });

  gsap.utils.toArray('.stagger-item').forEach((el, i) => {
    gsap.to(el, {
      scrollTrigger: {
        trigger: el.parentElement,
        start: 'top 80%',
        toggleActions: 'play none none none',
      },
      y: 0,
      opacity: 1,
      duration: 0.6,
      delay: i * 0.1,
      ease: 'power3.out',
    });
  });

  gsap.utils.toArray('.reveal-text').forEach((el) => {
    const lines = el.querySelectorAll('.line');
    if (lines.length) {
      gsap.to(lines, {
        scrollTrigger: {
          trigger: el,
          start: 'top 85%',
          toggleActions: 'play none none none',
        },
        y: 0,
        opacity: 1,
        duration: 0.8,
        stagger: 0.15,
        ease: 'power3.out',
      });
    }
  });

  gsap.utils.toArray('.parallax-inner').forEach((el) => {
    gsap.to(el, {
      scrollTrigger: {
        trigger: el.parentElement,
        start: 'top bottom',
        end: 'bottom top',
        scrub: true,
      },
      y: -60,
      ease: 'none',
    });
  });

  const heroTitle = document.querySelector('.hero-title');
  if (heroTitle) {
    gsap.from(heroTitle, {
      y: 60,
      opacity: 0,
      duration: 1.2,
      ease: 'power3.out',
      delay: 0.3,
    });
  }

  const heroRight = document.querySelector('.hero-right');
  if (heroRight) {
    gsap.from(heroRight.children, {
      y: 40,
      opacity: 0,
      duration: 0.8,
      stagger: 0.15,
      ease: 'power3.out',
      delay: 0.6,
    });
  }

  initMagneticButtons();
  initCounterAnimation();
}

function initMagneticButtons() {
  document.querySelectorAll('.btn-magnetic').forEach((btn) => {
    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;

      gsap.to(btn, {
        x: x * 0.2,
        y: y * 0.2,
        duration: 0.3,
        ease: 'power2.out',
      });
    });

    btn.addEventListener('mouseleave', () => {
      gsap.to(btn, {
        x: 0,
        y: 0,
        duration: 0.5,
        ease: 'elastic.out(1, 0.5)',
      });
    });
  });
}

function initCounterAnimation() {
  document.querySelectorAll('[data-counter]').forEach((el) => {
    const target = parseInt(el.dataset.counter, 10);
    const suffix = el.dataset.suffix || '';
    const format = el.dataset.format || 'number';

    ScrollTrigger.create({
      trigger: el,
      start: 'top 85%',
      once: true,
      onEnter: () => {
        gsap.to({ val: 0 }, {
          val: target,
          duration: 2,
          ease: 'power2.out',
          onUpdate: function () {
            const current = Math.floor(this.targets()[0].val);
            if (format === 'thousands') {
              el.textContent = `${Math.floor(current / 1000)}K+`;
            } else if (format === 'currency-m') {
              el.textContent = `$${current}M+`;
            } else {
              el.textContent = `${current}${suffix}`;
            }
          },
        });
      },
    });
  });
}

function initPageTransition() {
  const main = document.querySelector('main');
  if (main) {
    main.classList.add('loaded');
  }

  const loader = document.querySelector('.page-loader');
  if (loader) {
    setTimeout(() => loader.classList.add('hidden'), 800);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initPageTransition();
  initGSAPAnimations();
});
