const btns = document.getElementById('btn_search');
const create_form = document.getElementById('create_user_form')
create_form.addEventListener('submit', (evt) => {
    const isValidForm = document.getElementById('tab_number').checkValidity();
    if (isValidForm) {
        document.forms['create_user_form'].submit()
        btns.classList.add('activeLoading');
        btns.disabled = true
    }
})
