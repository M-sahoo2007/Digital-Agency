document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initMobileMenu();
  initMarquee();
  initLenis();
  initProjectFilters();
  initBlogPage();
  initContactForm();
  initCalendar();
  initNewsletter();
  setActiveNavLink();
  initLazyLoading();
});

function initNavbar() {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;

  const onScroll = () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

function initMobileMenu() {
  const hamburger = document.querySelector('.hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (!hamburger || !mobileMenu) return;

  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    mobileMenu.classList.toggle('open');
    document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
  });

  mobileMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('active');
      mobileMenu.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
}

function initMarquee() {
  const marquee = document.querySelector('.marquee');
  if (!marquee) return;

  const track = marquee.querySelector('.marquee-track');
  if (!track) return;

  const clone = track.cloneNode(true);
  clone.setAttribute('aria-hidden', 'true');
  marquee.appendChild(clone);
}

function initLenis() {
  if (typeof Lenis === 'undefined') return;

  const lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
  });

  function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }

  requestAnimationFrame(raf);

  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
  }
}

function setActiveNavLink() {
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.navbar-nav a, .mobile-menu a').forEach((link) => {
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });
}

const FALLBACK_PROJECTS = [
  { id: 1, title: 'Finance Management System', category: 'App Design', image: 'assets/images/project-1.svg' },
  { id: 2, title: 'SaaS Dashboard UI', category: 'SaaS', image: 'assets/images/project-2.svg' },
  { id: 3, title: 'Crypto Trading Platform', category: 'SaaS', image: 'assets/images/project-3.svg' },
  { id: 4, title: 'E-commerce Redesign', category: 'Webflow Development', image: 'assets/images/project-4.svg' },
  { id: 5, title: 'Health & Fitness App', category: 'App Design', image: 'assets/images/project-5.svg' },
  { id: 6, title: 'Real Estate Portal', category: 'Webflow Development', image: 'assets/images/project-6.svg' },
  { id: 7, title: 'Banking App Interaction', category: 'App Design', image: 'assets/images/project-7.svg' },
  { id: 8, title: 'Analytics Dashboard', category: 'SaaS', image: 'assets/images/project-8.svg' },
];

const FALLBACK_BLOGS = [
  { id: 1, title: 'The Future of Digital Product Design in 2026', category: 'Design', image: 'assets/images/blog-1.svg', created_at: '2026-01-15' },
  { id: 2, title: 'Building Scalable SaaS Applications', category: 'Development', image: 'assets/images/blog-2.svg', created_at: '2026-01-10' },
  { id: 3, title: 'Why Minimal Design Drives Conversion', category: 'Strategy', image: 'assets/images/blog-3.svg', created_at: '2025-12-28' },
  { id: 4, title: 'Mobile-First Development Best Practices', category: 'Development', image: 'assets/images/blog-4.svg', created_at: '2025-12-20' },
  { id: 5, title: 'The Role of AI in Creative Agencies', category: 'Innovation', image: 'assets/images/blog-5.svg', created_at: '2025-12-12' },
  { id: 6, title: 'Webflow vs Custom Development', category: 'Strategy', image: 'assets/images/blog-6.svg', created_at: '2025-12-05' },
];

function renderProjectCard(project) {
  return `
    <article class="project-card hover-lift hover-zoom stagger-item" data-category="${project.category}">
      <div class="project-card-image">
        <img src="${project.image}" alt="${project.title}" loading="lazy" width="600" height="400">
      </div>
      <div class="project-card-info">
        <p class="project-card-category">${project.category}</p>
        <h3 class="project-card-title">${project.title}</h3>
      </div>
    </article>
  `;
}

async function loadProjects(category = 'all') {
  const grid = document.querySelector('.projects-grid');
  if (!grid) return;

  let projects = FALLBACK_PROJECTS;

  try {
    const data = await window.msahooAPI.getProjects(category);
    if (data.projects && data.projects.length) {
      projects = data.projects.map((p) => ({
        ...p,
        image: p.image.startsWith('http') ? p.image : p.image.replace('.jpg', '.svg'),
      }));
    }
  } catch {
    if (category !== 'all') {
      projects = FALLBACK_PROJECTS.filter((p) => p.category === category);
    }
  }

  grid.innerHTML = projects.map(renderProjectCard).join('');

  if (typeof gsap !== 'undefined') {
    gsap.utils.toArray('.stagger-item').forEach((el, i) => {
      gsap.fromTo(el, { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, delay: i * 0.08, ease: 'power3.out' });
    });
  }
}

