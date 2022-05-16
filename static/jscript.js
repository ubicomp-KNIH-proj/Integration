function moveCursora(tel) {
    if (tel.value.length == 3) {
        document.getElementById("phonenum1").focus();
    }
} // 010에서 넘어가기
function moveCursorb(telbox) {
    if (telbox.value.length == 4) {
        document.getElementById("phonenum2").focus();
    }
}// 1234에서 5678로 넘어가기

// 팝업창 생성
function showPopup() { window.open("pop.html", "a", "width=400, height=300, left=100, top=50"); }
