function reset(){
    document.forms['my-form'].reset()
};

var counter_right_answers = 0;

function check() {
    var inputs = document.querySelectorAll('.radiobtn');
    for (var i = 0; i < inputs.length; i++) {
        if (!inputs[i].disabled) {
            console.log(inputs[i].tagName);
            return 0;
        }
    }
    var submit_btn = document.getElementById('submit_button');
    submit_btn.disabled = false;
    submit_btn.value = String(counter_right_answers)
}

document.addEventListener('change', function () {
  var chk = event.target
  var parent = chk.parentNode;
  var grand = parent.parentNode
  if (chk.tagName === 'INPUT' && chk.type === 'radio') {
     if (chk.value == "True") {
        counter_right_answers += 1;
        grand.style.backgroundColor = "rgb(188,238,176)";
     }
     else {
        grand.style.backgroundColor = 'rgb(255,135,97)';
     }
     var group = document.getElementsByName(chk.name);
     for (var i = 0; i < group.length; i++) {
        group[i].disabled  = true;
     }
  }
  check();
})