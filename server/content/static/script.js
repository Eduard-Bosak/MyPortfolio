document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('.site-header');
  const themeBtn = document.querySelector('.theme-toggle');
  const langBtn = document.querySelector('.lang-toggle');
  const navLinks = document.querySelectorAll('.main-navigation a');
  
  // --- Инициализация Particles.js ---
  if (document.getElementById('particles-js')) {
    particlesJS('particles-js', {
      particles: {
        number: { 
          value: 80, 
          density: { enable: true, value_area: 800 } 
        },
        color: { value: '#007aff' },
        opacity: { 
          value: 0.5, 
          random: false,
          anim: { enable: false }
        },
        size: { 
          value: 3, 
          random: true,
          anim: { enable: false } 
        },
        line_linked: {
          enable: true,
          distance: 150,
          color: '#007aff',
          opacity: 0.4,
          width: 1
        },
        move: {
          enable: true,
          speed: 2,
          direction: 'none',
          random: false,
          straight: false,
          out_mode: 'out', // Изменяем на "bounce" чтобы частицы не выходили за пределы
          bounce: true,    // Включаем отскок от границ контейнера
        }
      },
      interactivity: {
        detect_on: 'canvas',
        events: {
          onhover: { enable: true, mode: 'grab' },
          onclick: { enable: true, mode: 'push' },
          resize: true
        },
        modes: {
          grab: { distance: 140, line_linked: { opacity: 1 } },
          push: { particles_nb: 4 }
        }
      },
      retina_detect: true
    });
    
    // Обновляем цвета частиц при смене темы
    const updateParticlesColor = (isDarkMode) => {
      if (window.pJSDom && window.pJSDom[0] && window.pJSDom[0].pJS) {
        const color = isDarkMode ? '#0a84ff' : '#007aff';
        window.pJSDom[0].pJS.particles.array.forEach(particle => {
          particle.color.value = color;
          particle.color.rgb = hexToRgb(color);
        });
        window.pJSDom[0].pJS.particles.line_linked.color = color;
        window.pJSDom[0].pJS.particles.line_linked.color_rgb_line = hexToRgb(color);
      }
    };
    
    // Вспомогательная функция для конвертации hex в rgb
    function hexToRgb(hex) {
      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
      } : null;
    }
  }
  
  // --- Инициализация Typed.js для эффекта печати ---
  if (typeof Typed !== 'undefined') {
    // Для русского заголовка
    const heroTitleRu = document.getElementById('hero-title-ru');
    if (heroTitleRu && heroTitleRu.textContent) {
      const originalTextRu = heroTitleRu.textContent;
      heroTitleRu.textContent = '';
      
      const typedRu = new Typed(heroTitleRu, {
        strings: [originalTextRu],
        typeSpeed: 60,
        startDelay: 500,
        showCursor: true,
        cursorChar: '|',
        loop: false
      });
    }
    
    // Для английского заголовка
    const heroTitleEn = document.getElementById('hero-title-en');
    if (heroTitleEn && heroTitleEn.textContent) {
      const originalTextEn = heroTitleEn.textContent;
      heroTitleEn.textContent = '';
      
      const typedEn = new Typed(heroTitleEn, {
        strings: [originalTextEn],
        typeSpeed: 60,
        startDelay: 500,
        showCursor: true,
        cursorChar: '|',
        loop: false
      });
    }
  }

  // --- Инициализация AOS для анимаций при скроллинге ---
  if (typeof AOS !== 'undefined') {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }

  // --- Инициализация Fancybox для галереи проектов ---
  const initFancybox = () => {
    if (typeof Fancybox !== 'undefined') {
      Fancybox.bind('[data-fancybox]', {
        // Настройки Fancybox
      });
      
      // Преобразуем слайды проектов для открытия в Fancybox
      document.querySelectorAll('.swiper-slide').forEach(slide => {
        slide.setAttribute('data-fancybox', 'projects');
        slide.setAttribute('data-src', '#' + (slide.id || 'project-modal-' + Math.random().toString(36).substr(2, 9)));
      });
    }
  };
  initFancybox();

  // --- Инициализация Masonry для сетки проектов (альтернативный вид) ---
  const initMasonry = () => {
    const projectGrid = document.querySelector('.project-grid');
    if (projectGrid && typeof Masonry !== 'undefined') {
      new Masonry(projectGrid, {
        itemSelector: '.project-item',
        columnWidth: '.grid-sizer',
        percentPosition: true,
        gutter: 20
      });
    }
  };
  // Активируем Masonry, если на странице есть проектная сетка
  initMasonry();

  // --- API Interaction ---
  const API_BASE_URL = 'http://127.0.0.1:8000/api';
  
  // Функция для загрузки данных из API
  async function fetchFromAPI(endpoint) {
      try {
          const response = await fetch(`${API_BASE_URL}/${endpoint}`);
          if (!response.ok) {
              throw new Error(`API error: ${response.status}`);
          }
          return await response.json();
      } catch (error) {
          console.error(`Failed to fetch ${endpoint}:`, error);
          return null;
      }
  }
  
  // Загрузка всех проектов из API
  async function loadProjects() {
      const projectsData = await fetchFromAPI('projects/');
      if (projectsData && projectsData.results) {
          const projectsContainer = document.querySelector('.swiper-wrapper');
          if (!projectsContainer) return;
          
          // Очищаем контейнер перед добавлением новых данных
          projectsContainer.innerHTML = '';
          
          // Добавляем каждый проект из API
          projectsData.results.forEach(project => {
              const slide = document.createElement('div');
              slide.className = 'swiper-slide card';
              
              // Создаем HTML для проекта на русском
              const titleRu = document.createElement('h3');
              titleRu.setAttribute('data-lang', 'ru');
              titleRu.textContent = project.title_ru || 'Проект';
              
              const descRu = document.createElement('p');
              descRu.setAttribute('data-lang', 'ru');
              descRu.textContent = project.description_ru || 'Описание проекта отсутствует';
              
              // Создаем HTML для проекта на английском
              const titleEn = document.createElement('h3');
              titleEn.setAttribute('data-lang', 'en');
              titleEn.style.display = 'none';
              titleEn.textContent = project.title_en || 'Project';
              
              const descEn = document.createElement('p');
              descEn.setAttribute('data-lang', 'en');
              descEn.style.display = 'none';
              descEn.textContent = project.description_en || 'Project description is not available';
              
              // Добавляем элементы в слайд
              slide.appendChild(titleRu);
              slide.appendChild(titleEn);
              slide.appendChild(descRu);
              slide.appendChild(descEn);
              
              // Если есть ссылка на проект, добавляем ее
              if (project.url) {
                  const linkRu = document.createElement('a');
                  linkRu.href = project.url;
                  linkRu.className = 'project-link';
                  linkRu.setAttribute('data-lang', 'ru');
                  linkRu.textContent = 'Открыть проект';
                  linkRu.target = '_blank';
                  
                  const linkEn = document.createElement('a');
                  linkEn.href = project.url;
                  linkEn.className = 'project-link';
                  linkEn.setAttribute('data-lang', 'en');
                  linkEn.style.display = 'none';
                  linkEn.textContent = 'Open project';
                  linkEn.target = '_blank';
                  
                  slide.appendChild(linkRu);
                  slide.appendChild(linkEn);
              }
              
              projectsContainer.appendChild(slide);
          });
          
          // Обновляем Swiper после загрузки проектов
          if (window.projectSwiper) {
              window.projectSwiper.update();
          }
      }
  }
  
  // Вызываем функцию загрузки проектов при загрузке страницы
  loadProjects(); // Активируем загрузку проектов из API
  
  // --- GSAP & ScrollTrigger Setup ---
  gsap.registerPlugin(ScrollTrigger);
  
  // --- Smooth Scroll & Active Nav Link ---
  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      // Active link styling (basic)
      navLinks.forEach(nav => nav.classList.remove('active'));
      this.classList.add('active');
    });
  });

  // --- Header Scroll Effect ---
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 50);
  });
  
  // --- General Fade-in Animation for Sections & Elements ---
  gsap.utils.toArray('.fade-in').forEach((element) => {
    gsap.fromTo(element,
      { opacity: 0, y: 30 }, // Start state
      { // End state
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: "power2.out",
        scrollTrigger: {
          trigger: element,
          start: "top 85%", // Trigger animation when 85% of element enters viewport
          toggleActions: "play none none none" // Play animation once when it enters
        }
      }
    );
  });
  
  // --- Staggered Animation for List Items ---
  gsap.utils.toArray('.skills-grid .skill-category, .experience-item, .education-list > li').forEach((section) => {
    const listItems = section.querySelectorAll('ul li');
    if(listItems.length > 0) {
      gsap.from(listItems, {
        opacity: 0,
        x: -20,
        duration: 0.5,
        stagger: 0.1, // Delay between each item animating
        ease: "power1.out",
        scrollTrigger: {
          trigger: section, // Trigger when the section starts entering
          start: "top 75%",
          toggleActions: "play none none none"
        }
      });
    }
  });

  // --- Hero Section Animations ---
  const heroTl = gsap.timeline({ delay: 0.2 }); // Add a small delay
  // Не добавляем анимацию для заголовков, так как теперь это делает Typed.js
  heroTl.from('.hero-content .subtitle', { opacity: 0, y: 30, duration: 0.8, ease: "power3.out", delay: 1.2 })
        .from('.hero-content .subtitle-small', { opacity: 0, y: 20, duration: 0.8, ease: "power3.out" }, "-=0.6")
        .from('.hero-actions .cta-button', { opacity: 0, scale: 0.8, duration: 0.6, stagger: 0.2, ease: "back.out(1.7)" }, "-=0.5");

  // --- Current Year ---
  const currentYearElement = document.getElementById('current-year');
  if (currentYearElement) {
    currentYearElement.textContent = new Date().getFullYear();
  } else {
    console.warn("Element with ID 'current-year' not found.");
  }

  // --- Theme Toggle ---
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.body.classList.toggle('dark-mode', savedTheme === 'dark');
  themeBtn.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
  
  themeBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const isDarkMode = document.body.classList.contains('dark-mode');
    themeBtn.textContent = isDarkMode ? '☀️' : '🌙';
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light'); // Save preference
    
    // Обновляем цвет частиц при смене темы
    if (typeof updateParticlesColor === 'function') {
      updateParticlesColor(isDarkMode);
    }
    
    // Обновить AOS анимации после смены темы
    if (typeof AOS !== 'undefined') {
      setTimeout(() => {
        AOS.refresh();
      }, 300);
    }
  });

  // --- Language Toggle ---
  const savedLang = localStorage.getItem('language') || 'ru';
  langBtn.textContent = savedLang === 'ru' ? 'EN' : 'RU';
  document.querySelectorAll('[data-lang]').forEach(el => {
    el.style.display = el.getAttribute('data-lang') === savedLang ? '' : 'none';
  });
  // Set initial HTML lang attribute
  document.documentElement.lang = savedLang;

  langBtn.addEventListener('click', () => {
    const currentLang = document.documentElement.lang;
    const newLang = currentLang === 'ru' ? 'en' : 'ru';
    
    langBtn.textContent = newLang === 'ru' ? 'EN' : 'RU';
    localStorage.setItem('language', newLang); // Save preference
    document.documentElement.lang = newLang; // Update HTML lang attribute
    
    document.querySelectorAll('[data-lang]').forEach(el => {
      el.style.display = el.getAttribute('data-lang') === newLang ? '' : 'none';
    });
    
    // Re-initialize Swiper if needed after language change, as text direction might change
    if (projectSwiper) {
      projectSwiper.update();
    }
    
    // Обновляем typed.js если изменился язык
    if (typeof Typed !== 'undefined') {
      // Здесь можно добавить код для обновления Typed.js при смене языка
    }
  });

  // --- Project Carousel (Swiper JS) ---
  const projectSwiper = new Swiper('.project-swiper', {
    // Optional parameters
    loop: true, // Enable continuous loop mode
    slidesPerView: 1, // Default: show 1 slide at a time
    spaceBetween: 30, // Space between slides
    grabCursor: true, // Show grab cursor on hover
    
    // Responsive breakpoints
    breakpoints: {
      // when window width is >= 768px
      768: {
        slidesPerView: 2,
        spaceBetween: 30
      },
      // when window width is >= 1024px
      1024: {
        slidesPerView: 3,
        spaceBetween: 40
      }
    },
    
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
      clickable: true, // Allow clicking on pagination bullets
    },
    
    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    
    // Keyboard navigation
    keyboard: {
      enabled: true,
      onlyInViewport: true,
    },
  });

  // Экспортируем swiper для использования в других функциях
  window.projectSwiper = projectSwiper;
});