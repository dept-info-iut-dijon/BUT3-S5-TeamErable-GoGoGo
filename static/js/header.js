document.querySelector('.menu-toggle').addEventListener('click', function(){
    document.querySelector('.nav').classList.toggle('mobile-nav');
    this.classList.toggle('is-active');
});
