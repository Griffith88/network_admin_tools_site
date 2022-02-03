document.getElementById('search_type').addEventListener('change', function () {
    if (document.getElementById('search_type').value === 'Пользователь') {
        document.getElementById('value').setAttribute('placeholder', 'Введите имя пользователя')
    } else if (document.getElementById('search_type').value === 'ПК') {
        document.getElementById('value').setAttribute('placeholder', 'Введите имя ПК')
    }
})