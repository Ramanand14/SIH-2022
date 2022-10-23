const div1 = document.querySelector('.box1');
div1.addEventListener('click', (event) => {
	localStorage.setItem("l", "Hospital");
	window.open('keybored');
});

const div2 = document.querySelector('.box2');
div2.addEventListener('click', (event) => {
	localStorage.setItem("l", "Bank");
	window.open('keybored')
});

const div3 = document.querySelector('.box3');
div3.addEventListener('click', (event) => {
	localStorage.setItem("l", "School");
	window.open('keybored')
});

const div4 = document.querySelector('.box4');
div4.addEventListener('click', (event) => {
	localStorage.setItem("l", "Restaurant");
	window.open('keybored')
});

const div5 = document.querySelector('.box5');
div5.addEventListener('click', (event) => {
	localStorage.setItem("l", "General");
	window.open('keybored')
});

const div6 = document.querySelector('.box6');
div6.addEventListener('click', (event) => {
  	localStorage.setItem("l", "Market");
	window.open('keybored')
});