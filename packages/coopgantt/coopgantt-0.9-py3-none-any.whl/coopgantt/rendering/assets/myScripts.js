var mousePosition;
var offset = [0,0];
var div;
var isDown = false;


main_gantt = document.getElementById("main_gantt")
gantt_text = document.getElementById("gantt_text")
windowed_view = document.getElementById("windowed_view")

div = document.createElement("div");
div.style.position = "absolute";
div.style.left = "0px";
div.style.top = "0px";
div.style.width = (main_gantt.clientWidth / main_gantt.scrollWidth) * windowed_view.clientWidth + 'px';
div.style.height = (main_gantt.clientHeight / main_gantt.scrollHeight) * windowed_view.clientHeight + 'px';
div.style.background = "orange";
div.style.opacity = "0.3"
div.style.border = "5px solid orange";

windowed_view.appendChild(div);

div.addEventListener('mousedown', function(e) {
    isDown = true;
    offset = [
        div.offsetLeft - e.clientX,
        div.offsetTop - e.clientY
    ];
}, true);

document.addEventListener('mouseup', function() {
    isDown = false;
}, true);

document.addEventListener('mousemove', function(event) {
    event.preventDefault();

    mousePosition = {

      x : event.clientX,
      y : event.clientY

    };

    if (isDown &  (-offset[0] < mousePosition.x < screen.width - div.clientWidth - offset[0])){
        div.style.left = Math.max((mousePosition.x + offset[0]), 0) + 'px';
    }


    if (isDown &  (-offset[1] <= mousePosition.y <= windowed_view.clientHeight - div.clientHeight - offset[1]) ){
        div.style.top = Math.max((mousePosition.y + offset[1]), 0) + 'px';
    }

     if (isDown){
        main_gantt.scrollTo(
            Math.floor((mousePosition.x + offset[0]) / windowed_view.clientWidth * main_gantt.scrollWidth),
            Math.floor((mousePosition.y + offset[1]) / windowed_view.clientHeight * main_gantt.scrollHeight)
        );
        gantt_text.scrollTo(
            gantt_text.scrollLeft,
            Math.floor((mousePosition.y + offset[1]) / windowed_view.clientHeight * gantt_text.scrollHeight)
       )
     }

}, true);


main_gantt.onscroll = function(){
    div.style.left = Math.max((main_gantt.scrollLeft / main_gantt.scrollWidth) * windowed_view.clientWidth, 0) + 'px';

    perc = (main_gantt.scrollTop / main_gantt.scrollHeight)
    div.style.top = perc * windowed_view.clientHeight + 'px';

    gantt_text.scrollTo(
        0,
        Math.round(gantt_text.scrollHeight * perc)
    )
};

gantt_text.onscroll = function(){
    div.style.top = Math.max((main_gantt.scrollTop / main_gantt.scrollHeight) * windowed_view.clientHeight, 0) + 'px';
    perc = gantt_text.scrollTop / gantt_text.scrollHeight

    main_gantt.scrollTo(
        main_gantt.scrollLeft,
        Math.round(main_gantt.scrollHeight * perc)
    )
};