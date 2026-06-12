function initTestimonialSwiper() {
  const el = document.querySelector('.testimonial-swiper');
  if (!el || typeof Swiper === 'undefined') return;

  new Swiper('.testimonial-swiper', {
    slidesPerView: 1,
    spaceBetween: 32,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
      768: {
        slidesPerView: 1.5,
      },
      1280: {
        slidesPerView: 2,
      },
    },
  });
}

document.addEventListener('DOMContentLoaded', initTestimonialSwiper);
