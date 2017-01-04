function pad(n) {
    return (n < 10) ? ("0" + n) : n;
}
function commonjs() {
    $('.datetimeinput').datetimepicker({
        format: 'YYYY-MM-DD HH:mm:ss'
    });
}

commonjs();