function initProjectFilters() {
  const filters = document.querySelector('.filters');
  if (!filters) return;

  loadProjects();

  filters.addEventListener('click', (e) => {
    const btn = e.target.closest('.filter-btn');
    if (!btn) return;

    filters.querySelectorAll('.filter-btn').forEach((b) => b.classList.remove('active'));
    btn.classList.add('active');
    loadProjects(btn.dataset.filter);
  });
}

function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function renderBlogCard(blog) {
  return `
    <article class="blog-card stagger-item">
      <div class="blog-card-image">
        <img src="${blog.image}" alt="${blog.title}" loading="lazy" width="400" height="260">
      </div>
      <div class="blog-card-body">
        <div class="blog-card-meta">
          <span class="blog-card-category">${blog.category}</span>
          <span>${formatDate(blog.created_at)}</span>
        </div>
        <h3 class="blog-card-title">${blog.title}</h3>
        <a href="#" class="blog-card-link" data-blog-id="${blog.id}">Read More <span>&rarr;</span></a>
      </div>
    </article>
  `;
}

let blogState = { page: 1, search: '', category: 'all', totalPages: 1 };

async function loadBlogs() {
  const grid = document.querySelector('.blog-grid');
  if (!grid) return;

  let blogs = FALLBACK_BLOGS;
  let totalPages = 1;

  try {
    const params = { page: blogState.page, per_page: 6 };
    if (blogState.search) params.search = blogState.search;
    if (blogState.category !== 'all') params.category = blogState.category;

    const data = await window.msahooAPI.getBlogs(params);
    if (data.blogs && data.blogs.length) {
      blogs = data.blogs.map((b) => ({
        ...b,
        image: b.image.startsWith('http') ? b.image : b.image.replace('.jpg', '.svg'),
      }));
      totalPages = data.pages || 1;
    }
  } catch {
    blogs = FALLBACK_BLOGS.filter((b) => {
      const matchSearch = !blogState.search || b.title.toLowerCase().includes(blogState.search.toLowerCase());
      const matchCategory = blogState.category === 'all' || b.category === blogState.category;
      return matchSearch && matchCategory;
    });
    totalPages = Math.ceil(blogs.length / 6) || 1;
    const start = (blogState.page - 1) * 6;
    blogs = blogs.slice(start, start + 6);
  }

  blogState.totalPages = totalPages;
  grid.innerHTML = blogs.map(renderBlogCard).join('');
  renderPagination();
}

function renderPagination() {
  const pagination = document.querySelector('.pagination');
  if (!pagination) return;

  let html = `<button ${blogState.page <= 1 ? 'disabled' : ''} data-page="${blogState.page - 1}">&larr;</button>`;

  for (let i = 1; i <= blogState.totalPages; i++) {
    html += `<button class="${i === blogState.page ? 'active' : ''}" data-page="${i}">${i}</button>`;
  }

  html += `<button ${blogState.page >= blogState.totalPages ? 'disabled' : ''} data-page="${blogState.page + 1}">&rarr;</button>`;
  pagination.innerHTML = html;
}

