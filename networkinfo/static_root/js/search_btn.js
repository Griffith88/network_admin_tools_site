const btns = document.getElementById('btn_search');
btns.addEventListener('click', (evt) => {
    const isValidForm = document.getElementById('tab_number').checkValidity();
    if (isValidForm) {
        evt.target.classList.add('activeLoading');
    }
})
