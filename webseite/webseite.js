window.addEventListener('scroll', () =>{
    var scrollPosition = window.scrollY;
    var navbar =  document.getElementById("navbar");
    var scroll_down_box = document.getElementById("scroll_down_outer_box");
    var scroll_down_box_inner = document.getElementById("scroll_down");
    var logo_picture = document.getElementById("logo");

    if(scrollPosition > 0){
      navbar.style.backgroundColor="rgba(137, 207, 240, 0.5)";
      scroll_down_box.style.display = "none";
      logo_picture.style.height="130%"
      
      
    }else{
        navbar.style.backgroundColor= null
        scroll_down_box.style.display = "";
        logo_picture.style.height="100%"
        
    }
})

