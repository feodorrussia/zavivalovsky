$(document).ready(function() { // Ждём загрузки страницы

	$(".image").click(function(){	// Событие клика на маленькое изображение
	  	var img = $(this);	// Получаем изображение, на которое кликнули
		var src = img.attr('src'); // Достаем из этого изображения путь до картинки
		$("body").append("<div id='myCarousel' class='carousel slide border' data-ride='carousel'>"+
            "<div class='carousel-inner'>"+
               "<div class='carousel-item active'><img class='d-block w-100' src='../images/1.jpg' alt='Panther'></div>"+
               "<div class='carousel-item'><img class='d-block w-100' src='/images/2.jpg' alt='Black Cat'></div>"+
               "<div class='carousel-item'><img class='d-block w-100' src='/images/3.jpg' alt='Lion'></div></div></div>"+
               "<a class='carousel-control-prev' href='#myCarousel' role='button' data-slide='prev'>"+
     "<span class='carousel-control-prev-icon' aria-hidden='true'></span>"+
     "<span class='sr-only'>Previous</span>"+
   "</a>"+
   "<a class='carousel-control-next' href='#myCarousel' role='button' data-slide='next'>"+
     "<span class='carousel-control-next-icon' aria-hidden='true'></span>"+
     "<span class='sr-only'>Next</span>"+
   "</a>");
		$(".popup").fadeIn(800); // Медленно выводим изображение
		$(".popup_bg").click(function(){	// Событие клика на затемненный фон
			$(".popup").fadeOut(800);	// Медленно убираем всплывающее окно
			setTimeout(function() {	// Выставляем таймер
			  $(".popup").remove(); // Удаляем разметку всплывающего окна
			}, 800);
		});
	});

});