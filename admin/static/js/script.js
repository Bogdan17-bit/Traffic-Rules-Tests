document.addEventListener('DOMContentLoaded', e => {
  let file = document.querySelector('#file'),
      preview = document.querySelector('#preview');
  
  file.addEventListener('change', e => {
    if(file.files.length === 0)
      return;
    
    let f = file.files[0],
        fr = new FileReader();
    

    if(f.type.indexOf('image') === -1)
      return;
    
    fr.onload = e => {
      if(getComputedStyle(preview, null).display === 'none')
        preview.style.display = 'block';
      
      preview.src = e.target.result;
    }
    fr.readAsDataURL(f);
  });
});

var select_is_clicked = false

function SelectorOpen(counts) {
    if (select_is_clicked)
    {
        document.getElementById('dynamic_div').style.marginTop = '20px';
        select_is_clicked = false;
    }
    else
    {
        document.getElementById('dynamic_div').style.marginTop = String(counts*25) +'px';
        select_is_clicked = true;
    }
}

function SelectorClose() {
    document.getElementById('dynamic_div').style.marginTop = '20px';
}
