// ナビゲーションリンクにマウスがホバーされたときの処理
document.addEventListener('DOMContentLoaded', function() {
    var navLinks = document.querySelectorAll('.ul');
    navLinks.forEach(function(navLink) {
      navLink.addEventListener('mouseover', function() {
        navLink.style.color = '#ef1146'; // ホバー時のテキスト色を変更
      });
      navLink.addEventListener('mouseout', function() {
        navLink.style.color = '#ffffff'; // デフォルトのテキスト色に戻す
      });
    });
});

//ナビリンクの色を白に設定
function setNaviLinkColor(){
    var navLinks = document.querySelectorAll('.ul');
    navLinks.forEach(function(navLink) {
        navLink.style.color = '#ffffff';
    });
}
window.onload=setNaviLinkColor();