function initBlogPage() {
  const blogGrid = document.querySelector('.blog-grid');
  if (!blogGrid) return;

  loadBlogs();

  const searchInput = document.querySelector('#blog-search');
  if (searchInput) {
    let debounce;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounce);
      debounce = setTimeout(() => {
        blogState.search = e.target.value;
        blogState.page = 1;
        loadBlogs();
      }, 300);
    });
  }

  const categoryFilters = document.querySelector('.blog-categories');
  if (categoryFilters) {
    categoryFilters.addEventListener('click', (e) => {
      const btn = e.target.closest('.filter-btn');
      if (!btn) return;
      categoryFilters.querySelectorAll('.filter-btn').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      blogState.category = btn.dataset.filter;
      blogState.page = 1;
      loadBlogs();
    });
  }

  const pagination = document.querySelector('.pagination');
  if (pagination) {
    pagination.addEventListener('click', (e) => {
      const btn = e.target.closest('button[data-page]');
      if (!btn || btn.disabled) return;
      blogState.page = parseInt(btn.dataset.page, 10);
      loadBlogs();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  blogGrid.addEventListener('click', async (e) => {
    const link = e.target.closest('[data-blog-id]');
    if (!link) return;
    e.preventDefault();
    try {
      const data = await window.msahooAPI.getBlog(link.dataset.blogId);
      alert(data.content || data.title);
    } catch {
      const blog = FALLBACK_BLOGS.find((b) => b.id === parseInt(link.dataset.blogId, 10));
      if (blog) alert(blog.title);
    }
  });
}

function initContactForm() {
  const form = document.querySelector('#contact-form');
  if (!form) return;

  const pills = form.querySelectorAll('.service-pill');
  let selectedService = '';

  pills.forEach((pill) => {
    pill.addEventListener('click', () => {
      pills.forEach((p) => p.classList.remove('active'));
      pill.classList.add('active');
      selectedService = pill.dataset.service;
    });
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msgEl = form.querySelector('.form-message');
    const submitBtn = form.querySelector('[type="submit"]');
    const originalText = submitBtn.textContent;

    const formData = {
      name: form.querySelector('#name').value.trim(),
      email: form.querySelector('#email').value.trim(),
      phone: form.querySelector('#phone').value.trim(),
      website: form.querySelector('#website').value.trim(),
      message: form.querySelector('#message').value.trim(),
      service: selectedService,
    };

    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    msgEl.className = 'form-message';
    msgEl.textContent = '';

    try {
      await window.msahooAPI.submitContact(formData);
      msgEl.className = 'form-message success';
      msgEl.textContent = 'Thank you! Your message has been sent successfully.';
      form.reset();
      pills.forEach((p) => p.classList.remove('active'));
      selectedService = '';
    } catch (err) {
      msgEl.className = 'form-message error';
      msgEl.textContent = err.message || 'Something went wrong. Please try again.';
    } finally {
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }
  });
}

function initCalendar() {
  const widget = document.querySelector('.calendar-widget');
  if (!widget) return;

  const daysContainer = widget.querySelector('.calendar-days');
  const monthLabel = widget.querySelector('.calendar-month');
  const prevBtn = widget.querySelector('.cal-prev');
  const nextBtn = widget.querySelector('.cal-next');
  const timeSlots = widget.querySelectorAll('.time-slot');
  const scheduleBtn = widget.querySelector('.calendar-schedule-btn');

  let currentDate = new Date();
  let selectedDay = null;
  let selectedTime = null;

  function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const today = new Date();

    monthLabel.textContent = currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    let html = '';
    for (let i = 0; i < firstDay; i++) {
      html += '<div class="calendar-day empty"></div>';
    }

    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(year, month, day);
      const isPast = date < new Date(today.getFullYear(), today.getMonth(), today.getDate());
      const isSelected = selectedDay === day;
      html += `<div class="calendar-day ${isPast ? 'disabled' : ''} ${isSelected ? 'selected' : ''}" data-day="${day}">${day}</div>`;
    }

    daysContainer.innerHTML = html;
  }

  prevBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    selectedDay = null;
    renderCalendar();
  });

  nextBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    selectedDay = null;
    renderCalendar();
  });

  daysContainer.addEventListener('click', (e) => {
    const day = e.target.closest('.calendar-day:not(.disabled):not(.empty)');
    if (!day) return;
    selectedDay = parseInt(day.dataset.day, 10);
    daysContainer.querySelectorAll('.calendar-day').forEach((d) => d.classList.remove('selected'));
    day.classList.add('selected');
  });

  timeSlots.forEach((slot) => {
    slot.addEventListener('click', () => {
      timeSlots.forEach((s) => s.classList.remove('selected'));
      slot.classList.add('selected');
      selectedTime = slot.textContent;
    });
  });

  if (scheduleBtn) {
    scheduleBtn.addEventListener('click', () => {
      if (!selectedDay || !selectedTime) {
        alert('Please select a date and time slot.');
        return;
      }
      const dateStr = currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
      alert(`Discovery call scheduled for ${dateStr} ${selectedDay} at ${selectedTime}. We'll send a confirmation email shortly.`);
    });
  }

  renderCalendar();
}

function initNewsletter() {
  document.querySelectorAll('.footer-newsletter').forEach((form) => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const input = form.querySelector('input[type="email"]');
      const btn = form.querySelector('button');
      const email = input.value.trim();
      if (!email) return;

      btn.textContent = '...';
      try {
        await window.msahooAPI.subscribeNewsletter(email);
        input.value = '';
        btn.textContent = 'Done!';
        setTimeout(() => { btn.textContent = 'Subscribe'; }, 2000);
      } catch (err) {
        btn.textContent = 'Error';
        setTimeout(() => { btn.textContent = 'Subscribe'; }, 2000);
      }
    });
  });
}

function initLazyLoading() {
  if ('loading' in HTMLImageElement.prototype) return;

  const images = document.querySelectorAll('img[loading="lazy"]');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
        }
        observer.unobserve(img);
      }
    });
  });

  images.forEach((img) => observer.observe(img));
}
