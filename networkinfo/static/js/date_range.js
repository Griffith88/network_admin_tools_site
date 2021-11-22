function get_date_from_today(shift = 0) {
    const date = new Date();
    date.setDate(date.getDate() - shift)
    let day = date.getDate();
    let month = date.getMonth() + 1;
    const year = date.getFullYear();

    if (day < 10) {
        day = '0' + day;
    }
    if (month < 10) {
        month = '0' + month;
    }
    return year + '-' + month + '-' + day;
}

document.getElementById('startDate').value = get_date_from_today(30)
document.getElementById('endDate').value = get_date_from_today()
document.getElementById('startDate').setAttribute('max', get_date_from_today(1))
document.getElementById('endDate').setAttribute('max', get_date_from_today())
