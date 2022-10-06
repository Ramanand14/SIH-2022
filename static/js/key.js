const textarea = document.getElementById('screen');
let screen = document.getElementById('screen');
buttons = document.querySelectorAll('button');

let screenValue = '';
textarea.value = '';
var k;
// clear code
const btn = document.getElementById('back2');
btn.addEventListener('click', function handleClick() {
  
  screenValue = "";
            screen.value = screenValue;

});
 
// backspace code 

const bu = document.getElementById('back1');
bu.addEventListener('click', function() {
  var text = document.getElementById("screen").value;
  text = text.substring(0, text.length - 1);
 
  screen.value=text;
  
})

const backSpace=document.getElementById('b');
backSpace.addEventListener('click',function(){
 
})
// text to speech code 
const btn2 = document.getElementById('back3');
btn2.addEventListener('click', function handleClick() {
  
  window.speechSynthesis.speak(new SpeechSynthesisUtterance(screen.value));

});



for (item of buttons) {
    item.addEventListener('click', (e) => {
        buttonText = e.target.innerText;

        
        console.log('Button text is ', buttonText);
        var text = document.getElementById("screen").value;
        screenValue = text + " " + buttonText;
        screen.value = screenValue;
    
    });
  


}




